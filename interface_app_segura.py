import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF
import PyPDF2
import docx
from openai import OpenAI

# Configuração visual
st.set_page_config(page_title="Entrevista IA", layout="centered")
st.markdown("<h1 style='text-align: center;'>Entrevista IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>1️⃣ Envie seu currículo | 2️⃣ Cole a vaga | 3️⃣ Faça a pergunta</p>", unsafe_allow_html=True)

# Chave da API
chave_api = os.getenv("ABRIR_CHAVE_API")
client = OpenAI(api_key=chave_api)

# Função para extrair texto
def extrair_texto(caminho):
    texto = ""
    if caminho.name.endswith(".pdf"):
        with fitz.open(stream=caminho.read(), filetype="pdf") as doc:
            for pagina in doc:
                texto += pagina.get_text()
    elif caminho.name.endswith(".docx"):
        doc = docx.Document(caminho)
        texto = "\n".join([p.text for p in doc.paragraphs])
    return texto

# Layout: envio de currículo e vaga
col1, col2 = st.columns(2)
with col1:
    arquivo = st.file_uploader("📎 Currículo (PDF ou DOCX)", type=["pdf", "docx"])
with col2:
    vaga = st.text_area("💼 Cole a vaga", height=140)

# Campo de pergunta
if arquivo and vaga:
    texto_curriculo = extrair_texto(arquivo)
    pergunta = st.text_input("❓ Digite a pergunta do recrutador")

    if pergunta:
        with st.spinner("Gerando resposta..."):
            prompt = f"""
Você é um assistente de entrevistas. Com base neste currículo e nesta vaga, responda como se fosse o candidato.

VAGA:
{vaga}

CURRÍCULO:
{texto_curriculo}

PERGUNTA:
{pergunta}

RESPOSTA DO CANDIDATO EM ATÉ 5 LINHAS:
"""
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500
            )
            st.success(resposta.choices[0].message.content.strip())
else:
    st.info("📄 Envie o currículo e cole a vaga para ativar o campo de pergunta.")
