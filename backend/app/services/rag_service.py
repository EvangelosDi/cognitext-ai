def build_rag_prompt(
    question: str,
    context: str,
):
    return f"""
You are Cognitext AI, a document intelligence assistant.

Answer the user's question using ONLY the context below.
If the answer is not in the context, say that the document does not contain enough information.

Context:
{context}

Question:
{question}

Answer:
"""