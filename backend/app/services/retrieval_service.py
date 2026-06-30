from sqlalchemy.orm import Session

from app.models.document import DocumentChunk
from app.services.embedding_service import generate_embedding


def retrieve_relevant_chunks(
    query: str,
    db: Session,
    limit: int = 3,
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(limit)
        .all()
    )

    return results


def build_context_from_chunks(
    chunks,
):
    return "\n\n".join(
        chunk.chunk_text
        for chunk in chunks
    )