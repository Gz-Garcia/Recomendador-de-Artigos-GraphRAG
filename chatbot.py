import streamlit as st

from openai import OpenAI
from graph_rag import rag_app
from tools.search import search_papers, format_papers
from llm_helper import chat

st.set_page_config(
    page_title="Recomendador de Artigos",
    initial_sidebar_state="expanded"
)

st.title("Recomendador de artigos acadêmicos")

# Controles da barra lateral
with st.sidebar:
    st.markdown("# Opções do Modelo")
    
    method = st.selectbox('Método de busca',('LLM com graphRAG', 'LLM pura', 'API de busca'))
    
    if method != 'API de busca':
        # Seleção de modelos da openai
        model = st.selectbox('Modelo',('gpt-3.5-turbo', 'gpt-4o'))
    
    else:
        nreturns = st.number_input('Retornos', value=5, min_value=1, max_value=10, step=1,
                                            help="A quantidade de artigos que serão retornados")
    
    if method == 'LLM com graphRAG':
        st.divider()
        st.markdown("Dica: Para fazer outros tipos de perguntas à llm, troque o modo de busca")
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# função auxiliar para o envio de respostas
def stream_parser(stream):
    for chunk in stream:
            yield chunk

# Guarda os 
if user_prompt := st.chat_input("Peça recomendações de artigos acadêmicos sobre um determinado assunto"):
    # Mostra a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    # Adiciona a mensagem enviada na seção so usuário
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Spinner da interface
    with st.spinner('Procurando artigos...'):
        
        if(method == 'LLM com graphRAG'):

            # Chamada do graph rag com o prompt do usuario
            response = rag_app.invoke({'user_input':  user_prompt, 'selected_model': model})['answer']
            
        elif(method == 'LLM pura'):
            # Envia a resposta pro llm-helper e faz uma chamada pura para a OpenAI
            response = chat(user_prompt, model=model)
            
        else:
            # Envia o prompt diretamente pra SerpAPI e faz uma busca no googcle academico
            response = format_papers(search_papers(user_prompt, nreturns))
        
        # Mostrar a resposta em forma de cluxo
        stream_output = st.write_stream(stream_parser(response))
        
        # Adiciona a resposta na seção do usuário
        st.session_state.messages.append({"role": "assistant", "content": stream_output})

    # Seleciona a ultima resposta para evitar  odisplay repetido 
    last_response =  st.session_state.messages[len(st.session_state.messages)-1]['content']

    if str(last_response) != str(stream_output):
        with st.chat_message("assistant"):
            st.markdown(stream_output)



