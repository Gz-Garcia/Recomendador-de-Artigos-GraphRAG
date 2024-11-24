from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(model='gpt-4o')

# extrair informações importantes da entrada do usuário
class SearchInfos(BaseModel):
  query: str = Field(description="Termo principal da entrada do usuário. Será usado para buscar artigos acadêmicos. Não deve ser muito longo.")
  num_papers: int = Field(description="Quantidade de artigos que devem ser buscados. Caso o usuário não especifique, use o valor 10 como padrão.")

prompt_infos = ChatPromptTemplate.from_messages([
    ("system", """A partir de uma entrada do usuário, extraia as informações importantes que serão usadas para buscar artigos acadêmicos de acordo com a demanda específica do usuário. 
     Caso o usuário mencione artigos mais recentes, acrescente o ano '2024' na query que será usada para a busca de artigos relevantes."""),
    ("human", "{user_input}")
])

infos_chain = prompt_infos | llm.with_structured_output(schema=SearchInfos)