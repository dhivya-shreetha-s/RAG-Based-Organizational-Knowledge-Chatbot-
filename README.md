# RAG-Based Organizational Knowledge Chatbot

A retrieval-augmented generation (RAG) chatbot built with:
- `FastAPI` backend in `backend/main.py`
- `React` frontend in `frontend/src`
- `Chroma` vector store for embeddings
- `Groq` LLM integration via `langchain-groq`

## Project structure

- `backend/main.py` — main API server for the chatbot
- `frontend/src/App.jsx` — React UI for asking questions
- `app.py` — experimental/agricultural RAG script; not used by the React frontend
- `docs/` — source documents for retrieval
- `chroma_db/` — local Chroma vector store persistence

## What was fixed

- Backend now supports both PDF and CSV documents in `docs/`
- Root script `app.py` was updated to avoid hard-coded API keys
- Added a project-level `.gitignore`
- Added environment example files and a structured README
- Added `pandas` to `backend/requirements.txt`

## Requirements

- Python 3.10+ (recommended)
- Node.js 18+ and npm
- A valid `GROQ_API_KEY`

## Setup

### Backend

1. Create a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

3. Create a `.env` file in the repository root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

### Frontend

1. Install frontend dependencies:

```powershell
cd frontend
npm install
```

2. Create `frontend/.env`:

```text
VITE_API_URL=http://localhost:8000
```

## Running the app

### Start backend

From the repository root:

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start frontend

In a separate terminal:

```powershell
cd frontend
npm run dev
```

Then open the Vite dev URL shown in your terminal.

## Notes

- `backend/main.py` loads PDFs and CSVs from the `docs/` folder.
- If you want to use PDFs, place them inside `docs/`.
- The root `app.py` file is an alternate script and is not required for the current frontend chatbot.

## GitHub deployment

This repository has been prepared for Git usage with a `.gitignore` and documentation. If you want to push to GitHub, configure the remote and push from this project root.
