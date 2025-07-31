from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import torch
import os
import json

model = SentenceTransformer("Qwen/Qwen3-Embedding-8B",device="mps")

chroma_client = chromadb.Client(
                    Settings(
                        chroma_db_impl="duckdb+parquet", 
                        persist_directory="./backend/vector_stores/textbook_stores/chroma_store"
                    )
                )
collection = chroma_client.get_or_create_collection("textbook_chunks")

json_files = os.listdir("./data/chunks")

def embed_textbooks(json_files):
    data = []
    for file in json_files:
        with open(f"./data/chunks/textbook_chunks/{file}","r") as f:
            data.append(json.load(f))
            
    for chunk in data:
        text = chunk[text]
        metadata = {
            "chapter": chunk.get("chapter"),
            "section": chunk.get("section"),
            "page": chunk.get("page"),
            "chunk_index": chunk.get("chunk_index")
        }
        uid = f'{metadata["chapter"]}:{metadata["section"]}:{metadata["page"]}:{metadata["chunk_index"]}'
        embedding = model.encode(text)

        collection.add(
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding],
            ids = [uid]
        )
    chroma_client.persist()
        