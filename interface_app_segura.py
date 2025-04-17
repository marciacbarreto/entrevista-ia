import streamlit as st
import os

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

# Redirecionamento de página (compatível com Streamlit atual)
def redirecionar_para_pagina(pagina):
    st.switch_page(pagina)

def autenticar():
    st.markdown(
        """
        <style>
            .login-box {
                background-color: #f2f2f2;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 380px;
                margin: 0 auto;
            }
            .login-box input[type="text"],
            .login-box input[type="password"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            .login-box button {
                width: 100%;
                padding: 10px;
                background-color: #333;
                color: #fff;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
            }
            .login-box button:hover {
                background-color: #555;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">Entrevista IA</h2>', unsafe_allow_html=True)
    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.experimental_set_query_params(pagina="segunda")
            st.experimental_rerun()
        else:
            st.error("Credenciais inválidas. Tente novamente.")
    st.markdown('</div>', unsafe_allow_html=True)

# Verificar parâmetros da URL para mudança de página
param = st.experimental_get_query_params()
if param.get("pagina") == ["segunda"]:
    st.title("Página 2 – Upload e Link da Reunião")
    st.file_uploader("📎 Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    st.text_input("🔗 Adicione o link da reunião")
    st.markdown("⬅️ Voltar ao login", unsafe_allow_html=True)
    if st.button("Voltar"):
        st.experimental_set_query_params()
        st.experimental_rerun()
else:
    autenticar()
autenticar()
