import streamlit as st
import openai
import os

st.title("Entrevista IA")
st.write("Faça sua pergunta abaixo ou use o microfone (em breve)!")

# Chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Entrada do usuário
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    with st.spinner("Pensando..."):
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente de entrevistas amigável."},
                    {"role": "user", "content": pergunta}
                ]
            )
            st.success(resposta.choices[0].message.content)
        except Exception as e:
            st.error(f"Erro ao obter resposta: {e}")
