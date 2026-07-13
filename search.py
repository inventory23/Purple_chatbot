import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------
# Configuration
# -----------------------

MODEL_NAME = "BAAI/bge-small-en-v1.5"

INDEX_PATH = "database/faiss_index.bin"
CHUNKS_PATH = "database/chunks.pkl"

TOP_K = 5

# -----------------------
# Load Model
# -----------------------

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# -----------------------
# Load FAISS
# -----------------------

print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

# -----------------------
# Load Chunks
# -----------------------

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded {len(chunks)} chunks.")
print()


def search(query, top_k=TOP_K):
    # Create query embedding
    query = "Represent this sentence for searching relevant passages: " + query

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Normalize (same as indexing)
    faiss.normalize_L2(query_embedding)

    # Search
    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "score": float(score),
            "page": chunks[idx]["page"],
            "text": chunks[idx]["text"]
        })

    return results


# -----------------------
# Interactive Search
# -----------------------

while True:

    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    results = search(question)

    print("\nTop Results")
    print("=" * 80)

    for i, result in enumerate(results, 1):

        print(f"\nResult {i}")
        print("-" * 80)
        print(f"Similarity : {result['score']:.4f}")
        print(f"Page       : {result['page']}")
        print()
        print(result["text"])