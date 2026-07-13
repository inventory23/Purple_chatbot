import faiss
import pickle

from sentence_transformers import SentenceTransformer
from ollama import chat


# -----------------------------
# Configuration
# -----------------------------

MODEL_NAME = "BAAI/bge-small-en-v1.5"

OLLAMA_MODEL = "qwen2.5:7b"

TOP_K = 3


# -----------------------------
# Load Everything
# -----------------------------

print("Loading embedding model...")
embed_model = SentenceTransformer(MODEL_NAME)

print("Loading FAISS...")
index = faiss.read_index("database/faiss_index.bin")

print("Loading Chunks...")

with open("database/chunks.pkl","rb") as f:
    chunks = pickle.load(f)

print("Ready!")
print()


# -----------------------------
# Retrieve
# -----------------------------

def retrieve(query):

    query = "Represent this sentence for searching relevant passages: " + query

    vector = embed_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, ids = index.search(vector, TOP_K)

    context = ""

    for idx in ids[0]:

        context += chunks[idx]["text"]

        context += "\n\n"

    return context


# -----------------------------
# Ask LLM
# -----------------------------

def ask_llm(question):

    context = retrieve(question)

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not present,
reply:

"I couldn't find the answer in the provided documents."

Context:

{context}

Question:

{question}

Answer:
"""

    response = chat(

        model=OLLAMA_MODEL,

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )

    return response["message"]["content"]


# -----------------------------
# Chat Loop
# -----------------------------

while True:

    q = input("\nYou : ")

    if q.lower()=="exit":
        break

    answer = ask_llm(q)

    print()

    print("AI :")

    print(answer)# chat.py
