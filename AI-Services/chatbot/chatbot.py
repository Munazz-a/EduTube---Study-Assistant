import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # 👈 MUST be before Groq()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# Question Answering (RAG)
def answer_question(question, context):
    prompt = f"""
You are an intelligent assistant.

Transcript context:
{context}

Instructions:
- Use the transcript if it helps.
- If not, use general knowledge.
- Keep answer related to the topic.
- Ensure the answer is complete.
- Do not stop mid-sentence.
- If listing points, finish all points.


Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
        stop=None
    )

    return response.choices[0].message.content

# Hierarchical Summarization
# ---------------------------
def summarize_transcript(chunks):
    """
    Map-reduce summarization:
    1. Summarize each chunk
    2. Combine and generate final summary
    """

    chunk_summaries = []

    # Step 1: Summarize each chunk
    for chunk in chunks:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"Provide a concise academic summary of the following content:\n\n{chunk}"
                }
            ],
            temperature=0.3,
            max_tokens=300
        )

        chunk_summaries.append(response.choices[0].message.content)

    # Step 2: Combine summaries
    combined_text = "\n".join(chunk_summaries)

    final_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Generate a clear and structured final summary of the following combined summaries:\n\n{combined_text}"
            }
        ],
        temperature=0.3,
        max_tokens=800
    )

    return final_response.choices[0].message.content