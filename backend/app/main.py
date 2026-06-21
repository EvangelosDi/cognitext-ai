from app.database.database import Base
from app.database.database import engine

from app.models.document import Document

from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.document import DocumentCreate
from app.schemas.document import DocumentResponse

from app.models.document import Document
from fastapi import UploadFile
from fastapi import File

import os

app = FastAPI(
    title="Cognitext AI API",
    description="Backend API for the Cognitext AI Intelligent Document Intelligence Platform.",
    version="0.1.0",
)

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