#!/usr/bin/env python3
"""
Arduino Chat - Interactive RAG-based AI assistant for Arduino documentation.
Uses ChromaDB for vector search and Ollama/LangChain for LLM capabilities.
"""

from __future__ import annotations

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

SYSTEM_PROMPT = """You are an expert Arduino programming assistant.

Your job is to answer questions about Arduino clearly, correctly, and consistently.

## Core rules:
- Be factually correct and avoid guessing.
- Use the provided documentation context as the primary source of truth.
- If context is incomplete, you may use general Arduino knowledge.
- Never invent technical details or incorrect electrical explanations.
- Never leave the answer empty.

## Output style:
- Be concise and structured.
- Use simple language.
- Prefer bullet points when explaining concepts.
- Avoid repeating the same idea in different words.

## Response format (always follow):
1. Short definition (1–2 sentences)
2. Key points or modes (bullet list if applicable)
3. Short practical explanation or example (if relevant)

## Safety rules:
- Do not over-explain electronics unless explicitly asked.
- Do not hallucinate functions, modes, or hardware behavior.
- If unsure, say: "This is not clearly defined in the provided documentation."

CRITICAL RULES:
- Never use analogWrite unless explicitly mentioned in context.
- For LED blinking tasks, use ONLY digitalWrite + delay or millis.
- If unsure, say "not in documentation".
- Do not infer hardware behavior.
-Answer in Russian if the question is in Russian, otherwise answer in English.

## Goal:
Help the user understand Arduino quickly and accurately without confusion or unnecessary complexity.
"""


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
        num_ctx=8192,
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
            "Run: python src/ingest.py"
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
            "Re-run src/ingest.py to record and enforce the model match."
        )
        return

    if indexed_model != EMBEDDING_MODEL:
        raise ValueError(
            "Embedding model mismatch: "
            f"vector DB was indexed with {indexed_model!r}, "
            f"but chat is using {EMBEDDING_MODEL!r}. "
            "Use the same EMBEDDING_MODEL in src/ingest.py and src/chat.py, "
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

        MAX_DISTANCE = 0.8

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
            return [], []

        # 4. Сортировка по релевантности (ВАЖНО)
        candidates.sort(key=lambda x: x[2])

        # 5. Берем top-k
        top = candidates[:k]

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

def generate_answer(llm: Any, question: str, context: str) -> str:
    try:
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError:
        return "[Error importing LangChain]"

    has_useful_context = context_is_useful(context)

    context_block = context.strip() if has_useful_context else (
        "No relevant Arduino documentation was retrieved."
    )

    if len(context_block) > 800:
        context_block = context_block[:800]

    grounding_instruction = (
        "Use documentation as primary source."
        if has_useful_context
        else "Answer using general Arduino knowledge."
    )

    user_prompt = f"""Documentation Context:
{context_block}

User Question: {question}

{grounding_instruction}"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

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
) -> tuple[str, dict]:
    """Process a single user query and return answer with metadata."""
    # Retrieve relevant documents
    documents, metadatas = retrieve_relevant_docs(query, collection, embeddings)

    # Format context
    context = format_context(documents, metadatas)

    # Generate answer
    answer = generate_answer(llm, query, context)

    # Format response
    formatted_answer = format_response(answer)

    metadata = {
        "num_sources": len(documents),
        "sources": [m.get("source", "Unknown") for m in metadatas],
        "has_useful_context": context_is_useful(context),
    }

    return formatted_answer, metadata


def interactive_chat(
    collection: Any,
    embeddings: Any,
    llm: Any,
) -> None:
    """Run interactive chat loop."""
    print("\n" + "=" * 70)
    print("🤖 Arduino AI Tutor - RAG-based Chat System")
    print("=" * 70)
    print("\nWelcome! I'm your Arduino programming assistant.")
    print("Ask me anything about Arduino programming, hardware, or troubleshooting.")
    print("\nCommands:")
    print("  'help' - Show this message")
    print("  'exit' or 'quit' - End conversation")
    print("=" * 70 + "\n")

    conversation_count = 0

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(
                    "\n👋 Thank you for using Arduino AI Tutor! "
                    "Happy coding!\n"
                )
                break

            if user_input.lower() == "help":
                print("\n📚 Available commands:")
                print("  'help' - Show this message")
                print("  'exit' or 'quit' - End conversation\n")
                continue

            # Process query
            print("\n⏳ Processing your question...")
            answer, metadata = process_query(user_input, collection, embeddings, llm)

            print(f"\nAssistant: {answer}")
            if metadata["num_sources"] > 0:
                print(f"\n📚 Sources used: {', '.join(metadata['sources'][:2])}")
            print()

            conversation_count += 1

        except KeyboardInterrupt:
            print("\n\n⏹️  Chat interrupted. Thank you for using Arduino AI Tutor!\n")
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
    print("Arduino Chat - Initializing")
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
