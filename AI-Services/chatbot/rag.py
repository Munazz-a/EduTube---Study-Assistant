from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, size=500, overlap=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[i:i + size]))

    return chunks

def build_vector_store(text):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, chunks

def retrieve_context(question, index, chunks, k=3):
    q_emb = model.encode([question])
    _, ids = index.search(q_emb, k)
    return "\n\n".join(chunks[i] for i in ids[0])
