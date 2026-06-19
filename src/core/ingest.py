from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .config import (
        COLLECTION_EMBEDDING_MODEL_KEY,
        COLLECTION_NAME,
        DATA_DIR,
        EMBEDDING_MODEL,
        PROJECT_ROOT,
        VECTOR_DB_DIR,
    )
    from ..tools.chunking import split_text
except ImportError:
    from config import (
        COLLECTION_EMBEDDING_MODEL_KEY,
        COLLECTION_NAME,
        DATA_DIR,
        EMBEDDING_MODEL,
        PROJECT_ROOT,
        VECTOR_DB_DIR,
    )
    from tools.chunking import split_text

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
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={COLLECTION_EMBEDDING_MODEL_KEY: EMBEDDING_MODEL},
    )

    metadata = collection.metadata or {}
    indexed_model = metadata.get(COLLECTION_EMBEDDING_MODEL_KEY)
    if indexed_model and indexed_model != EMBEDDING_MODEL:
        raise SystemExit(
            "Embedding model mismatch: "
            f"existing collection uses {indexed_model!r}, "
            f"but ingestion is configured for {EMBEDDING_MODEL!r}. "
            "Delete/rebuild vector_db or use the original embedding model."
        )

    if not indexed_model:
        collection.modify(
            metadata={COLLECTION_EMBEDDING_MODEL_KEY: EMBEDDING_MODEL}
        )

    return collection


def create_metadata(file_path: Path) -> dict[str, Any]:
    """
    Creates metadata based on document location.

    Folder structure (flat, one file per board+component or topic):

    data/docs/
        arduino/...                       -> category: arduino
        esp32/...                         -> category: esp32
        components/...                    -> category: components
        connections/arduino_uno_hc-sr04.txt
                                           -> category: connections
                                              board: arduino_uno
                                              component: hc-sr04
        projects/...                      -> category: projects
        rules/...                         -> category: rules
    """
    relative_path = file_path.relative_to(DATA_DIR)
    parts = relative_path.parts

    # First folder under data/docs/ is always the category
    category = parts[0] if len(parts) > 1 else "uncategorized"

    metadata: dict[str, Any] = {
        "source": str(relative_path),
        "filename": file_path.name,
        "category": category,
    }

    if category == "connections":
        # Filenames look like: arduino_uno_hc-sr04.txt, esp32_dht22.txt
        stem = file_path.stem  # filename without .txt

        known_boards = ["arduino_uno", "arduino_nano", "arduino_mega", "esp32"]
        board = next((b for b in known_boards if stem.startswith(b)), None)

        if board:
            metadata["board"] = board
            metadata["component"] = stem[len(board) + 1:]  # +1 strips the underscore
        else:
            metadata["board"] = "unknown"
            metadata["component"] = stem

    return metadata


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

    base_metadata = create_metadata(file_path)

    ids = [f"{file_path.stem}:{i}" for i in range(len(chunks))]
    vectors = embeddings.embed_documents(chunks)
    metadatas = [
        {**base_metadata, "chunk_index": i}
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=chunks,
        metadatas=metadatas,
    )

    print(f"[OK] {file_path.name} ({len(chunks)} chunks)")
    return len(chunks)


def main() -> None:
    if not DATA_DIR.exists():
        raise SystemExit(f"Data directory does not exist: {DATA_DIR}")

    files = sorted(set(DATA_DIR.rglob("*.txt")) | set(DATA_DIR.rglob("*.md")))
    if not files:
        raise SystemExit(f"No documents found in {DATA_DIR}")

    embeddings = create_embeddings()
    collection = create_collection()

    total_chunks = 0
    for file_path in files:
        total_chunks += process_file(file_path, collection, embeddings)

    print(f"[OK] Ingestion complete: {len(files)} files, {total_chunks} chunks")


if __name__ == "__main__":
    main()