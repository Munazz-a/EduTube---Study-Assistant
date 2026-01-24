from fastapi import FastAPI
from pydantic import BaseModel
import traceback
import os
from chatbot import answer_question

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file_path = os.path.join(
    BASE_DIR,
    "AI-Services",
    "transcribe",
    "output",
    "clean.txt"
)
with open(file_path, "r", encoding="utf-8") as f:
    TRANSCRIPT = f.read()

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        print("Your question:", req.question)

        # TEMP TEST RESPONSE
        return {"answer": answer_question(req.question)}

    except Exception as e:
        print("ERROR:")
        traceback.print_exc()
        return {"error": str(e)}
