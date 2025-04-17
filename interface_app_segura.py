import streamlit as st

# Função para redirecionar entre páginas
def redirecionar_para(pagina):
    st.experimental_set_query_params(pagina=pagina)
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

# Página de upload
def exibir_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("📎 Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link_reuniao = st.text_input("🔗 Adicione o link da reunião")

    if st.button("Voltar ao login"):
        redirecionar_para("login")

# Controlador de página
param = st.experimental_get_query_params()
pagina = param.get("pagina", ["login"])[0]

# Roteamento
if pagina == "login":
    exibir_login()
elif pagina == "upload":
    exibir_upload()
else:
    exibir_login()
