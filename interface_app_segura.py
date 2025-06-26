import streamlit as st

# Configura layout fixo e oculta sidebar
st.set_page_config(page_title="Entrevista IA", layout="centered", initial_sidebar_state="collapsed")

# Inicia o fluxo
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"

# Página 1: Login
def pagina_login():
    st.markdown("<h1 style='text-align: center;'>Entrevista IA</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Faça o login para continuar.</h4>", unsafe_allow_html=True)
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    lembrar = st.checkbox("Lembrar-me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.session_state.etapa = "upload"
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Página 2: Upload e Link
def pagina_upload():
    st.markdown("<h2>Página 2 - Upload e Link da Reunião</h2>", unsafe_allow_html=True)
    st.markdown("Adicione seu currículo ou anexo (PDF, DOCX, TXT)")
    arquivo = st.file_uploader("Currículo", type=["pdf", "docx", "txt"])
    link = st.text_input("Link da reunião:")
    if st.button("Confirmar e entrar na reunião"):
        if arquivo and link:
            st.session_state.curriculo = arquivo.name
            st.session_state.link = link
            st.session_state.etapa = "simulacao"
        else:
            st.warning("Envie o currículo e o link.")
    if st.button("Voltar ao login"):
        st.session_state.etapa = "login"

# Página 3: Simulação
def pagina_simulacao():
    st.markdown("<h2>Página 3 - Simulação de Entrevista</h2>", unsafe_allow_html=True)
    st.write("Currículo recebido:", st.session_state.curriculo)
    st.write("Link da reunião:", f"[Acessar reunião]({st.session_state.link})")
    st.success("Aqui será a simulação da entrevista IA. Personalize conforme desejar!")
    if st.button("Voltar ao upload"):
        st.session_state.etapa = "upload"
    if st.button("Sair"):
        st.session_state.etapa = "login"

# Executa a página conforme o estágio
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
