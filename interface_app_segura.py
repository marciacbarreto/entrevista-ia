from pathlib import Path

codigo_corrigido = '''
import streamlit as st

# Título fixo
st.set_page_config(page_title="Entrevista IA", layout="centered")

# Inicia a sessão
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"

# Função da página de login
def pagina_login():
    st.title("Entrevista IA")
    st.subheader("Faça o login para continuar.")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    lembrar = st.checkbox("Lembrar-me")

    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state.etapa = "upload"
        else:
            st.error("Credenciais inválidas. Tente novamente.")

# Função da página de upload
def pagina_upload():
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

# Função da página de simulação
def pagina_simulacao():
    st.title("Página 3 - Simulação de Entrevista")
    st.markdown(f"**Currículo recebido:** {st.session_state.curriculo_nome}")
    st.markdown(f"**Link da reunião:** [Acessar reunião]({st.session_state.link_reuniao})")
    st.info("Aqui será a simulação da entrevista IA. Personalize conforme desejar!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar ao upload"):
            st.session_state.etapa = "upload"
    with col2:
        if st.button("Sair"):
            st.session_state.etapa = "login"

# Execução com base na etapa
if st.session_state.etapa == "login":
    pagina_login()
elif st.session_state.etapa == "upload":
    pagina_upload()
elif st.session_state.etapa == "simulacao":
    pagina_simulacao()
'''

# Salvar como arquivo pronto para colar no GitHub
caminho = "/mnt/data/interface_app_segura.py"
Path(caminho).write_text(codigo_corrigido, encoding="utf-8")

caminho
