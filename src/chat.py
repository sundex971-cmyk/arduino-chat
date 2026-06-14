#!/usr/bin/env python3
"""
Arduino Chat - Interactive RAG-based AI assistant for Arduino documentation.
Uses ChromaDB for vector search and Ollama/LangChain for LLM capabilities.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"
DATA_DIR = PROJECT_ROOT / "data" / "docs"
COLLECTION_NAME = "arduino_docs"
EMBEDDING_MODEL = "qwen3-embedding:0.6b"
LLM_MODEL = "qwen3.5:2b"

# Constants
CONTEXT_WINDOW_SIZE = 1
DEFAULT_TIMEOUT = 30
OLLAMA_BASE_URL = "http://localhost:11434"

SYSTEM_PROMPT = """You are an expert Arduino programming assistant. Your role is to help users with:
- Arduino programming, sketches, and coding best practices
- Hardware connections, pins, and microcontroller configuration
- Troubleshooting and debugging Arduino projects
- Providing clear code examples and explanations

When answering questions:
1. Use the provided documentation context as your primary source
2. Give clear, concise explanations suitable for both beginners and advanced users
3. Include code examples when relevant
4. Explain the "why" behind your recommendations
5. If the question falls outside Arduino scope, politely redirect

Always prioritize accuracy, safety, and helpful guidance."""


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
    """Load LLM model from Ollama."""
    try:
        from langchain_ollama import OllamaLLM
    except ImportError:
        try:
            from langchain_community.llms import Ollama
            OllamaLLM = Ollama
        except ImportError:
            raise ImportError(
                "Cannot import OllamaLLM. "
                "Install: pip install langchain-ollama"
            )

    print(f"[INFO] Loading LLM model: {LLM_MODEL}")
    return OllamaLLM(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.7,
        top_p=0.9,
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

    return client.get_collection(name=COLLECTION_NAME)


def retrieve_relevant_docs(
    query: str,
    collection: Any,
    embeddings: Any,
    k: int = CONTEXT_WINDOW_SIZE,
) -> tuple[list[str], list[dict]]:
    """Retrieve relevant documents from vector database."""
    try:
        # Embed the query
        query_embedding = embeddings.embed_query(query)

        # Search in ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"] or not results["documents"][0]:
            return [], []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0] if results["metadatas"][0] else []
        
        return documents, metadatas

    except Exception as e:
        print(f"[ERROR] Failed to retrieve documents: {e}")
        return [], []


def format_context(documents: list[str], metadatas: list[dict]) -> str:
    """Format retrieved documents into context string."""
    if not documents:
        return "No relevant documentation found in the knowledge base."

    context_parts = []
    for i, doc in enumerate(documents):
        metadata = metadatas[i] if i < len(metadatas) else {}
        source = metadata.get("source", "Unknown source")
        context_parts.append(f"[{i + 1}. From {source}]\n{doc}")

    return "\n\n---\n\n".join(context_parts)


def generate_answer(
    llm: Any,
    question: str,
    context: str,
) -> str:
    """Generate answer using LLM with context."""
    prompt = f"""System: {SYSTEM_PROMPT}

Documentation Context:
{context}

User Question: {question}

Provide a helpful and accurate answer based on the documentation. If the documentation doesn't contain relevant information, indicate that and provide general Arduino knowledge if appropriate."""

    try:
        response = llm.invoke(prompt)
        return response.strip() if response else "[No response generated]"
    except Exception as e:
        print(f"[ERROR] Failed to generate answer: {e}")
        return "[Error generating response. Please try again.]"


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
    except (ImportError, FileNotFoundError) as e:
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
