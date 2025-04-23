import streamlit as st
from pathlib import Path

# Ocultar barra superior e rodapé do Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Função para navegação entre páginas
def redirecionar_para(pagina):
    st.experimental_set_query_params(pagina=pagina)
    st.experimental_rerun()

# Página 1 - Login
def exibir_login():
    st.markdown('<div style="display:flex; flex-direction:column; align-items:center;">', unsafe_allow_html=True)
    st.markdown("<h2>Entrevista IA</h2>", unsafe_allow_html=True)
    email = st.text_input("Email ID")
    senha = st.text_input("Password", type="password")
    lembrar = st.checkbox("Remember me")
    if st.button("LOGIN"):
        if email == "admin@entrevista.com" and senha == "123456":
            st.success("Login realizado com sucesso!")
            redirecionar_para("upload")
        else:
            st.error("Credenciais inválidas. Tente novamente.")
    st.markdown('</div>', unsafe_allow_html=True)

# Página 2 - Upload do currículo e link da reunião
def exibir_upload():
    st.markdown("<h2>Página 2 - Upload e Link da Reunião</h2>", unsafe_allow_html=True)
    st.markdown("📎 Adicione seu currículo ou anexo")
    arquivo = st.file_uploader("Drag and drop file here", type=["pdf", "docx", "txt"])
    if arquivo is not None:
        st.success(f"Arquivo {arquivo.name} carregado com sucesso!")

    st.markdown("🔗 Adicione o link da reunião")
    link_reuniao = st.text_input("Cole o link da reunião aqui")
    
    if st.button("Confirmar e entrar na reunião"):
        if arquivo and link_reuniao:
            st.session_state["curriculo"] = arquivo.name
            st.session_state["link"] = link_reuniao
            redirecionar_para("entrevista")
        else:
            st.warning("Por favor, faça upload do currículo e adicione o link da reunião.")
    if st.button("Voltar ao login"):
        redirecionar_para("login")

# Página 3 - Simulação da entrevista
def exibir_entrevista():
    st.markdown("<h2>Simulação de Entrevista</h2>", unsafe_allow_html=True)
    st.write("Currículo recebido:", st.session_state.get("curriculo", "(não informado)"))
    st.write("Link da reunião:", st.session_state.get("link", "(não informado)"))
    st.markdown("""
    <b>A entrevista será iniciada agora.</b>  
    Mantenha a postura e boa sorte!  
    (Aqui você pode colocar uma simulação ou instruções interativas)
    """, unsafe_allow_html=True)
    if st.button("Finalizar"):
        redirecionar_para("login")

# Controlador de páginas
param = st.experimental_get_query_params()
pagina = param.get("pagina", ["login"])[0]

if pagina == "login":
    exibir_login()
elif pagina == "upload":
    exibir_upload()
elif pagina == "entrevista":
    exibir_entrevista()
