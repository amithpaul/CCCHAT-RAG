import pymupdf
import os
from preprocessing.processTools import split_by_structure
import json

def process_textbooks(book,skip_list = []):   
    doc = pymupdf.open(f"./data/raw/textbooks/{book}")
    pages = [(page.get_text(),page.number) for page in doc if page not in skip_list]
    chunks = split_by_structure(pages)
    with open(f"./data/chunks/textbook_chunks/{book.strip('.pdf')}_chunks.json", "w") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

# def main():
#     textbooks = os.listdir('./data/raw/textbooks')
#     print(textbooks)
#     for book in textbooks:
#         process_textbooks(book)
        
# if __name__ == "__main__":
#     main()