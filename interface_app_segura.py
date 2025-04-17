import streamlit as st
import os

# Redirecionar entre páginas
def redirecionar_para(pagina):
    st.query_params(pagina=pagina)
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
            redirecionar_para("segunda")
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Página 2 - Upload e link da reunião
def exibir_pagina2():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("📎 Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link_reuniao = st.text_input("🔗 Adicione o link da reunião")

    if st.button("Voltar ao login"):
        redirecionar_para("login")

# Controlador de páginas
param = st.query_params()
pagina = param.get("pagina", ["login"])[0]

if pagina == "login":
    exibir_login()
elif pagina == "segunda":
    exibir_pagina2()
else:
    exibir_login()
