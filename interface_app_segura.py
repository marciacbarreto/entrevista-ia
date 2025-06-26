# Gerar a versão FINAL com escuta automática da pergunta via microfone e resposta silenciosa da IA

codigo_voz = '''
import streamlit as st
import os
import openai
import base64
import tempfile
import speech_recognition as sr
from PyPDF2 import PdfReader

# Configuração visual
st.set_page_config(page_title="Entrevista IA", layout="centered")
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding-top: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Controle de etapas
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"

# Extrair texto do currículo
def extrair_texto_curriculo(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text()
        return texto
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

# Escutar pergunta via microfone
def escutar_pergunta():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Escutando... Faça a pergunta agora.")
        audio = reconhecedor.listen(source)
    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        return texto
    except sr.UnknownValueError:
        st.warning("Não entendi a pergunta. Tente novamente.")
        return ""
    except sr.RequestError:
        st.error("Erro ao acessar o serviço de voz.")
        return ""

# Responder com base no currículo
def responder_pergunta(pergunta, texto_curriculo):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Você é um candidato em uma entrevista. Com base neste currículo:\\n\\n{texto_curriculo}\\n\\nPergunta do recrutador: {pergunta}\\n\\nResponda como se fosse o candidato:"
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você está simulando uma entrevista profissional."},
            {"role": "user", "content": prompt}
        ]
    )
    return resposta.choices[0].message.content.strip()

# Página 1: Login
def pagina_login():
    st.title("Entrevista IA")
    st.subheader("Acesse com seu login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.session_state.etapa = "upload"
        else:
            st.error("Email ou senha incorretos.")

# Página 2: Upload
def pagina_upload():
    st.title("Envie seu currículo e link da reunião")
    curriculo = st.file_uploader("Currículo (PDF, DOCX ou TXT)", type=["pdf", "docx", "txt"])
    link = st.text_input("Link da reunião (Zoom, Meet, etc)")
    if st.button("Confirmar e continuar"):
        if curriculo and link:
            texto = extrair_texto_curriculo(curriculo)
            st.session_state.curriculo_texto = texto
            st.session_state.reuniao_link = link
            st.session_state.etapa = "entrevista"
        else:
            st.warning("Envie o currículo e o link da reunião.")

# Página 3: Simulação com escuta de voz
def pagina_entrevista():
    st.title("Simulação da Entrevista IA")
    st.markdown("Clique abaixo, fale a pergunta do recrutador e receba a resposta automaticamente.")
    if st.button("🎙️ Ouvir pergunta"):
        pergunta = escutar_pergunta()
        if pergunta:
            st.success(f"Pergunta transcrita: {pergunta}")
            resposta = responder_pergunta(pergunta, st.session_state.curriculo_texto)
            st.markdown("### Resposta sugerida pela IA:")
            st.success(resposta)

# Controle de páginas
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "entrevista":
    pagina_entrevista()
'''

from pathlib import Path

caminho_final_voz = Path("/mnt/data/interface_app_segura.py")
caminho_final_voz.write_text(codigo_voz, encoding="utf-8")
caminho_final_voz
