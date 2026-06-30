import ollama


client = ollama.Client(
    host="http://host.docker.internal:11434"
)


def generate_answer_from_context(
    prompt: str,
):
    response = client.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return {
        "answer": response["message"]["content"]
    }