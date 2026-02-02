import ollama

def answer_question(question, context):
    print("===== CONTEXT SENT TO LLM =====")
    print(context[:500])
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
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": prompt}],
        stream = False
    )
    return response["message"]["content"]


# import ollama

# def answer_question(question, context):
#     prompt = f"""
# You are an intelligent assistant.

# Transcript context:
# {context}

# Instructions:
# - Use the transcript if it helps.
# - If not, use general knowledge.
# - Keep answer related to the topic.

# Question:
# {question}
# """

#     stream = ollama.chat(
#         model="qwen2.5:3b",
#         messages=[{"role": "user", "content": prompt}],
#         stream=False
#     )

#     full_response = ""

#     for chunk in stream:
#         if "message" in chunk:
#             full_response += chunk["message"]["content"]

#     return full_response
