from pathlib import Path
import streamlit as st

# Ocultar barra superior
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Redirecionamento de página
def redirecionar_para(pagina):
    st.experimental_set_query_params(pagina=pagina)
    st.experimental_rerun()

# Página 1 - Login
def exibir_login():
    st.title("🔒 Entrevista IA")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    lembrar = st.checkbox("Remember me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            redirecionar_para("upload")
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Página 2 - Upload e link
def exibir_upload():
    st.title("📄 Página 2 - Upload e Link da Reunião")
    st.write("📎 Adicione seu currículo ou anexo")
    uploaded_file = st.file_uploader("Arraste ou selecione o arquivo", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        st.session_state["curriculo"] = uploaded_file.name

    link = st.text_input("🔗 Adicione o link da reunião")
    if link:
        st.session_state["link"] = link

    if st.button("Confirmar e entrar na reunião"):
        if "curriculo" in st.session_state and "link" in st.session_state:
            redirecionar_para("entrevista")
        else:
            st.warning("Por favor, envie o currículo e o link da reunião.")

    if st.button("Voltar ao login"):
        redirecionar_para("login")

# Página 3 - Simulação de entrevista
def exibir_entrevista():
    st.title("🧠 Simulação da Entrevista")
    st.write("**Currículo recebido:**", st.session_state.get("curriculo", "Não enviado"))
    st.write("**Link da reunião:**", st.session_state.get("link", "Não informado"))
    st.markdown("A entrevista será iniciada agora. Mantenha a postura e boa sorte!")

# Gerenciar as páginas
param = st.experimental_get_query_params()
pagina = param.get("pagina", ["login"])[0]

if pagina == "login":
    exibir_login()
elif pagina == "upload":
    exibir_upload()
elif pagina == "entrevista":
    exibir_entrevista()


