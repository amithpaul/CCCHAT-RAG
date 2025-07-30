import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from nltk.tokenize import sent_tokenize


def clean_title(title):
    # Remove dot leaders followed by page numbers
    title = re.sub(r'\.{3,}\s*\d+[\d–\-]*$', '', title)

    # Remove standalone trailing page numbers or numeric tokens
    title = re.sub(r'\s*\d+[\d–\-]*$', '', title)

    # Remove any trailing parentheses and their contents
    title = re.sub(r'\s*\(.*?\)\s*$', '', title)

    # Remove common junk patterns (e.g., Roman numerals + dots)
    title = re.sub(r'^[IVXLC]+\.', '', title)

    # Normalize all kinds of whitespace (including tabs/newlines)
    title = re.sub(r'\s+', ' ', title)

    # Strip leading/trailing punctuation and whitespace
    title = title.strip(" .:\n\t-")

    return title

def clean_text(title):
    # Remove trailing periods and page numbers at the end
    # e.g., "Intro. 45" -> "Intro"

    # Remove trailing page number
    title = re.sub(r'\s*\d+\s*$', '', title)   

    # Remove trailing periods
    title = re.sub(r'[.]+$', '', title.strip())  
         
    return title.strip()

def split_by_structure(pages):
    pass


def chunker(chunks,chunk_size=500,chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=[".",'\n','\n\n']
    )

    final_chunks = []

    for item in chunks:
        small_chunks = splitter.split_text(item['content'])


        for idx, chunk in enumerate(small_chunks):
            final_chunks.append({
                "chapter": clean_title(item["chapter"]),
                "section": clean_title(item["section"]),
                "chunk_id": f"{item['section']}-{idx}",
                "chunk_text": clean_text(chunk)
            })

    return final_chunks


    



    