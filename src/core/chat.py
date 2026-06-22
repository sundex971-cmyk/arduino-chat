#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
import os
from typing import Any

try:
    from .config import (
        COLLECTION_EMBEDDING_MODEL_KEY,
        COLLECTION_NAME,
        DATA_DIR,
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
        DATA_DIR,
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


def read_positive_int_env(name: str, default: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return value if value > 0 else default


OUTPUT_TOKEN_LIMIT = read_positive_int_env("ARDUINO_CHAT_OUTPUT_TOKEN_LIMIT", 1500)
HISTORY_TOKEN_LIMIT = read_positive_int_env("ARDUINO_CHAT_HISTORY_TOKEN_LIMIT", 3000)

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
    "ru": "Отвечай только на русском языке. Не используй английский или румынский в заголовках и пояснениях.",
    "ro": "Răspunde numai în limba română. Nu folosi engleza sau rusa în titluri și explicații.",
    "en": "Answer only in English. Do not use Russian or Romanian in headings or explanations.",
}

_PROJECT_SECTION_TITLES = {
    "ru": [
        "Название проекта",
        "Как работает",
        "Компоненты",
        "Подключение",
        "Альтернативы",
        "Предупреждения",
    ],
    "ro": [
        "Numele proiectului",
        "Cum funcționează",
        "Componente",
        "Conexiuni",
        "Alternative",
        "Avertismente",
    ],
    "en": [
        "Project name",
        "How it works",
        "Components",
        "Connections",
        "Alternatives",
        "Warnings",
    ],
}

_PIN_UNKNOWN_TEXT = {
    "ru": "Подключение пинов не определено в документации.",
    "ro": "Conexiunea pinilor nu este definită în documentație.",
    "en": "Pin connection is not defined in the documentation.",
}

_GENERAL_FORMAT_TITLES = {
    "ru": ["Краткое определение", "Важные моменты", "Простой пример"],
    "ro": ["Definiție scurtă", "Puncte importante", "Exemplu simplu"],
    "en": ["Short definition", "Important points", "Simple example"],
}

_COMPONENT_GROUP_LABELS = {
    "ru": ["обязательные компоненты", "опциональные улучшения"],
    "ro": ["componente obligatorii", "îmbunătățiri opționale"],
    "en": ["required components", "optional improvements"],
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
- The provided documentation context is the primary and preferred source of truth.
- Use general Arduino/ESP32 knowledge ONLY when it does not contradict the documentation.
- If information is missing, clearly say: "This is not defined in the provided documentation."
- Never invent components, modules, libraries, pin connections, voltage values, or hardware specifications.
- Never create professional or industrial solutions unless explicitly requested.
- Prefer simple educational solutions suitable for children.

## RAG rules:
- Always prioritize retrieved documentation over your own knowledge.
- Do not combine unrelated components from different documents unless the user asks for alternatives.
- Do not assume that a component exists in the project if it is not mentioned in context.
- If no matching documentation is found, explain this instead of designing a complete system from imagination.

## Safety rules:
- Never hallucinate hardware behavior.
- Never invent forbidden connections.
- Always check voltage compatibility:
  - Arduino Uno/Nano: usually 5V logic.
  - ESP32: 3.3V logic.
- Mention voltage protection only when it is actually relevant.
- Do not add unnecessary drivers, converters, or protection circuits.

## Beginner electronics rules:
- Prefer Arduino Uno + basic components for beginner projects.
- Prefer the simplest working design.
- Avoid adding WiFi, cameras, RFID, cloud systems, or advanced modules unless:
  1. they exist in documentation, or
  2. the user explicitly requests them.

## Response length:
- Keep answers concise.
- Do not repeat information.
- Avoid long theoretical explanations.
- For project descriptions: maximum ~1000 words.

## Documentation priority:
- When a retrieved document describes a project, follow that project exactly.
- Do not improve, redesign, or expand the project.
- Do not replace documented components with alternatives.
- Do not add optional features unless explicitly requested.
- Do not repeat the same information.
- Do not copy the same sentence twice.

## Hardware accuracy:
- Never invent pin numbers.
- Never invent voltage values.
- Never invent electrical requirements.
- Never invent detection thresholds, distance ranges, timing, buttons, or timers.
- If a value is not in documentation, say it is unknown.
- Preserve exact component names from documentation.
- Do not replace specific components with generic categories.
- Never shorten HC-SR04 to HC-SR4.

## Language:
- If the question is written in Russian (Cyrillic), answer in Russian.
- If the question is written in Romanian, answer in Romanian.
- Otherwise, answer in English.
"""


def build_project_system_prompt(language: str) -> str:
    titles = _PROJECT_SECTION_TITLES[language]
    unknown_pin_text = _PIN_UNKNOWN_TEXT[language]
    component_group_labels = _COMPONENT_GROUP_LABELS[language]

    return f"""You are an Arduino and ESP32 STEAM tutor for children.

The user is asking you to design or describe a hardware project.
Answer in the user's language only.

You MUST answer using EXACTLY the following 6-section format and section titles.

{_SHARED_RULES}

## Required response format:

1. {titles[0]}
   - Give a short educational project name.
   - Do not describe an industrial system.

2. {titles[1]}
   - Explain the working principle in simple language.
   - Describe only the components actually used.
   - Maximum 4-5 sentences.

3. {titles[2]}
   - List only required physical components.
   - Separate:
     - {component_group_labels[0]}
     - {component_group_labels[1]}
   - Do not add advanced components without request.

4. {titles[3]}
   - If verified wiring is available, write only: VERIFIED_CONNECTIONS
   - Otherwise say: "{unknown_pin_text}"
   - Do not explain wiring in your own words.

5. {titles[4]}
   - Give alternatives only if useful.
   - Maximum 2 alternatives.
   - Explain the trade-off briefly.
   - Do not add unnecessary complexity.

6. {titles[5]}
   - Mention only real beginner mistakes:
     - wrong polarity
     - missing resistor
     - voltage mismatch
     - power problems
   - Do not invent risks.

## Extra project rules:
- Prefer beginner STEAM projects:
  Arduino + sensors + simple outputs.
- Do not transform a simple school project into an industrial automation system.
- Do not add cameras, AI, servers, RFID, or cloud features unless requested.

"""


def build_general_system_prompt(language: str) -> str:
    titles = _GENERAL_FORMAT_TITLES[language]

    return f"""You are an Arduino and ESP32 programming assistant for children.

The user asks a general question:
definition, explanation, debugging, or programming help.

Do NOT use the project format.
Answer in the user's language only.

{_SHARED_RULES}

## Output style:
- Be concise.
- Use simple explanations.
- Prefer examples.
- Avoid unnecessary complexity.

## Response format:

1. {titles[0]}
2. {titles[1]}
3. {titles[2]} (if useful)

## Goal:
Help beginners understand Arduino and ESP32 accurately.
Do not overwhelm the user with advanced information.
"""


def select_system_prompt(query: str) -> tuple[str, str]:
    """Return (system_prompt, mode) for the given user query."""
    mode = detect_query_mode(query)
    language = detect_language(query)
    prompt = (
        build_project_system_prompt(language)
        if mode == "project"
        else build_general_system_prompt(language)
    )
    return prompt, mode


def approx_tokens(text: str) -> int:
    """Conservative token estimate for trimming local prompts/responses."""
    if not text:
        return 0

    words = len(re.findall(r"\S+", text))
    non_space_chars = len(re.sub(r"\s+", "", text))
    char_divisor = 3 if _CYRILLIC.search(text) else 4

    return max(1, int(words / 0.75), (non_space_chars + char_divisor - 1) // char_divisor)


def trim_history_by_tokens(
    history: list[tuple[str, str]],
    max_tokens: int = HISTORY_TOKEN_LIMIT,
) -> list[tuple[str, str]]:
    """Keep most recent exchanges while total estimated tokens <= max_tokens."""
    total = 0
    kept = []
    # идём с конца, чтобы сохранить последние сообщения
    for role, text in reversed(history):
        t = approx_tokens(text)
        if total + t > max_tokens:
            break
        kept.append((role, text))
        total += t
    return list(reversed(kept))


def trim_history(
    history: list[tuple[str, str]],
    max_pairs: int = MAX_HISTORY_PAIRS,
    max_tokens: int = HISTORY_TOKEN_LIMIT,
) -> list[tuple[str, str]]:
    """Keep recent conversation turns within both pair and token limits."""
    max_messages = max_pairs * 2
    recent = history[-max_messages:] if max_messages > 0 else []
    return trim_history_by_tokens(recent, max_tokens=max_tokens)


def limit_text_by_tokens(text: str, max_tokens: int = OUTPUT_TOKEN_LIMIT) -> str:
    """Hard fallback when the model ignores the requested output length."""
    if approx_tokens(text) <= max_tokens:
        return text

    pieces = re.split(r"(\s+)", text.strip())
    kept: list[str] = []

    for piece in pieces:
        candidate = "".join(kept) + piece
        if approx_tokens(candidate) > max_tokens:
            break
        kept.append(piece)

    trimmed = "".join(kept).rstrip()
    if trimmed:
        return trimmed

    return text[: max(1, max_tokens * 3)].rstrip()


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
        temperature=0.2,
        top_p=0.9,
        num_predict=OUTPUT_TOKEN_LIMIT, # native Ollama output-token cap
        reasoning=False,
        num_ctx=4096,                   # уменьшенный контекст для 2B модели
        repeat_penalty=1.2,
        stop=["<END>", "<STOP>"],       # явные стоп-токены
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


def normalize_arrow(text: str) -> str:
    return text.replace("→", "->").strip()


def extract_connections_from_text(text: str) -> list[str]:
    """Extract wiring lines from a Markdown-like Connections section."""
    match = re.search(
        r"(?ims)^##\s*(?:Connections|Hardware connection)\s*$"
        r"(?P<body>.*?)(?=^##\s+|\Z)",
        text,
    )
    if not match:
        return []

    lines: list[str] = []
    component = ""

    for raw_line in match.group("body").splitlines():
        line = raw_line.strip().strip("-")
        if not line:
            continue
        if line.startswith("###"):
            continue
        if line.endswith(":"):
            component = line[:-1].strip()
            continue

        line = normalize_arrow(line)
        if "->" in line:
            lines.append(f"{component} {line}".strip() if component else line)
        elif component and re.fullmatch(r"(?:D|A|GPIO)?\d+|GND|5V|3\.3V", line, re.I):
            lines.append(f"{component} signal/control pin -> {line}")

    return lines


def extract_main_components_from_text(text: str) -> list[str]:
    """Extract component names from a Markdown-like Main components section."""
    match = re.search(
        r"(?ims)^##\s*Main components\s*$"
        r"(?P<body>.*?)(?=^##\s+|\Z)",
        text,
    )
    if not match:
        return []

    components: list[str] = []
    label = ""

    for raw_line in match.group("body").splitlines():
        line = raw_line.strip().strip("-")
        if not line:
            continue
        if line.endswith(":"):
            label = line[:-1].strip()
            continue
        if label.lower() == "optional":
            continue
        components.append(f"{label}: {line}" if label else line)

    return components


def read_first_project_source(metadatas: list[dict]) -> str:
    for metadata in metadatas:
        if metadata.get("category") != "projects":
            continue

        source = metadata.get("source")
        if not source:
            continue

        source_path = (DATA_DIR / source).resolve()
        try:
            source_path.relative_to(DATA_DIR.resolve())
            return source_path.read_text(encoding="utf-8")
        except (OSError, ValueError):
            continue

    return ""


def verified_connections_from_sources(metadatas: list[dict]) -> list[str]:
    """Read exact wiring from retrieved project documents when available."""
    text = read_first_project_source(metadatas)
    return extract_connections_from_text(text) if text else []


def verified_components_from_sources(metadatas: list[dict]) -> list[str]:
    """Read exact component list from retrieved project documents when available."""
    text = read_first_project_source(metadatas)
    return extract_main_components_from_text(text) if text else []


def replace_connections_section(response: str, connections: list[str]) -> str:
    """Replace the model-written project wiring with verified document wiring."""
    if not connections:
        return response

    replacement_body = "\n".join(f"- {line}" for line in connections)
    if "VERIFIED_CONNECTIONS" in response:
        return response.replace("VERIFIED_CONNECTIONS", replacement_body)

    pattern = re.compile(
        r"(?s)((?:##\s*)?(?:4\.\s*)?(?:Подключение|Connections|Conexiuni)[^\n]*\n)"
        r".*?"
        r"(?=\n(?:##\s*)?(?:5\.\s*)?(?:Альтернативы|Alternatives|Alternative)\b)",
    )

    updated, count = pattern.subn(r"\1" + replacement_body + "\n", response, count=1)
    return updated if count else response


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
                print(
                    f"[WARN] LLM output reached the {OUTPUT_TOKEN_LIMIT}-token limit; "
                    "the answer may be truncated."
                )

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
    verified_connections: list[str] | None = None,
    verified_components: list[str] | None = None,
) -> str:
    try:
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    except ImportError:
        return "[Error importing LangChain]"

    has_useful_context = context_is_useful(context)

    context_block = context.strip() if has_useful_context else (
        "No relevant Arduino documentation was retrieved."
    )

    MAX_CONTEXT_CHARS = 3500
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
{language_instruction}
Keep the final answer within {OUTPUT_TOKEN_LIMIT} tokens."""

    if verified_connections:
        user_prompt += """

Verified wiring is available.
In section 4, write exactly one line: VERIFIED_CONNECTIONS"""

    if verified_components:
        component_lines = "\n".join(f"- {line}" for line in verified_components)
        user_prompt += f"""

Verified required components from documentation:
{component_lines}

Use these exact components in section 3. Do not omit any of them."""

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

        response = response.strip()
        if mode == "project" and verified_connections:
            response = replace_connections_section(response, verified_connections)

        return limit_text_by_tokens(response, OUTPUT_TOKEN_LIMIT)

    except Exception as e:
        print(f"[ERROR] Failed to generate answer: {e}")
        return "[Error generating response]"


def format_response(response: str) -> str:
    """Format response for better readability."""
    if not response:
        return "[No response]"

    response = response.strip()
    response = re.sub(r"\bHC-SR4\b", "HC-SR04", response)

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
    verified_connections = verified_connections_from_sources(metadatas)
    verified_components = verified_components_from_sources(metadatas)

    # Generate answer (with conversation history if provided)
    answer = generate_answer(
        llm,
        query,
        context,
        history=history,
        verified_connections=verified_connections,
        verified_components=verified_components,
    )

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
        "verified_connections": verified_connections,
        "verified_components": verified_components,
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
