from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "docs"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

COLLECTION_NAME = "arduino_docs"
COLLECTION_EMBEDDING_MODEL_KEY = "embedding_model"

EMBEDDING_MODEL = "qwen3-embedding:0.6b"
LLM_MODEL = "qwen3.5:2b"
OLLAMA_BASE_URL = "http://localhost:11434"
