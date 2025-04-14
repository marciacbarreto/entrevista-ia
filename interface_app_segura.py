import streamlit as st
import time

# --- Login com design moderno ---
def autenticar():
    st.set_page_config(page_title="Entrevista IA", layout="centered")
    st.markdown(
        """
        <style>
            .login-box {
                background-color: #f9f9f9;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 400px;
                margin: 50px auto;
                font-family: 'Segoe UI', sans-serif;
            }
            .login-box h2 {
                text-align: center;
                color: #333;
                margin-bottom: 25px;
            }
            .stTextInput>div>div>input, .stTextInput>div>div>div>input {
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #ccc;
                font-size: 14px;
            }
            .stButton button {
                width: 100%;
                padding: 10px;
                background-color: #333;
                color: #fff;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
            }
            .stButton button:hover {
                background-color: #444;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2>Entrevista IA</h2>', unsafe_allow_html=True)

    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")

    if st.button("LOGIN"):
        with st.spinner("Verificando credenciais..."):
            time.sleep(2)  # Simula tempo de verificação

        # Credenciais válidas
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("✅ Login realizado com sucesso!")
            # Aqui você pode chamar uma função ou redirecionar para outro conteúdo
        else:
            st.error("❌ Credenciais inválidas. Verifique seu e-mail e senha.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Executar a função de login
autenticar()
