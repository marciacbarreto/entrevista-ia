import streamlit as st

# 👉 Oculta menu lateral e rodapé
st.set_page_config(page_title="Entrevista IA", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        .block-container {
            max-width: 700px;
            margin: auto;
            padding-top: 3rem;
        }
        header, footer, .css-1v0mbdj.e115fcil1, .st-emotion-cache-6qob1r {
            display: none;
        }
        .stTextInput > div > div > input {
            text-align: center;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 0.5em;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .stMarkdown h1, .stMarkdown h2 {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 👉 Estado inicial
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"

# 👉 Página 1: Login
def pagina_login():
    st.title("Entrevista IA")
    st.subheader("Faça o login para continuar.")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    st.checkbox("Lembrar-me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.session_state.etapa = "upload"
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# 👉 Página 2: Upload e Link
def pagina_upload():
    st.title("Página 2 - Upload e Link da Reunião")
    st.markdown("Adicione seu currículo ou anexo (PDF, DOCX, TXT)")

    arquivo = st.file_uploader("Currículo:", type=["pdf", "docx", "txt"])
    link = st.text_input("Link da reunião:")

    if st.button("Confirmar e entrar na reunião"):
        st.session_state.curriculo_nome = arquivo.name if arquivo else "Nenhum arquivo"
        st.session_state.reuniao_link = link
        st.session_state.etapa = "simulacao"

    if st.button("Voltar ao login"):
        st.session_state.etapa = "login"

# 👉 Página 3: Simulação
def pagina_simulacao():
    st.title("Página 3 - Simulação de Entrevista")
    st.write(f"**Currículo recebido:** {st.session_state.get('curriculo_nome', 'Nenhum')}")
    st.write(f"**Link da reunião:** [Acessar reunião]({st.session_state.get('reuniao_link', '#')})")

    st.info("Aqui será a simulação da entrevista IA. Personalize conforme desejar!")

    if st.button("Voltar ao upload"):
        st.session_state.etapa = "upload"

    if st.button("Sair"):
        st.session_state.etapa = "login"

# 👉 Execução conforme etapa
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
