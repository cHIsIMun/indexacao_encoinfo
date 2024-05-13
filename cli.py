from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from flask import Flask, request, render_template
import requests
import html
import numpy as np
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

pc = Pinecone(api_key=os.environ('PINECONE_API_KEY'))
index_name = 'encoinfo'
index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

# Search CLI:
# while True:
#     query = input("Digite sua consulta: ")
#     if query.lower() == "exit":
#         break

#     # Gera o embedding para a consulta
#     embedding = model.encode(query)
#     # Converte o embedding em uma lista de floats
#     embedding_list = embedding.tolist()

#     # Realiza a consulta no Pinecone
#     try:
#         # Adapte os parâmetros conforme sua configuração de namespaces
#         results = index.query(
#             namespace="default",  # ou "ns1", "ns2" dependendo de sua configuração
#             vector=embedding_list,
#             top_k=5,
#             include_values=False  # ajuste para True se precisar dos valores dos vetores nas respostas
#         )
        
#         if results.get('matches'):  # Verifica se há resultados
#             for match in results['matches']:
#                 print(f"ID: {match['id']}, Score: {match['score']}")
#         else:
#             print("Nenhum resultado encontrado.")
#     except Exception as e:
#         print("Erro ao realizar consulta:", e)

def fetch_title(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            match = re.search('<title>(.*?)</title>', response.text, re.IGNORECASE)
            if match:
                return html.unescape(match.group(1).strip())
            return "Título não encontrado"
    except requests.RequestException:
        return "Erro ao acessar o site"

@app.route("/", methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            embedding = model.encode(query)
            embedding_list = embedding.tolist()
            results = index.query(namespace="default", vector=embedding_list, top_k=20)
            matches = results.get('matches', [])
            
            with ThreadPoolExecutor(max_workers=30) as executor:
                future_to_url = {executor.submit(fetch_title, match['id']): match for match in matches}
                for future in as_completed(future_to_url):
                    match = future_to_url[future]
                    try:
                        title = future.result()
                    except Exception as exc:
                        title = "Erro ao acessar o site"
                    match['title'] = title

            return render_template('index.html', matches=matches, query=query)
        else:
            return render_template('index.html', matches=[], query="")
    else:
        return render_template('index.html', matches=[], query="")

if __name__ == "__main__":
    app.run(debug=True)
