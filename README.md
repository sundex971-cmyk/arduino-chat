# Arduino AI Tutor (RAG System)

Локальный AI-ассистент по Arduino документации для обучения.

## 🧠 Что это

Проект использует:
- Ollama (локальная LLM)
- RAG (поиск по документации)
- ChromaDB (векторная база)
- Arduino documentation (GitHub source)

## ⚙️ Архитектура

1. scraper.py — скачивает документацию
2. ingest.py — создаёт embeddings и базу знаний
3. chat.py — чат с пользователем

### 1. Установить зависимости
```bash
pip install -r requirements.txt

### 2. Установить Ollama модели
ollama pull qwen3.5:2b
ollama pull qwen3-embedding:0.6b

### 3. Скачать документацию 
python src/scraper.py

### 4. Создать базу знаний
python src/ingest.py

### 5. Запустить чат
python src/chat.py