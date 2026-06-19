#!/usr/bin/env python3
"""
Arduino Chat - Interactive RAG-based AI assistant for Arduino documentation.
Uses ChromaDB for vector search and Ollama/LangChain for LLM capabilities.
"""

from __future__ import annotations

import re
import sys
import os
from typing import Any

try:
    from .config import (
        COLLECTION_EMBEDDING_MODEL_KEY,
        COLLECTION_NAME,
        EMBEDDING_MODEL,
        LLM_MODEL,
        OLLAMA_BASE_URL,
        PROJECT_ROOT,
        VECTOR_DB_DIR,
    )
except ImportError:
    from config import (
        COLLECTION_EMBEDDING_MODEL_KEY,
        COLLECTION_NAME,
        EMBEDDING_MODEL,
        LLM_MODEL,
        OLLAMA_BASE_URL,
        PROJECT_ROOT,
        VECTOR_DB_DIR,
    )

# Constants
CONTEXT_WINDOW_SIZE = 3
DEFAULT_TIMEOUT = 30
DEBUG = os.getenv("ARDUINO_CHAT_DEBUG", "").lower() in {"1", "true", "yes", "on"}
MIN_CONTEXT_CHARS = 120
MAX_HISTORY_PAIRS = 5  # сколько последних пар (вопрос+ответ) хранить в памяти

# ------------------------------------------------------------------ #
# Language detection                                                   #
# ------------------------------------------------------------------ #

# Romanian-specific letters/diacritics — strong signal even without accents
# typed (ă, â, î, ș/ş, ț/ţ) plus a few very common RO words that don't
# appear in Russian.
_RO_MARKERS = re.compile(
    r"[ăâîșşțţ]"
    r"|\b(ce|cum|unde|cand|când|pentru|si|şi|este|sunt|placa|proiect)\b",
    re.IGNORECASE,
)
_CYRILLIC = re.compile(r"[а-яА-ЯёЁ]")


def detect_language(text: str) -> str:
    """Return 'ru', 'ro', or 'en' based on the user's question."""
    if _CYRILLIC.search(text):
        return "ru"
    if _RO_MARKERS.search(text):
        return "ro"
    return "en"


_LANGUAGE_INSTRUCTION = {
    "ru": "Отвечай на русском языке.",
    "ro": "Răspunde în limba română.",
    "en": "Answer in English.",
}

# ------------------------------------------------------------------ #
# Query mode detection: "project" vs "general"                        #
# ------------------------------------------------------------------ #

# Phrases that signal the user wants a full project (schematic-style answer)
# rather than a definition/explanation/debugging answer.
_PROJECT_MARKERS = re.compile(
    r"\b("
    r"проект|сделай|собери|построй|схему|схема подключения|я хочу собрать|я хочу сделать|"
    r"как сделать|как собрать|"
    r"proiect|f[aă]|construie[sș]te|construie[sş]te|schema|vreau să fac|vreau să construiesc|cum să fac|cum să construiesc|"
    r"build|make a project|create a project|design a circuit|wire up"
    r")\b",
    re.IGNORECASE,
)


def detect_query_mode(query: str) -> str:
    """Return 'project' if the user is asking for a full project/circuit,
    otherwise 'general' for definitions, explanations, debugging, etc."""
    return "project" if _PROJECT_MARKERS.search(query) else "general"


# ------------------------------------------------------------------ #
# System prompts                                                       #
# ------------------------------------------------------------------ #

_SHARED_RULES = """## Core rules:
- Be factually correct and avoid guessing.
- Use the provided documentation context as the primary source of truth.
- If context is incomplete, you may use general Arduino/ESP32 knowledge.
- Never invent technical details or incorrect electrical explanations.
- Never leave the answer empty.

## Safety rules:
- Do not hallucinate functions, modes, or hardware behavior.
- If unsure, say: "This is not clearly defined in the provided documentation."
- Never suggest a connection listed as forbidden in the documentation context
  (e.g. signal pin to VCC, VCC to GND, 5V directly to an ESP32 GPIO).
- Always flag voltage-level mismatches between board and component
  (e.g. ESP32 is 3.3V logic, most Arduino boards are 5V logic).

CRITICAL RULES:
- Never use analogWrite unless explicitly mentioned in context.
- For LED blinking tasks, use ONLY digitalWrite + delay or millis.
- ESP32 has no analogWrite — use ledcAttach/ledcWrite (LEDC) instead, and say so
  explicitly if the board is ESP32.
- If unsure, say "not in documentation".
- Do not infer hardware behavior.

## Language:
- If the question is written in Russian (Cyrillic), answer in Russian.
- If the question is written in Romanian, answer in Romanian.
- Otherwise, answer in English.
"""

PROJECT_SYSTEM_PROMPT = f"""You are an expert Arduino and ESP32 hardware assistant.

The user is asking you to design or describe a hardware project (a device, a circuit,
something to build). You MUST answer using EXACTLY the following 6-section format,
in this order, with these exact section titles translated into the answer's language
but keeping the numbering 1-6.

{_SHARED_RULES}

## Required response format (always follow, do not skip or reorder sections):

1. Название проекта / Project name / Numele proiectului
   - One short, descriptive title for the project.

2. Как работает / How it works / Cum funcționează
   - 2-4 sentences explaining the operating principle in simple language.

3. Компоненты / Components / Componente
   - Bullet list of every physical part needed (board, sensors, resistors, etc).
   - Include resistor/capacitor values where relevant.

4. Подключение / Connections / Conexiuni
   - Pin-by-pin wiring list, formatted as "Component pin -> Board pin".
   - Mention the board's logic voltage (5V or 3.3V) and any required
     level-shifting or voltage divider if the documentation context covers it.

5. Альтернативы / Alternatives / Alternative
   - 2-4 bullet points: alternative components or approaches, with a short
     trade-off note for each (cheaper/more accurate/simpler/etc).

6. Предупреждения / Warnings / Avertismente
   - Bullet list of concrete risks: wrong polarity, missing resistor,
     voltage mismatch, current limits, common beginner mistakes.
   - Cross-check against any "forbidden connections" rules present in context
     and call them out explicitly if relevant.

Do not add extra sections. Do not merge sections. If information for a section
is missing from context, use general knowledge but mark uncertain details with
"⚠️ not confirmed in documentation".

For beginner STEAM projects:
- Prefer the simplest solution.
- Use only components from retrieved documentation.
- Do not add advanced alternatives unless requested.
- Always include exact wiring from project documentation.
"""

GENERAL_SYSTEM_PROMPT = f"""You are an expert Arduino and ESP32 programming assistant.

The user is asking a regular question (a definition, an explanation, debugging help,
or a "how does X work" question) — NOT a request to design a full project.
Do NOT use the 6-section project format for these questions.

{_SHARED_RULES}

## Output style:
- Be concise and structured.
- Use simple language.
- Prefer bullet points when explaining concepts.
- Avoid repeating the same idea in different words.

## Response format (always follow):
1. Short definition (1-2 sentences)
2. Key points or modes (bullet list if applicable)
3. Short practical explanation or example (if relevant)

## Goal:
Help the user understand Arduino/ESP32 quickly and accurately without confusion
or unnecessary complexity.
"""


def select_system_prompt(query: str) -> tuple[str, str]:
    """Return (system_prompt, mode) for the given user query."""
    mode = detect_query_mode(query)
    prompt = PROJECT_SYSTEM_PROMPT if mode == "project" else GENERAL_SYSTEM_PROMPT
    return prompt, mode


def trim_history(
    history: list[tuple[str, str]],
    max_pairs: int = MAX_HISTORY_PAIRS,
) -> list[tuple[str, str]]:
    """Keep only the last `max_pairs` (user, assistant) exchanges.

    `history` is a flat list like [("user", "..."), ("assistant", "..."), ...].
    Each pair is 2 entries, so we keep the last max_pairs * 2 entries.
    """
    max_entries = max_pairs * 2
    if len(history) <= max_entries:
        return history
    return history[-max_entries:]


def check_dependencies() -> bool:
    """Check if all required dependencies are installed."""
    required = ["chromadb", "langchain_core", "requests"]
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"[ERROR] Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    return True


def check_ollama_connection(base_url: str = OLLAMA_BASE_URL) -> bool:
    """Verify Ollama server is running and accessible."""
    try:
        import requests
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Cannot connect to Ollama: {e}")
        return False


def load_embeddings() -> Any:
    """Load embedding model from Ollama."""
    try:
        from langchain_ollama import OllamaEmbeddings
    except ImportError:
        try:
            from langchain_community.embeddings import OllamaEmbeddings
        except ImportError:
            raise ImportError(
                "Cannot import OllamaEmbeddings. "
                "Install: pip install langchain-ollama"
            )

    print(f"[INFO] Loading embeddings model: {EMBEDDING_MODEL}")
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)


def load_llm() -> Any:
    """Load chat model from Ollama."""
    try:
        from langchain_ollama import ChatOllama
    except ImportError:
        try:
            from langchain_community.chat_models import ChatOllama
        except ImportError:
            raise ImportError(
                "Cannot import ChatOllama. "
                "Install: pip install langchain-ollama"
            )

    print(f"[INFO] Loading LLM model: {LLM_MODEL}")
    return ChatOllama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.3,
        top_p=0.9,
        num_predict=-1,
        extra_body={"think": False},
        num_ctx=16384,
    )


def load_vector_db() -> Any:
    """Load ChromaDB vector database."""
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        raise ImportError(
            "Cannot import chromadb. "
            "Install: pip install chromadb"
        )

    if not VECTOR_DB_DIR.exists():
        raise FileNotFoundError(
            f"Vector DB not found at {VECTOR_DB_DIR}. "
            "Run: python src/core/ingest.py"
        )

    print(f"[INFO] Loading vector database from {VECTOR_DB_DIR}")
    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    collection = client.get_collection(name=COLLECTION_NAME)
    verify_embedding_model(collection)
    return collection


def verify_embedding_model(collection: Any) -> None:
    """Ensure indexed embeddings use the same model as chat-time search."""
    metadata = collection.metadata or {}
    indexed_model = metadata.get(COLLECTION_EMBEDDING_MODEL_KEY)

    if indexed_model is None:
        print(
            "[WARN] Vector DB does not store embedding model metadata. "
            f"Expected search model: {EMBEDDING_MODEL}. "
            "Re-run src/core/ingest.py to record and enforce the model match."
        )
        return

    if indexed_model != EMBEDDING_MODEL:
        raise ValueError(
            "Embedding model mismatch: "
            f"vector DB was indexed with {indexed_model!r}, "
            f"but chat is using {EMBEDDING_MODEL!r}. "
            "Use the same EMBEDDING_MODEL in src/core/ingest.py and src/core/chat.py, "
            "then re-run ingestion."
        )


def debug_log(title: str, value: Any) -> None:
    """Print verbose diagnostics when ARDUINO_CHAT_DEBUG is enabled."""
    if not DEBUG:
        return

    print(f"\n[DEBUG] {title}")
    print("-" * 70)
    print(value)
    print("-" * 70)


def retrieve_relevant_docs(
    query: str,
    collection: Any,
    embeddings: Any,
    k: int = CONTEXT_WINDOW_SIZE,
) -> tuple[list[str], list[dict]]:
    """Retrieve relevant documents from vector database (stable version)."""
    try:
        # 1. Embed query
        query_embedding = embeddings.embed_query(query)

        # 2. Query vector DB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=max(k * 3, 10),  # берем больше → потом фильтруем
            include=["documents", "metadatas", "distances"],
        )

        docs_batch = results.get("documents", [[]])[0]
        metas_batch = results.get("metadatas", [[]])[0]
        dists_batch = results.get("distances", [[]])[0]

        if not docs_batch:
            return [], []

        MAX_DISTANCE = 1.1  # было 0.8 — слишком строго резало кросс-языковые совпадения
                             # (русский запрос против англоязычных заголовков документов)

        candidates = []

        # 3. Собираем кандидатов (НЕ возвращаем внутри цикла!)
        for i, doc in enumerate(docs_batch):
            if not doc or not doc.strip():
                continue

            dist = dists_batch[i] if i < len(dists_batch) else 999

            if dist > MAX_DISTANCE:
                continue

            meta = metas_batch[i] if i < len(metas_batch) else {}
            if not isinstance(meta, dict):
                meta = {}

            candidates.append((doc.strip(), meta, dist))

        if not candidates:
            debug_log("Retrieval", "No candidates passed MAX_DISTANCE filter")
            return [], []

        # 4. Сортировка по релевантности (ВАЖНО)
        candidates.sort(key=lambda x: x[2])

        # 5. Берем top-k
        top = candidates[:k]

        debug_log(
            "Retrieved sources (source, distance)",
            [(c[1].get("source", "?"), round(c[2], 3)) for c in top],
        )

        final_docs = [c[0] for c in top]
        final_metas = [c[1] for c in top]

        return final_docs, final_metas

    except Exception as e:
        print(f"[ERROR] Failed to retrieve documents: {e}")
        return [], []


def format_context(documents: list[str], metadatas: list[dict]) -> str:
    """Format retrieved documents into context string."""
    if not documents:
        return ""

    context_parts = []
    for i, doc in enumerate(documents):
        if not doc or not doc.strip():
            continue
        metadata = metadatas[i] if i < len(metadatas) else {}
        source = metadata.get("source", "Unknown source")
        context_parts.append(f"[{i + 1}. From {source}]\n{doc.strip()}")

    return "\n\n---\n\n".join(context_parts)


def context_is_useful(context: str) -> bool:
    """Return True when retrieved context is likely useful for grounding."""
    return bool(context and len(context.strip()) >= MIN_CONTEXT_CHARS)


def normalize_llm_response(response: Any) -> str:
    if response is None:
        return ""

    # ChatOllama Message
    if hasattr(response, "content"):
        content = response.content
        if isinstance(content, str) and content.strip():
            return content

    if isinstance(response, str):
        return response

    if isinstance(response, dict):
        return response.get("content") or response.get("response") or ""

    return str(response)


def filter_query_domain(query: str) -> list[str]:
    q = query.lower()

    if "blink" in q or "led" in q:
        return ["digital-io", "pinMode", "digitalWrite"]

    if "analog" in q:
        return ["analog-io"]

    return []


def safe_llm_call(llm, messages, retries: int = 3) -> str:
    last_error = None

    for _ in range(retries):
        try:
            response = llm.invoke(messages)

            # Проверяем причину остановки
            done_reason = (
                response.response_metadata.get("done_reason", "")
                if hasattr(response, "response_metadata")
                else ""
            )
            if done_reason == "length":
                print("[WARN] LLM hit token limit — try increasing num_predict")

            text = normalize_llm_response(response)
            text = text.strip() if text else ""

            if text:
                return text

        except Exception as e:
            last_error = e

    return f"[ERROR] LLM failed after retries: {last_error}"


def generate_answer(
    llm: Any,
    question: str,
    context: str,
    history: list[tuple[str, str]] | None = None,
) -> str:
    try:
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    except ImportError:
        return "[Error importing LangChain]"

    has_useful_context = context_is_useful(context)

    context_block = context.strip() if has_useful_context else (
        "No relevant Arduino documentation was retrieved."
    )

    MAX_CONTEXT_CHARS = 3500  # было 800 — резало документ до того, как доходило
                               # до Connections/Warnings (часто в конце файла)
    if len(context_block) > MAX_CONTEXT_CHARS:
        cut = context_block[:MAX_CONTEXT_CHARS]
        # обрезаем по последнему переносу строки, а не посреди слова/числа
        last_newline = cut.rfind("\n")
        if last_newline > MAX_CONTEXT_CHARS * 0.5:
            cut = cut[:last_newline]
        context_block = cut + "\n[...context truncated...]"

    grounding_instruction = (
        "Use documentation as primary source."
        if has_useful_context
        else "Answer using general Arduino/ESP32 knowledge."
    )

    system_prompt, mode = select_system_prompt(question)
    language = detect_language(question)
    language_instruction = _LANGUAGE_INSTRUCTION[language]

    debug_log("Selected mode", mode)
    debug_log("Detected language", language)

    user_prompt = f"""Documentation Context:
{context_block}

User Question: {question}

{grounding_instruction}
{language_instruction}"""

    # Собираем сообщения: системный промпт -> история диалога -> текущий вопрос
    messages: list[Any] = [SystemMessage(content=system_prompt)]

    if history:
        trimmed = trim_history(history)
        debug_log("History entries used", len(trimmed))
        for role, content in trimmed:
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=user_prompt))

    try:
        response = safe_llm_call(llm, messages)

        if not response:
            return "[No response generated]"

        return response.strip()

    except Exception as e:
        print(f"[ERROR] Failed to generate answer: {e}")
        return "[Error generating response]"


def format_response(response: str) -> str:
    """Format response for better readability."""
    if not response:
        return "[No response]"

    response = response.strip()

    # Remove excessive whitespace
    lines = [line.rstrip() for line in response.split("\n")]
    lines = [line for line in lines if line or (lines and lines[-1])]

    return "\n".join(lines)


def process_query(
    query: str,
    collection: Any,
    embeddings: Any,
    llm: Any,
    history: list[tuple[str, str]] | None = None,
) -> tuple[str, dict]:
    """Process a single user query and return answer with metadata.

    If `history` is provided, it is used as conversation context for the LLM
    and updated in-place with the new (user, assistant) exchange.
    """
    # Retrieve relevant documents
    documents, metadatas = retrieve_relevant_docs(query, collection, embeddings)

    # Format context
    context = format_context(documents, metadatas)

    # Generate answer (with conversation history if provided)
    answer = generate_answer(llm, query, context, history=history)

    # Format response
    formatted_answer = format_response(answer)

    # Update history in-place so the caller's list grows across turns
    if history is not None:
        history.append(("user", query))
        history.append(("assistant", formatted_answer))
        # Сразу обрезаем, чтобы список не рос бесконечно в течение долгой сессии
        trimmed = trim_history(history)
        history[:] = trimmed

    metadata = {
        "num_sources": len(documents),
        "sources": [m.get("source", "Unknown") for m in metadatas],
        "has_useful_context": context_is_useful(context),
        "mode": detect_query_mode(query),
        "language": detect_language(query),
    }

    return formatted_answer, metadata


def interactive_chat(
    collection: Any,
    embeddings: Any,
    llm: Any,
) -> None:
    """Run interactive chat loop."""
    print("\n" + "=" * 70)
    print("🤖 STEAM AI Tutor - RAG-based Chat System")
    print("=" * 70)
    print("\nWelcome! I'm your STEAM programming assistant.")
    print("Ask me anything about STEAM programming, hardware, or troubleshooting.")
    print("\nCommands:")
    print("  'help'  - Show this message")
    print("  'reset' - Forget conversation history and start fresh")
    print("  'exit' or 'quit' - End conversation")
    print("=" * 70 + "\n")

    conversation_count = 0
    # Плоский список (role, content) — память в рамках текущей сессии.
    # Обрезается до последних MAX_HISTORY_PAIRS пар внутри process_query().
    conversation_history: list[tuple[str, str]] = []

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(
                    "\n👋 Thank you for using STEAM AI Tutor! "
                    "Happy coding!\n"
                )
                break

            if user_input.lower() == "help":
                print("\n📚 Available commands:")
                print("  'help'  - Show this message")
                print("  'reset' - Forget conversation history and start fresh")
                print("  'exit' or 'quit' - End conversation\n")
                continue

            if user_input.lower() == "reset":
                conversation_history.clear()
                print("\n🔄 Conversation history cleared.\n")
                continue

            # Process query (history is read AND updated in-place here)
            print("\n⏳ Processing your question...")
            answer, metadata = process_query(
                user_input, collection, embeddings, llm,
                history=conversation_history,
            )

            print(f"\nAssistant: {answer}")
            if metadata["num_sources"] > 0:
                print(f"\n📚 Sources used: {', '.join(metadata['sources'][:2])}")
            print()

            conversation_count += 1

        except KeyboardInterrupt:
            print("\n\n⏹️  Chat interrupted. Thank you for using STEAM AI Tutor!\n")
            break
        except EOFError:
            print("\n👋 End of input. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.\n")


def main() -> None:
    """Main entry point."""
    print("\n" + "=" * 70)
    print("STEAM Chat - Initializing")
    print("=" * 70 + "\n")

    # Check dependencies
    print("[CHECK] Verifying dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("[OK] All dependencies available\n")

    # Check Ollama connection
    print("[CHECK] Connecting to Ollama server...")
    if not check_ollama_connection():
        print("[ERROR] Ollama is not running!")
        print("Start it with: ollama serve")
        sys.exit(1)
    print("[OK] Connected to Ollama\n")

    # Load components
    try:
        print("[SETUP] Loading components...")
        embeddings = load_embeddings()
        llm = load_llm()
        collection = load_vector_db()
        print("[OK] All components loaded\n")
    except (ImportError, FileNotFoundError, ValueError) as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Start chat
    try:
        interactive_chat(collection, embeddings, llm)
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user\n")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()