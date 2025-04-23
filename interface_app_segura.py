import streamlit as st

# Ocultar barra lateral, menu e rodapé do Streamlit
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {padding-top: 3rem;}
    </style>
""", unsafe_allow_html=True)

def main():
    # Gerenciar qual página está ativa
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'upload':
        show_upload()
    elif st.session_state.page == 'entrevista':
        show_entrevista()

def show_login():
    st.markdown("## Entrevista IA")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.session_state.page = 'upload'
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def show_upload():
    st.markdown("## Página 2 - Upload e Link da Reunião")
    arquivo = st.file_uploader("Adicione seu currículo ou anexo", type=["pdf", "docx", "txt"])
    link = st.text_input("Adicione o link da reunião")
    if st.button("Confirmar e entrar na reunião"):
        if arquivo is not None and link.strip() != "":
            st.session_state.curriculo = arquivo.name
            st.session_state.link_reuniao = link
            st.session_state.page = 'entrevista'
            st.experimental_rerun()
        else:
            st.warning("Adicione o currículo e o link da reunião.")
    if st.button("Voltar ao login"):
        st.session_state.page = 'login'
        st.experimental_rerun()

def show_entrevista():
    st.markdown("## Página 3 - Simulação de Entrevista")
    st.write(f"**Currículo recebido:** {st.session_state.get('curriculo','')}")
    st.write(f"**Link da reunião:** {st.session_state.get('link_reuniao','')}")
    st.info("Aqui será a simulação da entrevista IA. (Personalize conforme desejar!)")
    if st.button("Voltar ao upload"):
        st.session_state.page = 'upload'
        st.experimental_rerun()
    if st.button("Sair"):
        st.session_state.page = 'login'
        st.experimental_rerun()

if __name__ == "__main__":
    main()
