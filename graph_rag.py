from typing_extensions import TypedDict
from typing import List

from tools.get_infos import infos_chain
from tools.search import search_papers, format_papers

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]

# criação do estado do grafo
class State(TypedDict):
    user_input: str
    papers: List[str]
    answer: str
    selected_model: str

def get_papers(state: State):
    user_input = state['user_input']

    # extrair informações importantes para a busca
    infos_search = infos_chain.invoke(user_input)
    query = infos_search.query
    num_papers = infos_search.num_papers
    print(f"\nInformações extraídas da entrada do usuário: {infos_search}")

    # buscar papers
    papers = search_papers(query, num_papers)
    #print(f"\nForam encontrados {len(papers)} artigos.")

    # formatar os papers (títulos, snippet, link)
    formated_papers = format_papers(papers)

    return {'papers': formated_papers}

def generate_answer(state: State):
    user_input = state['user_input']
    papers = state['papers']
    selected_model = state['selected_model']

    #print(f"\nO modelo usado para gerar a resposta é o: {selected_model}")
    llm = ChatOpenAI(model=selected_model)
    papers_text = "".join(papers)

    # prompt que será passado para o modelo
    prompt = f"""Você é um assistente especializado em pesquisa acadêmica. Com base na entrada do usuário e nos artigos fornecidos, gere uma resposta que recomende os artigos mais relevantes com um breve resumo e motivo da escolha., além de sugerir estratégias ou tópicos relacionados, se necessário.
    Entrada do usuário: {user_input}
    Informações dos artigos encontrados: {papers_text}
    Resposta do usuário: """

    answer = (llm.invoke(prompt)).content
    #print(f"\nResposta final: {answer}")

    return {"answer": answer}

# criação do grafo
graph = StateGraph(State)
graph.add_node("get_papers", get_papers)
graph.add_node("generate_answer", generate_answer)

# criar arestas do grafo
graph.add_edge(START, "get_papers")
graph.add_edge("get_papers", "generate_answer")
graph.add_edge("generate_answer", END)

rag_app = graph.compile()