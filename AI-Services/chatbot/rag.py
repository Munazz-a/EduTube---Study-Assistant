from embeddings import create_index
import numpy as np

def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

# rag.py (continued)
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_store(transcript):
    chunks = chunk_text(transcript)
    index, embeddings = create_index(chunks)
    return index, chunks

# rag.py (continued)
def retrieve_context(question, index, chunks, k=3):
    q_embedding = model.encode([question])
    distances, indices = index.search(q_embedding, k)

    retrieved = [chunks[i] for i in indices[0]]
    return "\n\n".join(retrieved)
