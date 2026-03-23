from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import glob

from rag import build_vector_store, retrieve_context
from chatbot import answer_question, summarize_transcript

app = FastAPI()
sessions = {}


CAPTION_DIR = "captions"
os.makedirs(CAPTION_DIR, exist_ok=True)


class TranscribeRequest(BaseModel):
    videoId: str
    sessionId: str

class ChatRequest(BaseModel):
    question: str
    sessionId: str

class SummarizeRequest(BaseModel):
    sessionId: str

def fetch_captions_with_ytdlp(video_id: str) -> str | None:
    url = f"https://www.youtube.com/watch?v={video_id}"

    cmd = [
        "yt-dlp",
        "--cookies", "cookies.txt",
        "--skip-download",
        "--write-auto-sub",
        "--write-sub",
        "--sub-lang", "en",
        "--sub-format", "vtt",
        "-o", f"{CAPTION_DIR}/{video_id}.%(ext)s",
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return None
    except subprocess.CalledProcessError:
        return None

    vtt_files = glob.glob(f"{CAPTION_DIR}/{video_id}*.vtt")
    if not vtt_files:
        return None

    transcript_lines = []
    with open(vtt_files[0], "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "-->" in line or line.isdigit():
                continue
            transcript_lines.append(line)

    return " ".join(transcript_lines)


@app.post("/transcribe")
def transcribe(req: TranscribeRequest):
    global index, chunks


    if req.sessionId in sessions:
        return {"status": "already_processed"}

    transcript = fetch_captions_with_ytdlp(req.videoId)
    if not transcript:
        return {"error": "❌ Captions unavailable (video restricted or CC disabled)"}

    index, chunks = build_vector_store(transcript)

    sessions[req.sessionId] = {
        "index": index,
        "chunks": chunks
    }
    return {
        "status": "ok",
        "preview": transcript[:3000]
    }


@app.post("/chat")
async def chat(req: ChatRequest):
    session = sessions.get(req.sessionId)
    print("Session:", req.sessionId)
    if not session:
        return {"answer": "Please transcribe a video first"}

    context = retrieve_context(
        req.question,
        session["index"],
        session["chunks"]
    )
    return {"answer": answer_question(req.question, context)}

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    session = sessions.get(req.sessionId)

    if not session:
        return {"summary": "Please transcribe a video first"}

    summary = summarize_transcript(session["chunks"])

    return {"summary": summary}