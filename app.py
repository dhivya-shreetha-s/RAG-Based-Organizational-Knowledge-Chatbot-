from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

import pandas as pd
from pathlib import Path
import os

load_dotenv()

AGRI_PROMPT = """
You are an AI Agricultural Advisor.

Your job is to recommend crops using:
1. Retrieved agricultural dataset information (highest priority)
2. Agricultural expertise and domain knowledge

Rules:
- Prioritize crops found in the retrieved dataset.
- Consider climate, soil type, water source, budget, and land size.
- Validate dataset recommendations using agricultural knowledge.
- Do not recommend duplicate crops.
- Rank crops by suitability and profitability.
- Clearly specify whether recommendations are based on:
  - Dataset
  - Knowledge
  - Both

For each crop provide:
- Crop Name
- Suitability Score (1-10)
- Source (Dataset/Knowledge/Both)
- Reason
- Water Requirement
- Profitability
- Risk Level

Finally provide:
- Ranked Top 10 Crops
- Best Overall Recommendation

Keep recommendations practical and concise.
"""
# ============================================
# SET YOUR GROQ API KEY
# ============================================

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

# ============================================
# LOAD PDF + EXCEL FILES
# ============================================

raw_docs = []

docs_folder = Path("./docs")

# --------------------------
# LOAD PDF FILES
# --------------------------

try:
    pdf_loader = DirectoryLoader(
        str(docs_folder),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    pdf_docs = pdf_loader.load()

    raw_docs.extend(pdf_docs)

    print(f"Loaded {len(pdf_docs)} PDF pages")

except Exception as e:
    print(f"PDF loading error: {e}")

# --------------------------
# LOAD EXCEL FILES
# --------------------------

excel_files = list(docs_folder.glob("*.xls")) + list(docs_folder.glob("*.xlsx"))

for excel_file in excel_files:

    try:
        print(f"Reading Excel: {excel_file.name}")

        df = pd.read_excel(excel_file)

        # Convert each row into a separate document
        for _, row in df.iterrows():

            row_text = "\n".join(
                [f"{col}: {row[col]}" for col in df.columns]
            )

            raw_docs.append(
                Document(
                    page_content=row_text,
                    metadata={
                        "source": str(excel_file)
                    }
                )
            )

        print(f"Loaded Excel: {excel_file.name}")

    except Exception as e:
        print(f"Error loading {excel_file.name}: {e}")

print(f"\nTotal Documents Loaded: {len(raw_docs)}")

# ============================================
# SPLIT INTO CHUNKS
# ============================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = splitter.split_documents(raw_docs)

print(f"Created {len(chunks)} chunks")

# ============================================
# EMBEDDINGS
# ============================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ============================================
# CHROMADB
# ============================================

vectordb = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

batch_size = 500

for i in range(0, len(chunks), batch_size):

    batch = chunks[i:i + batch_size]

    vectordb.add_documents(batch)

    print(f"Added batch {i // batch_size + 1}")

try:
    vectordb.persist()
except:
    pass

print("ChromaDB created successfully")

# ============================================
# RETRIEVER
# ============================================

retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20
    }
)

# ============================================
# GROQ MODEL
# ============================================

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# ============================================
# MEMORY
# ============================================

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ============================================
# RAG CHAIN
# ============================================

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

print("\nRAG Bot Ready!")
print("Type 'exit' to stop\n")

# ============================================
# CHAT LOOP
# ============================================

while True:

    query = input("You: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    try:
       final_query = AGRI_PROMPT + "\n\nFarmer Query:\n" + query

       result = chain({"question": final_query})

       print("\nAI:", result["answer"])
       print()

    except Exception as e:
       print(f"\nError: {e}")