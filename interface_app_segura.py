import streamlit as st
import openai
import os
import tempfile
import fitz  # PyMuPDF
import PyPDF2
import speech_recognition as sr

# Configuração visual
st.set_page_config(page_title="Entrevista IA", layout="centered")
st.title("🤖 Entrevista IA - Assistente de Respostas")

# Chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para extrair texto de currículo PDF
def extrair_texto_curriculo(caminho):
    if caminho.endswith(".pdf"):
        with fitz.open(caminho) as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            return texto
    return "Formato não suportado."

# Função para responder com base no currículo e vaga
def responder_pergunta(curriculo, vaga, pergunta):
    prompt = f"""
Você é um candidato se preparando para uma entrevista. Responda de forma profissional e convincente em até 5 linhas.
📄 Currículo: {curriculo}
🎯 Vaga: {vaga}
❓ Pergunta do recrutador: {pergunta}

Resposta ideal:
"""
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip()

# Upload do currículo
arquivo = st.file_uploader("📎 Envie seu currículo (PDF)", type=["pdf"])
vaga = st.text_area("📌 Cole aqui a descrição da vaga")

if arquivo and vaga:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(arquivo.read())
        caminho = tmp.name
        texto_curriculo = extrair_texto_curriculo(caminho)
        st.success("✅ Currículo processado com sucesso!")

    st.info("Clique abaixo e fale a pergunta do recrutador")
    if st.button("🎤 Escutar pergunta"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("⏳ Escutando...")
            try:
                audio = recognizer.listen(source, timeout=5)
                pergunta = recognizer.recognize_google(audio, language="pt-BR")
                resposta = responder_pergunta(texto_curriculo, vaga, pergunta)
                st.success(f"📣 Pergunta reconhecida: {pergunta}")
                st.markdown(f"🧠 **Resposta sugerida:**\n\n{resposta}")
            except Exception as e:
                st.error("❌ Não consegui entender sua voz. Tente novamente.")
