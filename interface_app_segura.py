import os
import io
import tempfile
import fitz  # PyMuPDF
import docx
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAI, RateLimitError

# ==========================
# Configuração inicial
# ==========================
st.set_page_config(page_title="Entrevista IA", layout="centered")
st.markdown("<h1 style='text-align: center;'>Entrevista IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>1️⃣ Envie seu currículo | 2️⃣ Cole/Anexe a vaga | 3️⃣ Faça a pergunta por voz ou texto</p>", unsafe_allow_html=True)

# ==========================
# Cliente OpenAI (aceita duas variáveis de ambiente)
# ==========================
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("ABRIR_CHAVE_API")
if not OPENAI_KEY:
    st.warning("⚠️ Defina a variável OPENAI_API_KEY (ou ABRIR_CHAVE_API) nos Secrets para funcionar.")
client = OpenAI(api_key=OPENAI_KEY)

# Modelos
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")        # leve/rápido
ASR_MODEL = os.getenv("ASR_MODEL", "whisper-1")          # transcrição

# ==========================
# Funções utilitárias
# ==========================

def extrair_texto_arquivo(uploaded_file) -> str:
    """Extrai texto de PDF ou DOCX (currículo ou vaga)."""
    if not uploaded_file:
        return ""
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".pdf"):
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                return "\n".join(p.get_text() for p in doc)
        elif name.endswith(".docx"):
            d = docx.Document(uploaded_file)
            return "\n".join(p.text for p in d.paragraphs)
        else:
            # fallback texto puro
            data = uploaded_file.read()
            try:
                return data.decode("utf-8", errors="ignore")
            except Exception:
                return str(data)
    except Exception as e:
        st.error(f"Erro ao ler {name}: {type(e).__name__}")
        return ""

# Trava anti-duplicação

def is_busy():
    return st.session_state.get("llm_busy", False)

def set_busy(v: bool):
    st.session_state["llm_busy"] = v

# Retry/backoff para 429
@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception_type(RateLimitError),
)
def call_llm(system_prompt: str, user_prompt: str) -> str:
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=350,
        top_p=1,
    )
    return resp.choices[0].message.content.strip()


def responder(pergunta_txt: str, contexto_cv: str, contexto_vaga: str) -> str | None:
    if not pergunta_txt or not pergunta_txt.strip():
        return None

    # Debounce: evita repetir mesma pergunta no rerun
    last_q = st.session_state.get("last_q")
    if last_q and pergunta_txt.strip() == last_q.strip():
        return st.session_state.get("last_answer")

    if is_busy():
        return st.session_state.get("last_answer")

    set_busy(True)
    try:
        system = (
            "Você é um assistente de entrevistas. Responda como se fosse o candidato, em primeira pessoa, "
            "de forma breve (2 a 5 frases), clara e confiante, sempre baseado no currículo e na vaga. "
            "Não produza áudio, apenas texto objetivo."
        )
        user = (
            f"PERGUNTA DO RECRUTADOR: {pergunta_txt}\n\n"
            f"CURRÍCULO (trechos relevantes):\n{contexto_cv}\n\n"
            f"VAGA/EMPRESA (trechos relevantes):\n{contexto_vaga}\n\n"
            "Monte uma resposta direta, com foco em resultados, habilidades e aderência à vaga."
        )
        resposta = call_llm(system, user)
        st.session_state["last_q"] = pergunta_txt
        st.session_state["last_answer"] = resposta
        return resposta
    finally:
        set_busy(False)


def transcrever_audio_bytes(audio_bytes: bytes, suffix: str = ".wav") -> str:
    """Envia bytes de áudio para o Whisper (ASR_MODEL) e retorna texto."""
    if not audio_bytes:
        return ""
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        tmp_name = tmp.name
    with open(tmp_name, "rb") as f:
        tr = client.audio.transcriptions.create(model=ASR_MODEL, file=f)
    return tr.text.strip() if hasattr(tr, "text") else (tr.get("text", "") if isinstance(tr, dict) else "")


# ==========================
# Layout principal
# ==========================
col1, col2 = st.columns(2)
with col1:
    cv_file = st.file_uploader("📎 Currículo (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="cv")
with col2:
    vaga_file = st.file_uploader("🏢 Vaga/Empresa (PDF/DOCX/TXT) — opcional", type=["pdf", "docx", "txt"], key="vaga_file")

vaga_texto = st.text_area("💼 Cole a descrição da vaga (opcional se anexou arquivo)", height=120)

# Extrai textos
texto_cv = extrair_texto_arquivo(cv_file) if cv_file else ""
texto_vaga = (extrair_texto_arquivo(vaga_file) if vaga_file else "") or vaga_texto

if not cv_file:
    st.info("📄 Envie o currículo para ativar a simulação.")

# ==========================
# Entrada por voz (microfone) + fallback por texto
# ==========================
st.markdown("---")
st.subheader("🎙️ Pergunta do recrutador (voz) ou digite abaixo")

# Tentativa com st-mic-recorder, mas mantendo o app estável mesmo sem a lib
audio_bytes = None
try:
    from st_mic_recorder import mic_recorder
    audio = mic_recorder(
        start_prompt="Clique para começar a escutar",
        stop_prompt="Parar",
        use_container_width=True,
        just_once=True,
        format="wav",
    )
    if audio and isinstance(audio, dict):
        audio_bytes = audio.get("bytes")
except Exception:
    st.caption("🎤 st-mic-recorder não disponível — usando apenas entrada por texto.")

# Fallback texto
pergunta_digitada = st.text_input("❓ Ou digite a pergunta do recrutador", placeholder="Ex.: Quais seus pontos fortes para esta vaga?")

# ==========================
# Gatilho: quando houver áudio final OU pergunta digitada nova
# ==========================
resposta_gerada = None

if cv_file:
    # Se veio áudio, transcreve e responde
    if audio_bytes:
        with st.spinner("Transcrevendo áudio..."):
            pergunta_transcrita = transcrever_audio_bytes(audio_bytes, suffix=".wav")
        if pergunta_transcrita:
            with st.spinner("Gerando resposta..."):
                resposta_gerada = responder(pergunta_transcrita, texto_cv, texto_vaga)
    # Se veio texto digitado
    elif pergunta_digitada:
        with st.spinner("Gerando resposta..."):
            resposta_gerada = responder(pergunta_digitada, texto_cv, texto_vaga)

# ==========================
# Saída em texto (somente você vê)
# ==========================
if resposta_gerada:
    st.success("Resposta sugerida (somente você vê):")
    st.write(resposta_gerada)
    st.caption("Dica: leia pausadamente. Se quiser refinar, faça nova pergunta por voz ou texto.")
