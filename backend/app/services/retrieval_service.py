from sqlalchemy.orm import Session

from app.models.document import DocumentChunk
from app.services.embedding_service import generate_embedding


def retrieve_relevant_chunks(
    query: str,
    db: Session,
    limit: int = 3,
    document_id: int | None = None,
):
    query_embedding = generate_embedding(query)

    query_builder = db.query(DocumentChunk)

    if document_id is not None:
        query_builder = query_builder.filter(
            DocumentChunk.document_id == document_id
        )

    results = (
        query_builder
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