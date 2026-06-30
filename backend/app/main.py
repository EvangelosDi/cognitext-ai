from app.database.database import Base
from app.database.database import engine

from app.models.document import Document
from app.models.document import DocumentChunk

from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.document import DocumentCreate
from app.schemas.document import DocumentResponse


from fastapi import UploadFile
from fastapi import File

import os

from app.services.pdf_service import extract_text_from_pdf

from app.services.text_splitter import split_text

from app.services.embedding_service import generate_embedding

from sqlalchemy import text

from app.services.rag_service import build_rag_prompt

from app.services.llm_service import generate_answer_from_context

app = FastAPI(
    title="Cognitext AI API",
    description="Backend API for the Cognitext AI Intelligent Document Intelligence Platform.",
    version="0.1.0",
)



with engine.connect() as connection:
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    connection.commit()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Welcome to Cognitext AI API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "cognitext-api",
    }


@app.post("/documents", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
):
    new_document = Document(
        filename=document.filename,
        filepath=document.filepath,
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": file.filename,
        "saved_to": file_path
    }


@app.get("/documents/extract")
def extract_document():

    pdf_path = (
        "uploads/"
        "Cognitext AI - Project State Summary (June 2026).pdf"
    )

    extracted_text = extract_text_from_pdf(
        pdf_path
    )

    return {
        "text": extracted_text[:3000]
    }

@app.get("/documents/chunks")
def chunk_document():

    pdf_path = (
        "uploads/"
        "Cognitext AI - Project State Summary (June 2026).pdf"
    )

    extracted_text = extract_text_from_pdf(
        pdf_path
    )

    chunks = split_text(
        extracted_text,
        chunk_size=800,
        overlap=100,
    )

    return {
        "number_of_chunks": len(chunks),
        "chunks": chunks[:3],
    }



@app.get("/documents/embeddings")
def create_embeddings():

    pdf_path = (
        "uploads/"
        "Cognitext AI - Project State Summary (June 2026).pdf"
    )

    extracted_text = extract_text_from_pdf(
        pdf_path
    )

    chunks = split_text(
        extracted_text,
        chunk_size=800,
        overlap=100,
    )

    embedding = generate_embedding(
        chunks[0]
    )

    return {
        "embedding_dimensions": len(
            embedding
        ),
        "first_10_values": embedding[:10]
    }

@app.post("/documents/process")
def process_document(
    db: Session = Depends(get_db),
):
    pdf_path = (
        "uploads/"
        "Cognitext AI - Project State Summary (June 2026).pdf"
    )

    extracted_text = extract_text_from_pdf(pdf_path)

    chunks = split_text(
        extracted_text,
        chunk_size=800,
        overlap=100,
    )

    saved_chunks = []

    for chunk in chunks:
        embedding = generate_embedding(chunk)

        document_chunk = DocumentChunk(
            document_id=None,
            chunk_text=chunk,
            embedding=embedding,
        )

        db.add(document_chunk)
        saved_chunks.append(document_chunk)

    db.commit()

    return {
        "message": "Document processed successfully",
        "chunks_saved": len(saved_chunks),
    }


@app.get("/documents/search")
def search_document(
    query: str,
    db: Session = Depends(get_db),
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
        .limit(5)
        .all()
    )

    return {
        "query": query,
        "results": [
            {
                "chunk_id": result.id,
                "chunk_text": result.chunk_text[:500],
            }
            for result in results
        ],
    }

@app.get("/documents/context")
def get_context(
    query: str,
    db: Session = Depends(get_db),
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(5)
        .all()
    )

    context = "\n\n".join(
        chunk.chunk_text
        for chunk in results
    )

    return {
        "query": query,
        "context": context
    }


@app.get("/documents/ask")
def ask_document(
    query: str,
    db: Session = Depends(get_db),
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(3)
        .all()
    )

    context = "\n\n".join(
        chunk.chunk_text
        for chunk in results
    )

    prompt = build_rag_prompt(
        question=query,
        context=context,
    )

    return {
        "query": query,
        "retrieved_chunks": len(results),
        "rag_prompt": prompt,
    }


@app.get("/documents/ask-preview")
def ask_document_preview(
    query: str,
    db: Session = Depends(get_db),
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(3)
        .all()
    )

    context = "\n\n".join(
        chunk.chunk_text
        for chunk in results
    )

    prompt = build_rag_prompt(
        question=query,
        context=context,
    )

    llm_response = generate_answer_from_context(
        prompt=prompt,
    )

    return {
        "query": query,
        "retrieved_chunks": len(results),
        "llm_response": llm_response,
    }