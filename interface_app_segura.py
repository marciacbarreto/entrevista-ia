
import streamlit as st
import openai
import os
import tempfile
import speech_recognition as sr
from PyPDF2 import PdfReader

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Entrevista IA", layout="centered", initial_sidebar_state="collapsed")

# GERENCIAMENTO DE PÁGINAS (Telas)
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

# TELA 1 – LOGIN
if st.session_state.pagina == "login":
    st.title("🔒 Acesso Restrito")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if email == "marciacbarreto@gmail.com" and senha == "123456":
            st.session_state.pagina = "upload"
            st.rerun()
        else:
            st.error("E-mail ou senha inválidos.")

# TELA 2 – UPLOAD DO CURRÍCULO + LINK DA REUNIÃO
elif st.session_state.pagina == "upload":
    st.title("Entrevista IA – Currículo e Link")
    uploaded_file = st.file_uploader("📎 Envie seu currículo (PDF)", type=["pdf"])
    link_reuniao = st.text_input("🔗 Cole o link da reunião")

    if "curriculo_texto" not in st.session_state:
        st.session_state.curriculo_texto = ""

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        reader = PdfReader(tmp_path)
        texto = " ".join([page.extract_text() or "" for page in reader.pages])
        st.session_state.curriculo_texto = texto
        st.success("✅ Currículo carregado com sucesso.")

    if uploaded_file and link_reuniao:
        if st.button("Avançar"):
            st.session_state.pagina = "entrevista"
            st.rerun()
    else:
        st.info("Envie o currículo e cole o link para continuar.")

# TELA 3 – SIMULAÇÃO DE ENTREVISTA POR VOZ
elif st.session_state.pagina == "entrevista":
    st.title("🎤 Entrevista IA (Simulação ao vivo)")
    st.info("Aguardando pergunta do recrutador... (microfone ativo)")

    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        audio = reconhecedor.listen(fonte, phrase_time_limit=6)

    try:
        pergunta = reconhecedor.recognize_google(audio, language="pt-BR")
        st.success(f"Pergunta captada: {pergunta}")

        openai.api_key = os.getenv("OPENAI_API_KEY")

        prompt = f"""Você está participando de uma entrevista de emprego.

Seu objetivo é responder à pergunta feita pelo recrutador usando como referência o conteúdo do currículo abaixo. Mantenha um tom profissional, confiante, objetivo e claro. Evite respostas vagas ou genéricas. Personalize a resposta com base nas experiências, habilidades e qualificações descritas no currículo.

Currículo:
{st.session_state.curriculo_texto}

Pergunta feita pelo recrutador:
{pergunta}

Instruções:
- Responda diretamente à pergunta com base no currículo.
- Use um tom natural e seguro, como se estivesse em uma entrevista real.
- Se a pergunta for pessoal ou comportamental, destaque conquistas, experiências ou atitudes que reforcem sua adequação à vaga.
- Se a pergunta for técnica, destaque experiências práticas, projetos, certificações ou conhecimentos adquiridos.

Importante:
- NÃO invente informações.
- NÃO cite nomes de empresas que não estão no currículo.
- NÃO diga que "não sabe" — use o que tiver no currículo para construir a melhor resposta possível.

Agora, gere a resposta ideal para o recrutador com base nas informações acima."""

        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um candidato em uma entrevista de emprego. Responda com objetividade, clareza e profissionalismo."},
                {"role": "user", "content": prompt}
            ]
        )

        resposta_texto = resposta['choices'][0]['message']['content']
        st.subheader("💬 Resposta da IA")
        st.write(resposta_texto)

    except sr.UnknownValueError:
        st.warning("Não foi possível entender a pergunta. Por favor, fale novamente.")
    except sr.RequestError as e:
        st.error(f"Erro na API de reconhecimento de voz: {e}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
