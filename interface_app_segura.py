import os
import re
import tempfile
import fitz  # PyMuPDF
import docx
import streamlit as st
from typing import List, Tuple

# ===== Pacotes para busca web e extração de conteúdo =====
# (IA gratuita via web — sem OpenAI)
from tavily import TavilyClient
import trafilatura
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================
# Configuração inicial
# ==========================
st.set_page_config(page_title="Entrevista IA (Web AI)", layout="centered")
st.markdown("<h1 style='text-align: center;'>Entrevista IA — IA gratuita via Web</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>1️⃣ Envie seu currículo | 2️⃣ Cole/Anexe a vaga | 3️⃣ Pergunte (texto ou voz*)</p>", unsafe_allow_html=True)
st.caption("*Voz opcional. Se o microfone não estiver disponível, use o campo de texto.")

# ==========================
# Chaves/Config (somente Tavily, grátis)
# ==========================
TAVILY_KEY = (
    st.secrets.get("TAVILY_API_KEY") if hasattr(st, "secrets") else None
) or os.getenv("TAVILY_API_KEY")

if not TAVILY_KEY:
    st.warning(
        "⚠️ Defina a chave gratuita do Tavily em Settings → Secrets → `TAVILY_API_KEY = \"tvly_...\"` para habilitar a busca na web."
    )

# ==========================
# Utilitários de arquivo
# ==========================

def extrair_texto_arquivo(uploaded_file) -> str:
    """Extrai texto de PDF/DOCX/TXT."""
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
        elif name.endswith(".txt"):
            data = uploaded_file.read()
            try:
                return data.decode("utf-8", errors="ignore")
            except Exception:
                return str(data)
        else:
            return ""
    except Exception as e:
        st.error(f"Erro ao ler {name}: {type(e).__name__}")
        return ""

# ==========================
# Busca na Web (Tavily) + coleta de conteúdo (Trafilatura)
# ==========================

@st.cache_data(show_spinner=False, ttl=600)
def tavily_search(query: str, max_results: int = 5) -> List[dict]:
    if not TAVILY_KEY:
        return []
    try:
        client = TavilyClient(api_key=TAVILY_KEY)
        res = client.search(query=query, max_results=max_results, include_raw_content=False)
        return res.get("results", [])
    except Exception:
        return []

@st.cache_data(show_spinner=False, ttl=600)
def baixar_texto_url(url: str, max_chars: int = 12000) -> str:
    try:
        dl = trafilatura.fetch_url(url, timeout=10)
        txt = trafilatura.extract(dl) if dl else ""
        return (txt or "")[:max_chars]
    except Exception:
        return ""

# ==========================
# Extração de empresa/cargo da vaga (heurístico)
# ==========================

def guess_company_and_role(vaga_txt: str) -> Tuple[str, str]:
    empresa, cargo = "", ""
    if not vaga_txt:
        return empresa, cargo
    m = re.search(r"(?i)empresa[:\s-]+([\w .&-]{2,80})", vaga_txt)
    if m:
        empresa = m.group(1).strip()
    m2 = re.search(r"(?i)cargo[:\s-]+([\w .&/-]{2,80})", vaga_txt)
    if m2:
        cargo = m2.group(1).strip()
    # fallback simples
    if not cargo:
        m3 = re.search(r"(?i)vaga[:\s-]+([\w .&/-]{2,80})", vaga_txt)
        cargo = m3.group(1).strip() if m3 else cargo
    return empresa, cargo

# ==========================
# Resumo simples (extrativo) e seleção por relevância
# ==========================

def sent_tokenize(texto: str) -> List[str]:
    # separa por ponto/interrogação/exclamação de forma simples
    partes = re.split(r"(?<=[\.!?])\s+", texto.strip())
    return [s.strip() for s in partes if len(s.strip()) > 0]

@st.cache_data(show_spinner=False, ttl=600)
def resumo_extrativo(texto: str, max_sent: int = 6) -> str:
    if not texto:
        return ""
