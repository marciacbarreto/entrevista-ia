import streamlit as st
import tempfile
import os
import speech_recognition as sr
import openai
from PyPDF2 import PdfReader

# Chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para extrair texto do currículo PDF
def extrair_texto_pdf(arquivo):
    leitor = PdfReader(arquivo)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text()
    return texto

# Função para escutar e transcrever a pergunta do recrutador
def escutar_pergunta():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        with st.spinner("Escutando pergunta..."):
            audio = reconhecedor.listen(fonte)
        try:
            pergunta = reconhecedor.recognize_google(audio, language='pt-BR')
            return pergunta
        except:
            return "Não foi possível reconhecer a pergunta."

# Função para gerar resposta com base no currículo e na vaga
def responder_ia(curriculo, vaga, pergunta):
    prompt = f"""
    Você é um assistente de entrevista inteligente. 
    Analise o currículo abaixo e a descrição da vaga. 
    Responda à pergunta do recrutador de forma objetiva, clara e profissional, em até 5 linhas.

    Currículo:
    {curriculo}

    Vaga:
    {vaga}

    Pergunta:
    {pergunta}

    Resposta:
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip()

# Interface limpa
st.set_page_config(page_title="Entrevista IA", layout="centered", initial_sidebar_state="collapsed")
st.title("🤖 Entrevista IA - Assistente de Respostas")

# Upload do currículo
curriculo_enviado = st.file_uploader("📄 Envie seu currículo (PDF)", type=["pdf"])
campo_vaga = st.text_area("💼 Cole a descrição da vaga")

if curriculo_enviado and campo_vaga:
    if st.button("🎤 Escutar e Responder"):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(curriculo_enviado.read())
            caminho = tmp.name
        texto_curriculo = extrair_texto_pdf(caminho)
        pergunta = escutar_pergunta()
        resposta = responder_ia(texto_curriculo, campo_vaga, pergunta)
        st.success("✅ Resposta gerada:")
        st.markdown(f"**{resposta}**")
else:
    st.info("Envie o currículo e cole a vaga para ativar o assistente."
