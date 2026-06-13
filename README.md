# Cognitext AI

**Cognitext AI** is an Intelligent Document Intelligence Platform that allows users to upload documents, index their content, and interact with them through a Retrieval-Augmented Generation (RAG) chatbot.

The platform is designed to work across domains such as finance, humanitarian operations, research, policy analysis, business intelligence, and technical documentation.

## Core Features

- Upload PDF documents
- Extract and process text
- Split documents into semantic chunks
- Generate embeddings using local embedding models
- Store vectors in PostgreSQL with pgvector
- Perform semantic search over uploaded documents
- Ask questions through a chatbot interface
- Generate grounded answers using retrieved context
- Display uploaded documents and query history in a dashboard

## Tech Stack

### Backend
- FastAPI
- Python
- SQLAlchemy
- PostgreSQL
- pgvector

### AI / NLP
- Sentence Transformers
- Ollama
- Local LLMs such as Llama, Mistral, or Qwen
- Retrieval-Augmented Generation

### Frontend
- Streamlit

### Infrastructure
- Docker
- Docker Compose

### Future Cloud Deployment
- AWS EC2
- AWS S3
- GitHub Actions CI/CD

## Architecture Overview

```text
User
 ↓
Streamlit Dashboard
 ↓
FastAPI Backend
 ↓
PostgreSQL + pgvector
 ↓
Embedding Model / Ollama LLM