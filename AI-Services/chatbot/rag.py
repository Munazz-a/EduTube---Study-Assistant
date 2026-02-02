from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from functools import lru_cache

# ✅ Embedding model (DO NOT change this to Ollama model)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text, size=250, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[i:i + size]))

    return chunks


def build_vector_store(text):
    chunks = chunk_text(text)

    # ⚠️ This runs ONCE per video (expensive but acceptable)
    embeddings = embed_model.encode(chunks, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, chunks


# ✅ CACHE question embeddings (THIS is what I told you to add)
@lru_cache(maxsize=128)
def embed_question(question: str):
    return embed_model.encode([question])


def retrieve_context(question, index, chunks, k=2):
    q_emb = embed_question(question)
    _, ids = index.search(q_emb, k)
    return "\n\n".join(chunks[i] for i in ids[0])
