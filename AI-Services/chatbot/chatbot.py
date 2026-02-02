import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # 👈 MUST be before Groq()

api_key = os.getenv("GROQ_API_KEY")
print("Loaded key:", api_key)  # TEMP DEBUG

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


Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content
