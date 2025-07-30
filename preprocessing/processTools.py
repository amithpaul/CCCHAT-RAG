import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from nltk.tokenize import sent_tokenize

splitter = RecursiveCharacterTextSplitter(
       chunk_size = 1000,
       chunk_overlap = 100,
       separators=[".","\n","\n\n"]
    )

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

def clean_text(text):
    # Remove trailing periods and page numbers at the end
    # e.g., "Intro. 45" -> "Intro"

    # Remove trailing page number
    text = re.sub(r'\s*\d+\s*$', '', text)   

    # Remove trailing periods
    text = re.sub(r'[.]+$', '', text.strip())  
    
    #Remove figure numbers
    text = re.sub(r'Figure\s*\d+\.\d+', '', text)

    return text.strip()

def split_text(text,meta):
    '''Used to split and fit text data into hash maps'''
    subchunks = []
    splits = splitter.split_text(text)
    for i, sub in enumerate(splits):
        subchunks.append({
            **meta,
            "text": clean_text(sub),
            "chunk_index": i
        })
    return subchunks

def split_by_structure(pages):
    chunks = []
    current_chapter = None
    current_section = None
    current_text = ""


    chapter_pattern = re.compile(r"\bchapter\s+\d+.*", re.IGNORECASE)
    section_pattern = re.compile(r"\b\d+\.\d+.*")

    for page in pages:
        lines = page[0].splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            meta = {
                "chapter": current_chapter or "UNKNOWN",
                "section": current_section,
                "page" : page[1]
                }
            # Assigns chapter name
            if chapter_pattern.match(line):
                current_chapter = line

            # Assigns section name
            elif section_pattern.match(line):
                if current_section and current_text.strip():
                    chunk_text = split_text(page[0],meta)
                    chunks.extend(chunk_text)

                current_section = line
                current_text = ""

            elif current_section:
                current_text += line + "\n"

    return chunks


     


# def chunker(chunks,chunk_size=500,chunk_overlap=100):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size, 
#         chunk_overlap=chunk_overlap,
#         separators=[".",'\n','\n\n']
#     )

#     final_chunks = []

#     for item in chunks:
#         small_chunks = splitter.split_text(item['content'])


#         for idx, chunk in enumerate(small_chunks):
#             final_chunks.append({
#                 "chapter": clean_title(item["chapter"]),
#                 "section": clean_title(item["section"]),
#                 "chunk_id": f"{item['section']}-{idx}",
#                 "chunk_text": clean_text(chunk)
#             })

#     return final_chunks


    



    