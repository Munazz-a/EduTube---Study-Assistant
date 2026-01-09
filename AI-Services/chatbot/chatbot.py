import ollama

def answer_question(question, context=""):
    prompt = f"""
You are an intelligent assistant.

Transcript context:
{context}

Instructions:
- Use the transcript if it helps.
- If not, use general knowledge.
- Keep answer related to the topic.

Question:
{question}
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]
