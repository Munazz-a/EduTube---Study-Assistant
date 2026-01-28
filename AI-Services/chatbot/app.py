from fastapi import FastAPI
from pydantic import BaseModel
import os

from chatbot import answer_question
from rag import build_vector_store, retrieve_context

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

# ---------- PATH FIX (robust) ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TRANSCRIPT_PATH = os.path.join(
    BASE_DIR,
    "Ai-Services",
    "transcribe",
    "output",
    "clean.txt"
)

# ---------- GLOBAL CACHE ----------
index = None
chunks = None
transcript_loaded = False


def load_transcript_once():
    global index, chunks, transcript_loaded

    if transcript_loaded:
        return

    if not os.path.exists(TRANSCRIPT_PATH):
        raise FileNotFoundError("Transcript not found")

    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        transcript = f.read()

    index, chunks = build_vector_store(transcript)
    transcript_loaded = True
    print("✅ Transcript loaded & indexed")


@app.post("/chat")
def chat(req: ChatRequest):
    global index, chunks

    try:
        load_transcript_once()
    except FileNotFoundError:
        return {
            "answer": "Transcript not found. Please summarize the video first."
        }

    context = retrieve_context(req.question, index, chunks)
    answer = answer_question(req.question, context)
    return {"answer": answer}
