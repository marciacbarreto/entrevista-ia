import streamlit as st

st.set_page_config(page_title="Entrevista IA", layout="centered")

# Oculta barra superior
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Controle de página
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"
if "curriculo" not in st.session_state:
    st.session_state.curriculo = None
if "link" not in st.session_state:
    st.session_state.link = ""

# Página 1 - Login
def pagina_login():
    st.title("Entrevista IA")
    st.write("Faça o login para continuar.")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    lembrar = st.checkbox("Lembrar-me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state.etapa = "upload"
            st.experimental_rerun()
        else:
            st.error("Email ou senha incorretos.")

# Página 2 - Upload + Link
def pagina_upload():
    st.title("Reunião")
    st.markdown("Adicione seu currículo ou anexo (PDF, DOCX, TXT)")
    arquivo = st.file_uploader("Currículo:", type=["pdf", "docx", "txt"])
    if arquivo:
        st.session_state.curriculo = arquivo
    link = st.text_input("Adicione o link da reunião", value=st.session_state.link)
    if link:
        st.session_state.link = link
    if st.button("Confirmar e entrar na reunião"):
        if st.session_state.curriculo and st.session_state.link:
            st.session_state.etapa = "simulacao"
            st.experimental_rerun()
        else:
            st.warning("Por favor, adicione o currículo e o link da reunião.")
    if st.button("Voltar para login"):
        st.session_state.etapa = "login"
        st.experimental_rerun()

# Página 3 - Simulação da entrevista
def pagina_simulacao():
    st.title("Página 3 - Simulação de Entrevista")
    st.markdown(f"**Currículo recebido:** {st.session_state.curriculo.name if st.session_state.curriculo else ''}")
    st.markdown(f"**Link da reunião:** [Acessar reunião]({st.session_state.link})")
    st.info("Aqui será a simulação da entrevista IA. Personalize com IA ou orientações.")
    if st.button("Voltar para upload"):
        st.session_state.etapa = "upload"
        st.experimental_rerun()
    if st.button("Sair"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

# Execução com base na etapa
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
