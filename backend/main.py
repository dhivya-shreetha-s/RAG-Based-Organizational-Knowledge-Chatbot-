from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

app = FastAPI(
    title="PDF RAG Chatbot API",
    description="FastAPI backend for a PDF retrieval-augmented generation chatbot.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chain: ConversationalRetrievalChain | None = None


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


def build_rag_chain() -> ConversationalRetrievalChain:
    docs_path = BASE_DIR / "docs"
    db_path = BASE_DIR / "chroma_db"

    if not docs_path.exists():
        raise FileNotFoundError(f"Document folder not found: {docs_path}")

    raw_docs = []

    pdf_loader = DirectoryLoader(
        str(docs_path),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    pdf_docs = pdf_loader.load()
    raw_docs.extend(pdf_docs)
    print(f"Loaded {len(pdf_docs)} PDF documents from {docs_path}")

    csv_paths = list(docs_path.glob("**/*.csv"))
    for csv_path in csv_paths:
        csv_loader = CSVLoader(str(csv_path), encoding="utf-8")
        csv_docs = csv_loader.load()
        raw_docs.extend(csv_docs)
        print(f"Loaded {len(csv_docs)} CSV documents from {csv_path.name}")

    if not raw_docs:
        raise FileNotFoundError(
            f"No supported documents found in {docs_path}. Add PDFs or CSVs to the docs folder."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = splitter.split_documents(raw_docs)
    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db_path.mkdir(parents=True, exist_ok=True)
    vectordb = Chroma(
        persist_directory=str(db_path),
        embedding_function=embeddings,
    )

    if not any(db_path.iterdir()):
        batch_size = 500
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vectordb.add_documents(batch)
            print(f"Added batch {i // batch_size + 1}")
        vectordb.persist()
        print("ChromaDB created successfully")
    else:
        print("Existing ChromaDB found, skipping re-ingestion")

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20,
        },
    )

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
    )


@app.on_event("startup")
def startup_event() -> None:
    global chain
    chain = build_rag_chain()
    print("RAG pipeline initialized and ready")


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Question text cannot be empty.")

    if chain is None:
        raise HTTPException(status_code=500, detail="The RAG pipeline is not available.")

    try:
        result = chain({"question": request.question})
        answer = result.get("answer") or result.get("output_text") or ""
        return ChatResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
