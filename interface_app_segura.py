import streamlit as st
import openai
import os
import tempfile
import fitz  # PyMuPDF
import speech_recognition as sr
import docx2txt
import pdfplumber

st.set_page_config(page_title="Entrevista IA", layout="wide")

# Inicializa a etapa da navegação
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"

def pagina_login():
    st.title("Entrevista IA")
    st.subheader("Faça o login para continuar")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email == "marciacbarreto@gmail.com" and senha == "123456":
            st.session_state.etapa = "upload"
        else:
            st.error("Credenciais inválidas.")

def pagina_upload():
    st.title("Upload do Currículo e Link da Reunião")
    arquivo = st.file_uploader("Envie seu currículo (PDF, DOCX ou TXT)", type=["pdf", "docx", "txt"])
    link_reuniao = st.text_input("Cole aqui o link da reunião (Zoom, Meet, etc.)")
    if st.button("Confirmar e continuar"):
        if arquivo:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(arquivo.read())
                caminho_arquivo = tmp.name
            st.session_state.curriculo = extrair_texto_curriculo(caminho_arquivo)
            st.session_state.etapa = "entrevista"
        else:
            st.error("Por favor, envie seu currículo.")

def pagina_entrevista():
    st.title("Entrevista Simulada")
    pergunta = st.text_input("Pergunta do recrutador (digite ou use o microfone)")
    if st.button("Responder"):
        if pergunta:
            resposta = responder_ia(pergunta)
            st.success(f"Resposta sugerida: {resposta}")
        else:
            st.warning("Digite a pergunta para obter a resposta.")

def extrair_texto_curriculo(caminho):
    if caminho.endswith(".pdf"):
        texto = ""
        try:
            with pdfplumber.open(caminho) as pdf:
                for page in pdf.pages:
                    texto += page.extract_text() or ""
        except:
            texto = "Erro ao ler PDF."
        return texto
    elif caminho.endswith(".docx"):
        return docx2txt.process(caminho)
    elif caminho.endswith(".txt"):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def responder_ia(pergunta):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    contexto = f"Base do currículo: {st.session_state.curriculo}\nPergunta: {pergunta}\nResposta:"
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": contexto}]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao responder: {e}"

# Controle de navegação
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "entrevista":
    pagina_entrevista()
