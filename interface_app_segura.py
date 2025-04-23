import streamlit as st

# Gerenciador de páginas
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"
if "curriculo_nome" not in st.session_state:
    st.session_state["curriculo_nome"] = ""
if "link_reuniao" not in st.session_state:
    st.session_state["link_reuniao"] = ""

def login_page():
    st.title("Entrevista IA")
    st.write("Faça o login para continuar.")
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")
    lembrar = st.checkbox("Lembrar-me")

    if st.button("LOGIN"):
        # Simples login fixo
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state["pagina"] = "upload"
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def upload_page():
    st.title("Página 2 - Upload e Link da Reunião")
    st.write("Adicione seu currículo ou anexo (PDF, DOCX, TXT)")
    curriculo = st.file_uploader("Currículo:", type=["pdf", "docx", "txt"], key="upload_curriculo")
    link = st.text_input("Adicione o link da reunião:", key="link_reuniao")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Confirmar e entrar na reunião"):
            if curriculo is not None and link:
                st.session_state["curriculo_nome"] = curriculo.name
                st.session_state["link_reuniao"] = link
                st.session_state["pagina"] = "simulacao"
                st.experimental_rerun()
            else:
                st.error("Anexe o currículo e informe o link da reunião.")
    with col2:
        if st.button("Voltar ao login"):
            st.session_state["pagina"] = "login"
            st.experimental_rerun()

def simulacao_page():
    st.title("Página 3 - Simulação de Entrevista")
    st.markdown(f"**Currículo recebido:** {st.session_state['curriculo_nome']}")
    st.markdown(f"**Link da reunião:** {st.session_state['link_reuniao']}")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Entrar na reunião"):
            st.markdown(f"[Clique aqui para acessar a reunião]({st.session_state['link_reuniao']})", unsafe_allow_html=True)
    with col2:
        if st.button("Voltar ao upload"):
            st.session_state["pagina"] = "upload"
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("Simulação da entrevista IA")
    st.info("Aqui será exibida a simulação da entrevista IA (em breve).")

# --- Fluxo de navegação entre páginas ---
if st.session_state["pagina"] == "login":
    login_page()
elif st.session_state["pagina"] == "upload":
    upload_page()
elif st.session_state["pagina"] == "simulacao":
    simulacao_page()
