import pickle
import faiss
from sentence_transformers import SentenceTransformer
from ollama import chat

# =====================================================
# Configuration
# =====================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
  

OLLAMA_MODEL = "qwen2.5:7b "

    # Change to qwen2.5:7b if installed

TOP_K = 3

# =====================================================
# Load Everything (Only Once)
# =====================================================

print("=" * 60)
print("Loading AI Engine...")
print("=" * 60)

print("Loading Embedding Model...")
embed_model = SentenceTransformer(EMBEDDING_MODEL)

print("Loading FAISS Index...")
index = faiss.read_index("database/faiss_index.bin")

print("Loading Chunk Metadata...")

with open("database/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded {len(chunks)} chunks.")

print("AI Engine Ready!")
print("=" * 60)


# =====================================================
# Retrieve Relevant Chunks
# =====================================================

def retrieve_context(question):

    query = (
        "Represent this sentence for searching relevant passages: "
        + question
    )

    query_vector = embed_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(query_vector, TOP_K)

    context = ""

    sources = []

    for score, idx in zip(scores[0], indices[0]):

        chunk = chunks[idx]

        context += chunk["text"]
        context += "\n\n"

        sources.append({
            "page": chunk["page"],
            "score": float(score)
        })

    return context, sources


# =====================================================
# Ask Local LLM
# =====================================================

def ask_llm(question):

    context, sources = retrieve_context(question)

    prompt = f"""
You are an intelligent AI assistant.

Answer ONLY using the information provided in the context.

If the answer is not available in the context, reply exactly:

I couldn't find the answer in the provided PDF documents.

Do not make up facts.

----------------------------

Context:

{context}

----------------------------

Question:

{question}

Answer:
"""

    response = chat(

        model=OLLAMA_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    answer = response["message"]["content"]

    # Add source pages
    '''pages = sorted(set([s["page"] for s in sources]))

    answer += "\n\n"

    answer += "Source Pages : "

    answer += ", ".join(str(p) for p in pages)'''

    return answer