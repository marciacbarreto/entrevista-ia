import streamlit as st
import openai
import os

# Ocultar elementos do Streamlit (barra superior, menu, footer)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# LOGIN
def autenticar():
    st.markdown("""
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
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">Entrevista IA</h2>', unsafe_allow_html=True)
    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.experimental_set_query_params(pagina="upload")  # <- Troca de tela aqui
        else:
            st.error("Credenciais inválidas. Tente novamente.")
    st.markdown('</div>', unsafe_allow_html=True)

autenticar()
