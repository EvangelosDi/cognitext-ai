# Cognitext AI

**Current Version**

v0.4.0

---

# Current Milestone

Local Retrieval-Augmented Generation (RAG) platform with dynamic document ingestion, semantic search, document-aware retrieval and local Large Language Model (LLM) integration using Ollama.

---

# Project Goal

Cognitext AI is a modular Document Intelligence Platform designed to allow users to upload documents, automatically process them, generate vector embeddings and interact with them through semantic search and Retrieval-Augmented Generation (RAG).

The long-term vision is to evolve Cognitext into a production-ready AI platform capable of supporting multiple domains such as:

- Humanitarian Operations
- Monitoring & Evaluation
- Research
- Finance
- Legal
- Corporate Knowledge Management

---

# Current Architecture

User

↓

FastAPI Backend

↓

Document Services

↓

Embedding Service

↓

PostgreSQL + pgvector

↓

Semantic Retrieval

↓

LLM Service (Ollama)

↓

Answer

---

# Repository Structure

backend/

app/

database/

models/

schemas/

services/

main.py

frontend/

docs/

docker-compose.yml

README.md

---

# Tech Stack

Backend

- FastAPI

Database

- PostgreSQL
- pgvector

ORM

- SQLAlchemy

AI

- Sentence Transformers
- Ollama
- Llama 3.2

Containerization

- Docker
- Docker Compose

Version Control

- Git
- GitHub

---

# Implemented Features

✅ Document Upload

✅ PDF Text Extraction

✅ Intelligent Chunking

✅ Embedding Generation

✅ pgvector Storage

✅ Semantic Search

✅ Context Builder

✅ Prompt Builder

✅ Local LLM Integration

✅ Retrieval-Augmented Generation

✅ Document-aware Semantic Search

✅ Document Management API

---



# Current API Endpoints

POST /documents

POST /documents/upload

GET /documents

GET /documents/{document_id}

DELETE /documents/{document_id}

GET /documents/search

GET /documents/context

GET /documents/ask

GET /documents/ask-preview

GET /documents/chunks

GET /documents/extract

GET /documents/embeddings

---

# Database Schema

documents

- id
- filename
- filepath

document_chunks

- id
- document_id
- chunk_text
- embedding (384-dimensional vector)

---

# Implemented Services

pdf_service.py

Extracts text from uploaded PDF files.

text_splitter.py

Splits extracted text into overlapping chunks.

embedding_service.py

Generates vector embeddings using Sentence Transformers.

retrieval_service.py

Performs semantic similarity search and builds context.

rag_service.py

Builds prompts for Retrieval-Augmented Generation.

llm_service.py

Communicates with the local Ollama LLM.

---

# Current Workflow

User uploads PDF

↓

Document stored

↓

Text extracted

↓

Chunks created

↓

Embeddings generated

↓

Stored in PostgreSQL + pgvector

↓

Semantic retrieval

↓

Context generation

↓

Prompt construction

↓

Ollama generates answer

↓

Answer returned with supporting source chunks

---

# Known Limitations

Current system searches one selected document at a time.

No frontend yet.

No authentication.

No cloud deployment.

No conversation memory.

No document collections.

---

# Next Milestone

Implement document collections and improved document management.

Build frontend (Streamlit).

Improve metadata management.

---

# Long-term Vision

Transform Cognitext AI into a production-ready Document Intelligence Platform supporting:

- Multiple users
- Authentication
- Cloud deployment
- AWS infrastructure
- PySpark pipelines
- Enterprise knowledge bases
- Domain-specific AI assistants
- Production monitoring