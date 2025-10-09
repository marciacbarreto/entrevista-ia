import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF
import PyPDF2
import speech_recognition as sr
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Entrevista IA", layout="centered")
st.markdown("<h1 style='text-align: center;'>Entrevista IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Envie seu currículo e a vaga. Fale e receba a resposta ideal.</p>", unsafe_allow_html=True)

# API OpenAI
chave_api = os.getenv("ABRIR_CHAVE_API")
client = OpenAI(api_key=chave_api)

# Função para extrair texto do currículo
def extrair_texto_pdf(caminho):
    texto = ""
    if caminho.name.endswith(".pdf"):
        with fitz.open(stream=caminho.read(), filetype="pdf") as doc:
            for pagina in doc:
                texto += pagina.get_text()
    return texto

# Upload dos arquivos
col1, col2 = st.columns(2)
with col1:
    arquivo_curriculo = st.file_uploader("📎 Anexe seu currículo (PDF)", type="pdf")
with col2:
    vaga = st.text_area("💼 Cole a vaga de interesse", height=130)

# Campo para iniciar escuta
if arquivo_curriculo and vaga:
    texto_curriculo = extrair_texto_pdf(arquivo_curriculo)

    st.markdown("---")
    st.markdown("🎙️ Clique abaixo e faça sua pergunta como se fosse o recrutador:")

    if st.button("🎤 Ouvir pergunta"):
        reconhecedor = sr.Recognizer()
        with sr.Microphone() as source:
            audio = reconhecedor.listen(source, phrase_time_limit=5)

        try:
            pergunta = reconhecedor.recognize_google(audio, language="pt-BR")
            with st.spinner("Pensando na melhor resposta..."):
                prompt = f"""
Você é um assistente de entrevistas. Com base neste currículo e nesta vaga, responda de forma natural como se fosse o candidato.

VAGA:
{vaga}

CURRÍCULO:
{texto_curriculo}

PERGUNTA DO RECRUTADOR:
{pergunta}

RESPOSTA DO CANDIDATO EM ATÉ 5 LINHAS:
"""
                resposta = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=500
                )
                st.success(resposta.choices[0].message.content.strip())

        except sr.UnknownValueError:
            st.warning("⚠️ Não foi possível entender o que foi falado.")
        except Exception as e:
            st.error(f"Erro: {e}")
else:
    st.info("📄 Envie o currículo e cole a vaga para ativar o campo de pergunta.")
