import pandas as pd
from sentence_transformers import SentenceTransformer
import os
from pinecone import Pinecone, ServerlessSpec
import numpy as np
from tqdm import tqdm

pc = Pinecone(api_key=os.environ('PINECONE_API_KEY'))

index_name = 'encoinfo'

index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

data = pd.read_csv('pages.csv')

def create_embeddings(text):
    return model.encode(text, show_progress_bar=True)

vectors_to_upsert = []
for url, content in tqdm(data.itertuples(index=False), total=len(data), desc="Preparando dados para o Pinecone"):
    embedding = create_embeddings(content)
    vector = {"id": url, "values": embedding.tolist()}
    vectors_to_upsert.append(vector)

batch_size = 100  #Tamanho do lote
for i in range(0, len(vectors_to_upsert), batch_size):
    batch = vectors_to_upsert[i:i + batch_size]
    index.upsert(vectors=batch, namespace="default")

print("Dados inseridos com sucesso no Pinecone.")