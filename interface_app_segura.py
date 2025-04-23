import streamlit as st

# Ocultar barra superior do Streamlit (ícones Share, GitHub, etc)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Navegação entre páginas usando session_state
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

def exibir_login():
    st.markdown('<h2 style="text-align:center;">Entrevista IA</h2>', unsafe_allow_html=True)
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    lembrar = st.checkbox("Remember me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            st.session_state["pagina"] = "upload"
            st.experimental_rerun()
        else:
            st.error("Credenciais inválidas. Tente novamente.")

def exibir_upload():
    st.markdown("## Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link = st.text_input("Adicione o link da reunião")
    if st.button("Confirmar e entrar na reunião"):
        if arquivo and link:
            st.session_state["curriculo_nome"] = arquivo.name
            st.session_state["link_reuniao"] = link
            st.session_state["pagina"] = "entrevista"
            st.experimental_rerun()
        else:
            st.warning("Adicione o currículo e o link da reunião antes de avançar.")
    if st.button("Voltar ao login"):
        st.session_state["pagina"] = "login"
        st.experimental_rerun()

def exibir_entrevista():
    st.markdown("## Página 3 - Simulação de Entrevista")
    curriculo_nome = st.session_state.get("curriculo_nome", "Nenhum arquivo enviado")
    link_reuniao = st.session_state.get("link_reuniao", "Nenhum link")
    st.write(f"**Currículo recebido:** {curriculo_nome}")
    st.write(f"**Link da reunião:** {link_reuniao}")
    st.info("Aqui será a simulação da entrevista IA. (Personalize conforme desejar!)")
    if st.button("Voltar ao upload"):
        st.session_state["pagina"] = "upload"
        st.experimental_rerun()
    if st.button("Sair"):
        st.session_state["pagina"] = "login"
        st.experimental_rerun()

# Roteamento das páginas
if st.session_state["pagina"] == "login":
    exibir_login()
elif st.session_state["pagina"] == "upload":
    exibir_upload()
elif st.session_state["pagina"] == "entrevista":
    exibir_entrevista()
