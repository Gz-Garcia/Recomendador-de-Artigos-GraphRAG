from openai import OpenAI
import streamlit as st

with open('tools/llm_prompt.txt', 'r', encoding = 'utf-8') as f:
    system_prompt = f.read()

# https://platform.openai.com/docs/api-reference/chat/create
def chat(user_prompt, model, max_tokens=200, temp=0.5):
    # Cria o chat usando a API
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    completion = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content":  user_prompt}
        ],
        temperature=temp,
        max_tokens=max_tokens,
        stream=True
    )

    return completion

# handles stream response back from LLM
def stream_parser_llm(stream):
    for chunk in stream:
        if chunk.choices[0].delta.content != None:
            yield chunk.choices[0].delta.content