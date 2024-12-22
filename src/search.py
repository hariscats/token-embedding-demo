import os
import pickle
import numpy as np
import torch

from embeddings import get_sentence_embedding

CORPUS_FILE = os.path.join(os.path.dirname(__file__), "data", "corpus.txt")
EMBEDDINGS_FILE = os.path.join(os.path.dirname(__file__), "data", "corpus_embeddings.pkl")

def build_corpus_embeddings():
    """
    Reads lines from corpus.txt, computes embeddings, and saves them for later use.
    """
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Compute embeddings for each line
    embeddings = []
    for line in lines:
        vec = get_sentence_embedding(line)
        embeddings.append(vec)

    # Save corpus lines and embeddings to a pickle file
    with open(EMBEDDINGS_FILE, "wb") as f:
        data = {
            "lines": lines,
            "embeddings": embeddings
        }
        pickle.dump(data, f)

def load_corpus_embeddings():
    """
    Loads the precomputed embeddings and lines from pickle.
    """
    if not os.path.exists(EMBEDDINGS_FILE):
        build_corpus_embeddings()

    with open(EMBEDDINGS_FILE, "rb") as f:
        data = pickle.load(f)
    return data["lines"], data["embeddings"]

def get_top_k_similar(query_embedding, k=3):
    """
    Returns the top-k most similar lines from the corpus
    by cosine similarity.
    """
    lines, embeddings = load_corpus_embeddings()

    # Convert to numpy if needed
    if isinstance(query_embedding, torch.Tensor):
        query_embedding = query_embedding.numpy()

    # Compute cosine similarity
    scores = []
    for idx, emb in enumerate(embeddings):
        # Dot product + normalization is the typical cosine similarity approach
        sim = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
        scores.append((idx, sim))

    # Sort by similarity descending
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-k
    top_k = scores[:k]
    results = []
    for idx, score in top_k:
        results.append({"text": lines[idx], "score": float(score)})

    return results

if __name__ == "__main__":
    print("Building corpus embeddings...")
    build_corpus_embeddings()
    print("Done. Embeddings saved to:", EMBEDDINGS_FILE)
