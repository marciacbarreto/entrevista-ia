import streamlit as st
import os
import openai
import speech_recognition as sr

# Configura a página e oculta o menu lateral
st.set_page_config(page_title="Entrevista IA", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inicializa a etapa de navegação
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"

# Função: Login
def pagina_login():
    st.title("Entrevista IA")
    st.subheader("Faça o login para continuar.")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    st.checkbox("Lembrar-me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state.etapa = "upload"
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Função: Upload de currículo e link
def pagina_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    st.markdown("Adicione seu currículo ou anexo (PDF, DOCX, TXT)")

    arquivo = st.file_uploader("Currículo:", type=["pdf", "docx", "txt"])
    link = st.text_input("Link da reunião:")

    if st.button("Confirmar e entrar na reunião"):
        if arquivo is not None:
            texto_cv = arquivo.read().decode("utf-8", errors="ignore")
            st.session_state.curriculo_texto = texto_cv
            st.session_state.reuniao_link = link
            st.session_state.etapa = "simulacao"
        else:
            st.warning("Envie o currículo antes de continuar.")

    if st.button("Voltar ao login"):
        st.session_state.etapa = "login"

# Função: Escutar pergunta via voz
def escutar_pergunta():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Ouvindo... Faça a pergunta agora.")
        audio = recognizer.listen(source)
    try:
        pergunta = recognizer.recognize_google(audio, language="pt-BR")
        st.success(f"Pergunta transcrita: {pergunta}")
        return pergunta
    except sr.UnknownValueError:
        st.error("Não entendi a pergunta. Fale novamente.")
        return ""
    except sr.RequestError:
        st.error("Erro na conexão com o serviço de transcrição.")
        return ""

# Função: Responder com base no currículo
def responder_ia(pergunta, curriculo_texto):
    prompt = f"""Baseado no seguinte currículo:\n\n{curriculo_texto}\n\nResponda à pergunta a seguir como se fosse o candidato:\n\n{pergunta}"""
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

# Função: Simulação da entrevista
def pagina_simulacao():
    st.title("Página 3 - Simulação de Entrevista")
    st.write("Clique no botão abaixo e fale como se fosse o recrutador.")

    if st.button("Ouvir pergunta"):
        pergunta = escutar_pergunta()
        if pergunta:
            resposta = responder_ia(pergunta, st.session_state.get("curriculo_texto", ""))
            st.markdown("### Resposta sugerida:")
            st.success(resposta)

    if st.button("Voltar para upload"):
        st.session_state.etapa = "upload"
    if st.button("Sair"):
        st.session_state.etapa = "login"

# Controle de navegação
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
