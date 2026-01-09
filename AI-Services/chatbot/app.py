from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import answer_question

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    return {"answer": answer_question(query.question)}
