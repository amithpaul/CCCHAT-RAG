from sentence_transformers import SentenceTransformer
import faiss
import os
import json

model = SentenceTransformer("Qwen/Qwen3-Embedding-8B")

json_files = os.listdir("./data/chunks")
data = []
for file in json_files:
    with open(f"./data/chunks/{file}","r") as f:
        data.append(json.load(f))
# print(data)
embeddings = model.encode([doc["chunk_text"] for doc in data])
        