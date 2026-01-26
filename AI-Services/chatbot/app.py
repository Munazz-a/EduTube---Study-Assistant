from fastapi import FastAPI
from pydantic import BaseModel
import os
from chatbot import answer_question

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

TRANSCRIPT_PATH = "AI-Services/transcribe/output/clean.txt"

@app.post("/chat")
def chat(req: ChatRequest):
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        transcript = f.read()

    answer = answer_question(req.question, transcript)
    return {"answer": answer}
