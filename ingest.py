import fitz
import os

from utils.cleaner import clean_text
from utils.chunker import split_into_chunks

PDF_FOLDER = "data"


def process_pdf(pdf_path):

    document = fitz.open(pdf_path)

    all_chunks = []

    for page_no in range(len(document)):

        page = document.load_page(page_no)

        text = page.get_text("text")

        text = clean_text(text)

        if not text:
            continue

        chunks = split_into_chunks(text)

        for chunk in chunks:

            all_chunks.append({

                "page": page_no + 1,

                "text": chunk

            })

    document.close()

    return all_chunks


def main():

    pdfs = [
        file
        for file in os.listdir(PDF_FOLDER)
        if file.endswith(".pdf")
    ]

    if len(pdfs) == 0:

        print("No PDF found.")

        return

    for pdf in pdfs:

        print("=" * 60)

        print(pdf)

        print("=" * 60)

        chunks = process_pdf(os.path.join(PDF_FOLDER, pdf))

        print()

        print("Total Chunks :", len(chunks))

        print()

        for i in range(min(5, len(chunks))):

            print("-" * 60)

            print("Chunk :", i + 1)

            print("Page :", chunks[i]["page"])

            print()

            print(chunks[i]["text"])

            print()

        print("=" * 60)


if __name__ == "__main__":
    main()