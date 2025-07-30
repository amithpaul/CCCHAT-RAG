import pymupdf
import os
from preprocessing.processTools import split_by_structure, chunker
import json

def process_textbooks(book,skip_arr):   
    doc = pymupdf.open(f"./data/raw/textbooks/{book}")
    pages = [(page.get_text(),page.number) for page in doc]

    splits = split_by_structure(pages)
    chunks = chunker(splits,chunk_size=450,chunk_overlap=100)
    
    with open(f"./data/chunks/{book.strip('.pdf')}_chunks.json", "w") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

def main():
    textbooks = os.listdir('./data/raw/textbooks')
    print(textbooks)
    
