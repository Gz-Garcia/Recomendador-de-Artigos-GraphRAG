from serpapi import GoogleSearch
import streamlit as st

SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]

# busca por artigos
def search_papers(query: str, k: int):
  params = {
        "engine": "google_scholar",
        "q": query,  # tópico a ser pesquisado
        "num": k,  # número de resultados
        "api_key": SERPAPI_API_KEY
    }

  search = GoogleSearch(params)
  results = search.get_dict()

  artigos = results.get("organic_results", [])
  #print(f"\nForam encontrados {len(artigos)} artigos.")

  return artigos

def format_papers(papers : dict):
  
  # formatar os papers (títulos, snippet, link)
  format_papers = []

  for i, article in enumerate(papers):
      title = article.get('title', "Título não encontrado")
      link = article.get('link', "Link não encontrado")
      authors = [author['name'] for author in article.get('publication_info', {}).get('authors', [])]
      snippet = article.get('snippet', "Trecho não encontrado")

      new_paper = f"Informações sobre o artigo {i+1}:\n\tTítulo: {title}\n\tAutores: {authors}\n\tTrecho do artigo: {snippet}\n\tLink do artigo: {link}\n"
      format_papers.append(new_paper)
  
  return format_papers
