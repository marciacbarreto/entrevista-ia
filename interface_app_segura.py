import streamlit as st

# ----- Funções das páginas -----
def pagina_login():
    st.title("Entrevista IA")
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.session_state["logado"] = True
            st.session_state["pagina"] = "upload"
        else:
            st.error("Login ou senha incorretos.")

def pagina_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link = st.text_input("Adicione o link da reunião")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Confirmar e entrar na reunião"):
            if arquivo and link:
                st.session_state["arquivo"] = arquivo.name
                st.session_state["link"] = link
                st.session_state["pagina"] = "entrevista"
            else:
                st.warning("Adicione o currículo e o link da reunião!")
    with col2:
        st.button("Voltar ao login", on_click=lambda: mudar_pagina("login"))

def pagina_entrevista():
    st.title("Página 3 - Simulação de Entrevista")
    st.write(f"**Currículo recebido:** {st.session_state.get('arquivo', '')}")
    st.write(f"**Link da reunião:** {st.session_state.get('link', '')}")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://via.placeholder.com/180x220.png?text=Eu+na+reuni%C3%A3o", caption="Eu na reunião")
    with col2:
        st.image("https://via.placeholder.com/180x220.png?text=Recrutador", caption="Recrutador")
    st.markdown("### Perguntas e resposta aqui")
    st.info("Aqui será a simulação da entrevista IA. (Personalize conforme desejar!)")
    st.button("Sair", on_click=lambda: mudar_pagina("login"))

# ----- Fluxo de páginas -----
def mudar_pagina(destino):
    st.session_state["pagina"] = destino
    if destino == "login":
        st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"
if "logado" not in st.session_state:
    st.session_state["logado"] = False

st.set_page_config(page_title="Entrevista IA", layout="wide")

# ----- Remove barra, rodapé e menu do Streamlit -----
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ----- Renderização das páginas -----
if st.session_state["pagina"] == "login":
    pagina_login()
elif st.session_state["pagina"] == "upload":
    pagina_upload()
elif st.session_state["pagina"] == "entrevista":
    pagina_entrevista()
