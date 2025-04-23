import streamlit as st

# Funções para navegação de páginas
def trocar_pagina(pagina):
    st.session_state["pagina"] = pagina

# Página 1: Login
def exibir_login():
    st.title("Entrevista IA")
    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            trocar_pagina("upload")
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Página 2: Upload e Link da Reunião
def exibir_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link_reuniao = st.text_input("Adicione o link da reunião")
    if st.button("Confirmar e entrar na reunião"):
        if arquivo is not None and link_reuniao:
            st.session_state["curriculo_nome"] = arquivo.name
            st.session_state["link_reuniao"] = link_reuniao
            trocar_pagina("entrevista")
        else:
            st.warning("Adicione o currículo e o link da reunião antes de avançar.")
    if st.button("Voltar ao login"):
        trocar_pagina("login")

# Página 3: Simulação de Entrevista
def exibir_entrevista():
    st.title("Página 3 - Simulação de Entrevista")
    nome_curriculo = st.session_state.get("curriculo_nome", "Nenhum arquivo enviado")
    link_reuniao = st.session_state.get("link_reuniao", "Não informado")
    st.write(f"**Currículo recebido:** {nome_curriculo}")
    st.write(f"**Link da reunião:** {link_reuniao}")
    st.info("Aqui será a simulação da entrevista IA. (Personalize conforme desejar!)")
    if st.button("Voltar ao upload"):
        trocar_pagina("upload")
    if st.button("Sair"):
        trocar_pagina("login")

# Roteamento das páginas
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

if st.session_state["pagina"] == "login":
    exibir_login()
elif st.session_state["pagina"] == "upload":
    exibir_upload()
elif st.session_state["pagina"] == "entrevista":
    exibir_entrevista()
