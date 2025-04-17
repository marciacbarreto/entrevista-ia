import streamlit as st

# Ocultar elementos do Streamlit (barra superior, menu, rodapé)
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Função para redirecionar de página
def redirecionar_para(pagina):
    st.session_state["pagina"] = pagina
    st.experimental_rerun()

# Página de login
def exibir_login():
    st.markdown("## Entrevista IA")
    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            redirecionar_para("upload")
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Página de upload e link
def exibir_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    st.file_uploader("📎 Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    st.text_input("🔗 Adicione o link da reunião")

    if st.button("Voltar ao login"):
        redirecionar_para("login")

# Inicializa estado da sessão
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

# Roteamento
if st.session_state["pagina"] == "login":
    exibir_login()
elif st.session_state["pagina"] == "upload":
    exibir_upload()
