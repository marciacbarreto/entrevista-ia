from pathlib import Path

# Código final completo com todas as correções solicitadas, incluindo:
# - Login no início
# - Uso do currículo como base, mas não como limitação
# - Prompt ajustado para respeitar a pergunta do recrutador
codigo_final_completo = '''
import streamlit as st
import openai
import os
import json
import base64
import tempfile
import speech_recognition as sr
from PyPDF2 import PdfReader

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Entrevista IA", layout="centered")

# LOGIN - BLOQUEIA O APP ATÉ O USUÁRIO AUTORIZADO ENTRAR
emails_autorizados = ["marciacbarreto@gmail.com"]
senha_correta = "123456"

st.title("🔒 Login de Acesso")
email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

if email not in emails_autorizados or senha != senha_correta:
    st.warning("Informe seu e-mail e senha corretos para acessar.")
    st.stop()

# CONTEÚDO PRINCIPAL DO APP
st.title("Entrevista IA")
st.write("Faça sua pergunta abaixo ou use o microfone (em breve!)")

# CHAVE DA API
openai.api_key = os.getenv("OPENAI_API_KEY")

# UPLOAD DE CURRÍCULO
st.subheader("Upload do currículo (PDF, DOCX, etc.)")
uploaded_file = st.file_uploader("Escolha o arquivo do currículo", type=["pdf", "docx", "txt"])

dados_curriculo = ""
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(tmp_path)
        dados_curriculo = " ".join([page.extract_text() or "" for page in reader.pages])
    elif uploaded_file.name.endswith(".txt") or uploaded_file.name.endswith(".docx"):
        with open(tmp_path, "r", encoding="utf-8") as f:
            dados_curriculo = f.read()
    st.success("Currículo carregado com sucesso!")

# CAMPO PARA LINK DA REUNIÃO
st.subheader("Link da reunião")
link_reuniao = st.text_input("Cole aqui o link da reunião")

# CAMPO PARA PERGUNTA DO RECRUTADOR
st.subheader("Pergunta do recrutador")
pergunta = st.text_input("Digite ou fale sua pergunta")

# BOTÃO PARA GERAR RESPOSTA
if st.button("Responder"):
    if not dados_curriculo:
        st.error("Por favor, envie um currículo primeiro.")
    elif not pergunta:
        st.error("Digite ou fale a pergunta primeiro.")
    else:
        prompt = f"Você é um candidato em uma entrevista de emprego. Use o currículo abaixo como base, mas responda à pergunta do recrutador de forma completa, mesmo que precise ir além do currículo.\n\nCurrículo:\n{dados_curriculo}\n\nPergunta do recrutador:\n{pergunta}"
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você está participando de uma entrevista de emprego. Responda com confiança e objetividade."},
                {"role": "user", "content": prompt}
            ]
        )
        resposta_texto = resposta['choices'][0]['message']['content']
        st.success("Resposta sugerida:")
        st.write(resposta_texto)
'''

# Salvar o código em arquivo
arquivo_final = Path("/mnt/data/interface_app_segura.py")
arquivo_final.write_text(codigo_final_completo)

arquivo_final.name
