import streamlit as st

# Lista de usuários válidos
USUARIOS_VALIDOS = {
    "marciacbarreto@gmail.com": "senha123",
    "teste@entrevista.com": "entrevista123"
}

def autenticar(email, senha):
    return email in USUARIOS_VALIDOS and USUARIOS_VALIDOS[email] == senha

# Interface de login
st.markdown("""
    <style>
        .login-box {
            background-color: #fff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 8px #ccc;
            width: 340px;
            margin: auto;
        }
        .login-button {
            background-color: #ff4b4b;
            color: white;
            border: none;
            width: 100%;
            padding: 0.5rem;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Entrevista IA</h2>", unsafe_allow_html=True)

with st.form("login_form"):
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    email = st.text_input("Email_

