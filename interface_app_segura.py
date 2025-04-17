import streamlit as st

def redirecionar_para(pagina):
    st.experimental_set_query_params(pagina=pagina)
    st.experimental_rerun()

def exibir_login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">Entrevista IA</h2>', unsafe_allow_html=True)

    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            redirecionar_para("segunda")
        else:
            st.error("Credenciais inválidas. Tente novamente.")
    st.markdown('</div>', unsafe_allow_html=True)

def exibir_pagina2():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("📁 Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link_reuniao = st.text_input("🔗 Adicione o link da reunião")

    if st.button("Voltar ao login"):
        redirecionar_para("login")

# 🔁 Controlador de página
param = st.experimental_get_query_params()
pagina = param.get("pagina", ["login"])[0]

if pagina == "login":
    exibir_login()
elif pagina == "segunda":
    exibir_pagina2()
else:
    exibir_login()

# ✅ Download do código corrigido (opcional)
codigo_corrigido = '''
import streamlit as st

def redirecionar_para(pagina):
    st.experimental_set_query_params(pagina=pagina)
    st.experimental_rerun()

def exibir_login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">Entrevista IA</h2>', unsafe_allow_html=True)
    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            redirecionar_para("segunda")
        else:
            st.error("Credenciais inválidas. Tente novamente.")
    st.markdown('</div>', unsafe_allow_html=True)

def exibir_pagina2():
    st.title("Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("📁 Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link_reuniao = st.text_input("🔗 Adicione o link da reunião")
    if st.button("Voltar ao login"):
        redirecionar_para("login")

param = st.experimental_get_query_params()
pagina = param.get("pagina", ["login"])[0]

if pagina == "login":
    exibir_login()
elif pagina == "segunda":
    exibir_pagina2()
else:
    exibir_login()
'''

import base64
b64 = base64.b64encode(codigo_corrigido.encode()).decode()
href = f'<a href="data:file/txt;base64,{b64}" download="interface_app_segura.py">📥 Clique aqui para baixar o código corrigido</a>'
st.markdown(href, unsafe_allow_html=True)
