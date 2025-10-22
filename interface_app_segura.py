import os
import re
from pypdf import PdfReader
import docx
import streamlit as st
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==============================
# CONFIGURAÇÃO VISUAL E FIXES
# ==============================
st.set_page_config(page_title="Entrevista IA — Turbo Local", layout="centered")

# CSS anti-bug visual (removeChild)
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { animation: none !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;'>Entrevista IA — Turbo Local (sem API)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>1️⃣ Envie seu currículo | 2️⃣ Cole/Anexe a vaga | 3️⃣ Pergunte (voz ou texto)</p>", unsafe_allow_html=True)

# ==============================
# FUNÇÕES PRINCIPAIS
# ==============================
def extrair_texto_arquivo(uploaded_file) -> str:
    """Extrai texto de PDF (pypdf), DOCX (python-docx) ou TXT."""
    if not uploaded_file:
        return ""
    nome = uploaded_file.name.lower()
    try:
        if nome.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            partes = []
            for page in reader.pages:
                partes.append(page.extract_text() or "")
            return "\n".join(partes)
        elif nome.endswith(".docx"):
            d = docx.Document(uploaded_file)
            return "\n".join(p.text for p in d.paragraphs)
        elif nome.endswith(".txt"):
            data = uploaded_file.read()
            return data.decode("utf-8", errors="ignore")
        else:
            return ""
    except Exception as e:
        st.error(f"Erro ao ler {nome}: {e}")
        return ""

def sent_tokenize(texto: str) -> List[str]:
    """Divide texto em frases simples."""
    if not texto:
        return []
    partes = re.split(r"(?<=[\.\!\?])\s+", texto.strip())
    return [s.strip() for s in partes if s.strip()]

def selecionar_trechos(pergunta: str, *textos: str, limite_chars: int = 1200) -> str:
    """Seleciona trechos mais relevantes com TF-IDF + cosseno."""
    corpus = []
    for t in textos:
        if not t:
            continue
        for s in sent_tokenize(t):
            if 25 <= len(s) <= 300:
                corpus.append(s)
    if not corpus:
        return (" ".join(textos))[:limite_chars]
    try:
        vec = TfidfVectorizer().fit_transform([pergunta] + corpus)
        sims = cosine_similarity(vec[0:1], vec[1:]).ravel()
        idx = sims.argsort()[::-1][:20]
        escolhidas = [corpus[i] for i in idx]
        return " ".join(escolhidas)[:limite_chars]
    except Exception:
        return (" ".join(textos))[:limite_chars]

def montar_resposta(pergunta: str, cv_ctx: str, vaga_ctx: str) -> str:
    """Monta resposta curta e direta em 2–5 frases."""
    intro = f'Sobre "{pergunta}": '
    p1 = "Tenho experiência direta nas atividades e foco em resultados."
    if cv_ctx:
        p1 += " Do meu currículo, destaco: " + cv_ctx[:250]
    p2 = " Em relação à vaga, vejo forte alinhamento com as responsabilidades e requisitos."
    if vaga_ctx:
        p2 += " Pontos de aderência: " + vaga_ctx[:220]
    p3 = " Posso começar contribuindo rapidamente, com organização e comunicação clara."
    return f"{intro}{p1}{p2}{p3}"

# ==============================
# INTERFACE PRINCIPAL
# ==============================
col1, col2 = st.columns(2)
with col1:
    cv_file = st.file_uploader("📎 Currículo (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="cv_uploader")
with col2:
    vaga_file = st.file_uploader("🏢 Vaga/Empresa (PDF/DOCX/TXT) — opcional", type=["pdf", "docx", "txt"], key="vaga_uploader")

vaga_texto = st.text_area("💼 Cole a descrição da vaga (opcional se anexou arquivo)", height=120)

texto_cv = extrair_texto_arquivo(cv_file) if cv_file else ""
texto_vaga = (extrair_texto_arquivo(vaga_file) if vaga_file else "") or vaga_texto

if not cv_file:
    st.info("📄 Envie o currículo para ativar a simulação.")

st.markdown("---")
st.subheader("🎙️ Pergunta do recrutador (voz ou texto)")

# Microfone opcional (não bloqueia o app se indisponível)
try:
    from st_mic_recorder import mic_recorder
    a = mic_recorder(
        start_prompt="🎤 Gravar pergunta",
        stop_prompt="⏹️ Parar gravação",
        use_container_width=True,
        just_once=True,
        format="wav",
    )
    if a and isinstance(a, dict) and a.get("bytes"):
        st.info("🎧 Áudio detectado. Digite/cole abaixo a pergunta transcrita (esta versão é 100% local).")
except Exception:
    st.caption("🎤 Microfone indisponível — use a entrada por texto.")

pergunta = st.text_input("❓ Digite a pergunta do recrutador", placeholder="Ex.: O que você fazia na empresa?")

# ==============================
# PIPELINE LOCAL (instantâneo)
# ==============================
if texto_cv and pergunta:
    with st.spinner("Gerando resposta (local)..."):
        cv_ctx = selecionar_trechos(pergunta, texto_cv)
        vaga_ctx = selecionar_trechos(pergunta, texto_vaga)
        resposta = montar_resposta(pergunta, cv_ctx, vaga_ctx)

    st.success("Resposta sugerida (somente você vê):")
    st.write(resposta)
    st.caption("Dica: leia pausadamente. Faça uma nova pergunta para outra resposta.")

# Limpa caches ao final (evita conflitos de renderização no Streamlit Cloud)
st.cache_data.clear()
st.cache_resource.clear()
