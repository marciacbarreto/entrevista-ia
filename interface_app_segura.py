import streamlit as st

# --- Login Simples com E-mail e Senha ---
def autenticar():
    st.markdown(
        """
        <style>
        .login-box {
            background-color: #f7f1eb;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 8px #ccc;
            width: 340px;
            margin: auto;
        }
        .login-button {
            background-color: #222;
            color: white;
            font-weight: bold;
            padding: 0.6rem 0;
            width: 100%;
            border-radius: 4px;
            border: none;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Entrevista IA</h2>", unsafe_allow_html=True)

    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.checkbox("Remember me")
    with col2:
        st.markdown("<p style='text-align:right;'>Forgot Password?</p>", unsafe_allow_html=True)

    login = st.button("LOGIN", key="login", type="primary")

    st.markdown('</div>', unsafe_allow_html=True)

    # Validação simples
    if login:
        if email == "teste@teste.com" and senha == "1234":
            st.session_state["autenticado"] = True
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# --- Executa a verificação de login ---
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    autenticar()
    st.stop()
