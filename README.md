# 🤖 RAG-Based Organizational Knowledge Chatbot

## Transforming Organizational Knowledge into Intelligent Conversations

A Retrieval-Augmented Generation (RAG) powered chatbot that enables users to interact with organizational documents through natural language conversations. Built using React, FastAPI, ChromaDB, LangChain, and Groq LLMs, the system retrieves relevant information from PDFs and CSVs and generates context-aware responses grounded in source documents.

---

## 🚀 Tech Stack

**React • Vite • FastAPI • ChromaDB • LangChain • Groq • Hugging Face**

---

## 📖 Overview

The RAG-Based Organizational Knowledge Chatbot is designed to help organizations unlock the value of their internal documents through AI-powered search and conversation.

By combining semantic search, vector embeddings, and Large Language Models, the chatbot can retrieve relevant information from PDFs and CSV files and generate accurate, context-aware answers. The system reduces hallucinations by grounding responses in actual organizational knowledge stored within the document repository.

---

## ✨ Core Features

### 📄 Multi-Document Knowledge Base

Supports ingestion and retrieval from PDF and CSV documents stored in the knowledge repository.

### 🔍 Semantic Search Engine

Uses vector embeddings and similarity search to retrieve the most relevant document chunks based on user queries.

### 🤖 AI-Powered Response Generation

Leverages Groq LLMs through LangChain to generate natural, context-aware responses.

### 💬 Interactive Chat Interface

Modern React-based chat UI with real-time conversations and response rendering.

### 🧠 Retrieval-Augmented Generation (RAG)

Combines document retrieval with LLM reasoning to improve answer accuracy and reduce hallucinations.

### ⚡ FastAPI Backend Services

High-performance REST API handling document retrieval, embeddings, and AI response generation.

### 🔐 Secure Environment Configuration

Uses environment variables to securely manage API keys and application settings.

---

## 🔄 Project Architecture & User Flow

### Flow Walkthrough

1. User enters a question through the React chat interface.
2. Frontend sends the query to the FastAPI backend.
3. Backend performs semantic similarity search on ChromaDB.
4. Relevant document chunks are retrieved from the vector database.
5. Retrieved context is passed to the Groq LLM.
6. Groq generates a grounded response using retrieved knowledge.
7. Response is returned and displayed in the chat interface.

```text
rag-chatbot/
│
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Backend dependencies
│   └── chroma_db/              # Vector database storage
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   └── components/         # UI components
│   │
│   ├── package.json
│   └── vite.config.js
│
├── docs/                       # Source PDF & CSV documents
│
├── app.py                      # Experimental RAG script
├── .env                        # Environment variables
├── .gitignore
└── README.md
```


---

## 🧠 The RAG Pipeline

Rather than relying solely on LLM knowledge, the chatbot retrieves information directly from organizational documents before generating responses.

### 📥 Document Loading

* Loads PDF documents using PyPDFLoader.
* Loads CSV files using LangChain document loaders.
* Processes all files stored in the `docs/` directory.

### ✂️ Text Chunking

* Splits large documents into manageable chunks.
* Uses RecursiveCharacterTextSplitter for efficient retrieval.

### 🔢 Embedding Generation

* Converts text chunks into dense vector embeddings.
* Uses Hugging Face model:
  `sentence-transformers/all-MiniLM-L6-v2`

### 🗄️ ChromaDB Vector Store

* Stores embeddings in a persistent local vector database.
* Enables fast semantic similarity searches.

### 🔎 Retrieval

* Finds the most relevant document chunks for a given query.
* Retrieves contextual information to support answer generation.

### 🤖 Response Synthesis

* Uses ChatGroq via LangChain.
* Combines user query and retrieved context.
* Generates grounded and context-aware responses.

---

## 🛠️ Tech Stack Breakdown

### Frontend

* React 18
* Vite
* Axios
* Modern Chat UI Components

### Backend

* FastAPI
* Uvicorn
* Pydantic
* CORS Middleware

### AI & Machine Learning

* LangChain
* LangChain Community
* ChatGroq
* Hugging Face Embeddings
* Retrieval-Augmented Generation

### Database & Storage

* ChromaDB Vector Store
* Local Document Repository
* Persistent Embedding Storage

---

## 📁 Project Structure

```text
RAG_PROJECT/
│
├── .env.example
├── .gitignore
├── README.md
├── app.py
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── chroma_db/
│
├── docs/
│   ├── PDF Documents
│   └── CSV Files
│
└── frontend/
    ├── .env.example
    ├── package.json
    ├── vite.config.js
    │
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── components/
        │   ├── ChatBubble.jsx
        │   └── TypingIndicator.jsx
        └── styles/
            └── app.css
```

---

## 💻 Local Installation & Setup

### Prerequisites

* Python 3.10+
* Node.js 18+
* npm
* Groq API Key

### 1. Clone Repository

```bash
git clone https://github.com/dhivya-shreetha-s/RAG-Based-Organizational-Knowledge-Chatbot-.git

cd RAG-Based-Organizational-Knowledge-Chatbot-
```

### 2. Backend Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r backend/requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend

npm install
```

---

## 🔑 Environment Variables

Create a root `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## ▶️ Running the Application

### Start Backend

```bash
cd backend

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend

```bash
cd frontend

npm run dev
```

Open:

```text
http://localhost:5173
```

---

## ☁️ Deployment Guide

### Backend Deployment

* Render
* Railway
* Azure App Service
* AWS EC2
* Docker Containers

### Frontend Deployment

* Vercel
* Netlify
* Firebase Hosting

### Production Notes

* Configure GROQ_API_KEY as an environment variable.
* Persist ChromaDB storage across deployments.
* Configure CORS for frontend-backend communication.

---

## 📤 GitHub Push Instructions

```bash
git init

git add .

git commit -m "Initial commit: RAG-Based Organizational Knowledge Chatbot"

git branch -M main

git remote add origin https://github.com/dhivya-shreetha-s/RAG-Based-Organizational-Knowledge-Chatbot-.git

git push -u origin main
```

---

## 🚀 Future Enhancements

* Document Upload Interface
* Source Citation Support
* Multi-user Authentication
* Role-Based Access Control
* DOCX, PPTX & TXT Support
* Chat History Persistence
* Cloud Vector Database Integration
* Voice-Based Interaction

---

## 📝 Notes

* `backend/main.py` contains the production FastAPI RAG API.
* `frontend/src/App.jsx` powers the chat interface.
* `chroma_db/` stores persistent vector embeddings.
* `docs/` acts as the organizational knowledge repository.

---

## 💼 Why This Project Matters

Organizations generate large amounts of information that often remain difficult to access. This project demonstrates how Retrieval-Augmented Generation can transform static documents into intelligent conversational knowledge systems, enabling faster information discovery, improved productivity, and AI-assisted decision-making.
