import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # 👈 MUST be before Groq()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

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
