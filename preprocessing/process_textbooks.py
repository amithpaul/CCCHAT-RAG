import pymupdf
import os

textbooks = os.listdir('./data/raw/textbooks')

for book in textbooks:
    
    doc = pymupdf.open(f"./data/raw/textbooks/{book}")
    raw_text = "".join([page.get_text() for page in book])
