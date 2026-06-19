===ENG===
# STEAM AI Tutor (RAG System)

A local AI assistant for learning STEAM through documentation-based retrieval.

## ⚙️ Architecture

The project consists of three main components:

1. `fetch_docs.py` — downloads Arduino documentation  
2. `ingest.py` — creates embeddings and builds the knowledge base (ChromaDB)  
3. `chat.py` — interactive chat interface with the AI assistant  

---

## 🚀 Setup & Installation

### 1. Create and activate virtual environment (Windows / VS Code)

If Python 3.11 is not installed, install it first.

```bash
py -3.11 -m venv venv
```

**Windows (PowerShell):**
```powershell
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

Upgrade pip tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Ollama

```powershell
irm https://ollama.com/install.ps1 | iex
```

---

### 4. Download AI models

```bash
ollama pull qwen3.5:2b
ollama pull qwen3-embedding:0.6b
```

---

### 5. Download Arduino documentation

```bash
python src/core/fetch_docs.py
```

---

### 6. Build knowledge base (vector DB)

```bash
python src/core/ingest.py
```

---

### 7. Start chat interface

```bash
python src/core/chat.py
```

---

## 📌 Notes

- Make sure Ollama service is running before starting `chat.py`
- First run may take time due to embedding generation
- All data is stored locally (no cloud required)

---

## 🧩 Tech Stack

- Python 3.11
- Ollama
- ChromaDB
- LangChain / Embeddings
- Arduino Documentation API

---

=====RU=====
# Локальный AI-ассистент по STEAM документации для обучения.

## 🧠 Что это

Проект использует:
- Ollama (локальная LLM)
- RAG (поиск по документации)
- ChromaDB (векторная база)
- Arduino documentation (GitHub source)

## ⚙️ Архитектура

1. fetch_docs.py — скачивает документацию
2. ingest.py — создаёт embeddings и базу знаний
3. chat.py — чат с пользователем

### 1. Запустить и активировать виртуальное окружение внутри проекта (при работе в VS code). Если до этого не был установлен Python 3.11 - установить. 
```bash
py -3.11 -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip setuptools wheel

### 2. Установить зависимости
pip install -r requirements.txt
```

### 2. Установить Ollama
```powershell 
irm https://ollama.com/install.ps1 | iex

### 3. Установить Ollama модели
ollama pull qwen3.5:2b
ollama pull qwen3-embedding:0.6b
```

### 4. Скачать документацию 
python src/core/fetch_docs.py

### 5. Создать базу знаний
python src/core/ingest.py
```powershell 
python -m src.core.ingest    
```
### 6. Запустить чат
python src/core/chat.py