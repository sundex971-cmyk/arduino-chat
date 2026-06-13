from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .chunking import split_text
except ImportError:
    from chunking import split_text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "docs"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"
COLLECTION_NAME = "arduino_docs"
EMBEDDING_MODEL = "qwen3-embedding:8b"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def create_embeddings() -> Any:
    try:
        from langchain_ollama import OllamaEmbeddings
    except ImportError:
        try:
            from langchain_community.embeddings import OllamaEmbeddings
        except ImportError as error:
            raise SystemExit(
                "Missing embedding dependency. Install langchain-ollama "
                "or langchain-community before running ingestion."
            ) from error

    return OllamaEmbeddings(model=EMBEDDING_MODEL)


def create_collection() -> Any:
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError as error:
        raise SystemExit(
            "Missing vector DB dependency. Install chromadb before running ingestion."
        ) from error

    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_or_create_collection(name=COLLECTION_NAME)


def process_file(file_path: Path, collection: Any, embeddings: Any) -> int:
    print(f"[INFO] Processing {file_path.name}")

    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"[ERROR] Failed to read {file_path}: {error}")
        return 0

    chunks = split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    if not chunks:
        print(f"[WARN] Skipping empty file: {file_path.name}")
        return 0

    ids = [f"{file_path.stem}:{i}" for i in range(len(chunks))]
    vectors = embeddings.embed_documents(chunks)
    metadatas = [
        {
            "source": file_path.name,
            "path": str(file_path.relative_to(PROJECT_ROOT)),
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def main() -> None:
    if not DATA_DIR.exists():
        raise SystemExit(f"Data directory does not exist: {DATA_DIR}")

    files = sorted(DATA_DIR.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files found in {DATA_DIR}")

    embeddings = create_embeddings()
    collection = create_collection()

    total_chunks = 0
    for file_path in files:
        total_chunks += process_file(file_path, collection, embeddings)

    print(f"[OK] Ingestion complete: {len(files)} files, {total_chunks} chunks")


if __name__ == "__main__":
    main()
