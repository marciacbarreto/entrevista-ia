import streamlit as st

# Configura o layout fixo da página
st.set_page_config(page_title="Entrevista IA", layout="centered")

# Inicializa a etapa da navegação
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"


def pagina_login():
    """Tela inicial de login."""
    st.title("Entrevista IA")
    st.subheader("Faça o login para continuar.")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    st.checkbox("Lembrar-me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state.etapa = "upload"
        else:
            st.error("Credenciais inválidas. Tente novamente.")


def pagina_upload():
    """Tela de envio do currículo e link da reunião."""
    st.title("Página 2 - Upload e Link da Reunião")
    st.markdown("Adicione seu currículo ou anexo (PDF, DOCX, TXT)")

    arquivo = st.file_uploader("Currículo:", type=["pdf", "docx", "txt"])
    link = st.text_input("Adicione o link da reunião:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirmar e entrar na reunião"):
            if arquivo and link:
                st.session_state["curriculo_nome"] = arquivo.name
                st.session_state["link_reuniao"] = link
                st.session_state.etapa = "simulacao"
            else:
                st.error("Anexe o currículo e informe o link da reunião.")
    with col2:
        if st.button("Voltar ao login"):
            st.session_state.etapa = "login"


def pagina_simulacao():
    """Página de simulação da entrevista."""
    st.title("Página 3 - Simulação de Entrevista")

    curriculo = st.session_state.get("curriculo_nome", "Não informado")
    link = st.session_state.get("link_reuniao", "#")

    st.markdown(f"**Currículo recebido:** {curriculo}")
    st.markdown(f"**Link da reunião:** [Acessar reunião]({link})")
    st.info("Aqui será a simulação da entrevista IA. Personalize conforme desejar!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar ao upload"):
            st.session_state.etapa = "upload"
    with col2:
        if st.button("Sair"):
            st.session_state.etapa = "login"


# Execução com base na etapa atual
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
