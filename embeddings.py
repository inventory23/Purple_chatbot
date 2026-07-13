import os
import fitz
import pickle
import faiss
import numpy as np

from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from utils.cleaner import clean_text
from utils.chunker import split_into_chunks


# -----------------------------
# Configuration
# -----------------------------

PDF_FOLDER = "data"

DATABASE_FOLDER = "database"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

os.makedirs(DATABASE_FOLDER, exist_ok=True)


# -----------------------------
# Load Embedding Model
# -----------------------------

print("="*60)
print("Loading Embedding Model...")
print("="*60)

model = SentenceTransformer(EMBEDDING_MODEL)

print("Model Loaded Successfully")
print()


# -----------------------------
# Read PDF
# -----------------------------

def extract_chunks(pdf_path):

    document = fitz.open(pdf_path)

    all_chunks = []

    for page_no in range(len(document)):

        page = document.load_page(page_no)

        text = page.get_text()

        text = clean_text(text)

        if len(text) == 0:
            continue

        chunks = split_into_chunks(text)

        for chunk in chunks:

            all_chunks.append({

                "page": page_no + 1,

                "text": chunk

            })

    document.close()

    return all_chunks


# -----------------------------
# Read Every PDF
# -----------------------------

all_chunks = []

pdf_files = [

    file

    for file in os.listdir(PDF_FOLDER)

    if file.endswith(".pdf")

]

for pdf in pdf_files:

    print("Reading:", pdf)

    pdf_path = os.path.join(PDF_FOLDER, pdf)

    chunks = extract_chunks(pdf_path)

    all_chunks.extend(chunks)

print()

print("Total Chunks :", len(all_chunks))

print()


# -----------------------------
# Generate Embeddings
# -----------------------------

texts = [

    chunk["text"]

    for chunk in all_chunks

]

print("="*60)
print("Generating Embeddings...")
print("="*60)

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print()

print("Embedding Shape :", embeddings.shape)

print()


# -----------------------------
# Normalize
# -----------------------------

faiss.normalize_L2(embeddings)


# -----------------------------
# Create FAISS Index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print("FAISS Index Created")

print("Vectors :", index.ntotal)

print()


# -----------------------------
# Save Index
# -----------------------------

faiss.write_index(

    index,

    os.path.join(

        DATABASE_FOLDER,

        "faiss_index.bin"

    )

)

print("FAISS Saved")


# -----------------------------
# Save Metadata
# -----------------------------

with open(

    os.path.join(

        DATABASE_FOLDER,

        "chunks.pkl"

    ),

    "wb"

) as file:

    pickle.dump(

        all_chunks,

        file

    )

print("Chunk Metadata Saved")

print()

print("="*60)
print("DONE")
print("="*60)