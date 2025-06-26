import streamlit as st
import os
import openai
import speech_recognition as sr

st.set_page_config(page_title="Entrevista IA", layout="centered")

if "etapa" not in st.session_state:
    st.session_state.etapa = "Conecte-se"

def pagina_login():
    st.title("Entrevista IA")
    st.subheader("Faça o login para continuar.")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    st.checkbox("Lembrar-me")

    if st.button("CONECTE-SE"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state.etapa = "carregar"
        else:
            st.error("Credenciais inválidas.")

def pagina_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("Currículo", type=["pdf", "docx", "txt"])
    link = st.text_input("Link da reunião:")

    if st.button("Confirmar e entrar na reunião"):
        if arquivo and link:
            st.session_state.curriculo = arquivo.read().decode("utf-8", errors="ignore")
            st.session_state.reuniao = link
            st.session_state.etapa = "simulacao"
        else:
            st.warning("Envie o currículo e o link.")

    if st.button("Voltar ao login"):
        st.session_state.etapa = "Conecte-se"

def pagina_simulacao():
    st.title("Página 3 - Simulação da Entrevista")
    pergunta = ""

    if st.button("Ouvir pergunta do recrutador"):
        reconhecedor = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Escutando...")
            audio = reconhecedor.listen(source)
        try:
            pergunta = reconhecedor.recognize_google(audio, language="pt-BR")
            st.success(f"Pergunta reconhecida: {pergunta}")
        except sr.UnknownValueError:
            st.warning("Não entendi a pergunta.")
        except sr.RequestError:
            st.error("Erro ao acessar o serviço de voz.")

    if pergunta:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Currículo:\n{st.session_state.curriculo}\n\nPergunta: {pergunta}\n\nResponda como se fosse o candidato:"
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você está simulando uma entrevista de emprego."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.write("### Resposta sugerida:")
            st.success(resposta.choices[0].message.content)
        except Exception as e:
            st.error("Erro ao gerar resposta da IA.")

    if st.button("Voltar ao upload"):
        st.session_state.etapa = "carregar"
    if st.button("Sair"):
        st.session_state.etapa = "Conecte-se"

if st.session_state.etapa == "Conecte-se":
    pagina_login()
elif st.session_state.etapa == "carregar":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
