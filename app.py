import streamlit as st
import sys
import os

# Python'un modül yolunu bulmasını garanti altına al
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from modules.borsa import borsa_analiz_ekrani
from modules.banka_finans import banka_finans_ekrani
from modules.risk_simulasyon import risk_simulasyon_ekrani

st.set_page_config(
    page_title="ERMADEFİAN | Kurumsal Finans Ekosistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {background-color: #0b0e14; color: #f0f6fc;}
    .stMetric {background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d;}
    h1, h2, h3 {color: #58a6ff;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("💎 ERMADEFİAN TERMINAL")
st.sidebar.caption("Modüler Kurumsal Finans Sistemi")
st.sidebar.markdown("---")

modul = st.sidebar.radio("Modül Seçimi", [
    "📈 Borsa & Hisse Analiz Merkezi",
    "🏦 Bankacılık & Mevduat Optimizasyonu",
    "🛡️ Algoritmik Risk & Portföy"
])

st.sidebar.markdown("---")
st.sidebar.info("Modüler Mimari Tam Aktif v5.0")

if modul == "📈 Borsa & Hisse Analiz Merkezi":
    borsa_analiz_ekrani()
elif modul == "🏦 Bankacılık & Mevduat Optimizasyonu":
    banka_finans_ekrani()
elif modul == "🛡️ Algoritmik Risk & Portföy":
    risk_simulasyon_ekrani()
