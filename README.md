# 🤖 AI Agent MVP

A minimal AI-powered agent architecture built using **FastAPI**, **MongoDB**, **ChromaDB**, and **DuckDuckGo Search**. This MVP is organized into microservices for **chat**, **knowledge base**, **search**, and **history**.

---

## 📁 Project Structure

```
ai-agent-mvp/
├── chat_service/
├── knowledge_service/
├── search_service/
├── history_service/
└── README.md
```

---

## 🚀 Features

* Chat interface with fallback mechanism
* In-memory knowledge base powered by ChromaDB + Sentence Transformers
* Web search fallback via DuckDuckGo
* History logging using MongoDB
* Modular microservice architecture

---

## 🛠️ Tech Stack

* **FastAPI** — Web framework
* **MongoDB** — For storing chat history
* **ChromaDB** — Embedding-based document storage
* **SentenceTransformers** — Embedding generator (all-MiniLM-L6-v2)
* **DuckDuckGo Search** — Fallback for external queries

---

## 🖥️ Prerequisites

* Python 3.10+ ✅
* MongoDB installed and running locally ✅
* Git installed ✅

---

## 🧾 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-agent-mvp.git
cd ai-agent-mvp
```

### 2. Install Python Dependencies

You can create a virtual environment if desired.

```bash
pip install -r requirements.txt
```

### 3. Start MongoDB

Make sure MongoDB is running locally:

```bash
mongod
```

### 4. Start Services (in separate terminals)

#### Start Knowledge Service

```bash
uvicorn knowledge_service.main:app --port 8001 --reload
```

#### Start Search Service

```bash
uvicorn search_service.main:app --port 8002 --reload
```

#### Start History Service

```bash
uvicorn history_service.main:app --port 8003 --reload
```

#### Start Chat Service

```bash
uvicorn chat_service.main:app --port 8000 --reload
```

---

## ✅ Usage Guide

### Ingest Knowledge

```http
POST http://localhost:8001/ingest
{
  "documents": [
    "Python is a programming language",
    "AI stands for Artificial Intelligence",
    "Prime Minister is Narendra Modi"
  ]
}
```

### Ask a Question

```http
POST http://localhost:8000/chat
{
  "query": "Who is the Prime Minister?"
}
```

### Get Chat History

```http
GET http://localhost:8000/chat/{chat_id}
```

---

## 📦 Example `.env` or Config (if needed)

Update MongoDB or external URLs if you host remotely.

---

## 🔍 Search Fallback Logic

If the answer is **not found in ChromaDB**, the app performs a real-time web search using **DuckDuckGo**, and then logs that result.

---

## 🧠 Knowledge Base Matching Logic

We use cosine distance thresholding:

```python
if distance < 0.5:
  return kb_result
else:
  fallback to search
```

---

## 📜 License

MIT

---

## 🙋‍♂️ Author

Dhruvil — [GitHub](https://github.com/dhruvilad1001)

---

## 🌐 Demo (Coming Soon)

---

Feel free to ⭐ star this repo if you like the project!
Update README.md with full project setup and documentation
