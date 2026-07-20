import streamlit as st
import sys
import os

# Modül yollarını sisteme entegre etme
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
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
    import streamlit as str
import yfinance as yf
import requests
import json

str.title("Devrimsel Finans ve Analiz Platformu")
str.write("Yerel Llama 3 ile Gerçek Zamanlı Yapay Zeka Analizi")

# Kullanıcıdan hisse senedi kodu alma
hisse = str.text_input("Analiz edilecek hisse kodunu girin (Örn: AAPL, TSLA, THYAO.IS):", "AAPL")

if str.button("Verileri Çek ve Analiz Et"):
    # 1. Finansal Verileri Çekme
    str.info(f"{hisse} için güncel veriler çekiliyor...")
    data = yf.Ticker(hisse)
    hist = data.history(period="7d")
    
    if not hist.empty:
        kapanis = hist['Close'].iloc[-1]
        str.success(f"Güncel Kapanış Fiyatı: ${kapanis:.2f}")
        str.line_chart(hist['Close'])
        
        # 2. Yapay Zekaya Gönderilecek Soruyu Hazırlama
        prompt = f"{hisse} kodlu hissenin son 7 günlük kapanış fiyatları sırasıyla şöyledir: {list(hist['Close'].round(2))}. Bu verilere göre teknik bir analiz yap ve kısa bir yatırım tavsiyesi içermeyen yorum üret."
        
        # 3. Yerel Llama 3'e İstek Atma
        str.info("Yerel Llama 3 yapay zeka analizi yapıyor...")
        url = "http://localhost:11434/api/generate"
        payload = {"model": "llama3", "prompt": prompt, "stream": False}
        
        try:
            response = requests.post(url, json=payload)
            analiz = response.json().get("response", "Analiz alınamadı.")
            str.subheader("Yapay Zeka Analiz Raporu")
            str.write(analiz)
        except Exception as e:
            str.error(f"Ollama bağlantı hatası: {e}. Arka planda Ollama uygulamasının açık olduğundan emin olun.")
    else:
        str.error("Hisse verisi bulunamadı. Kodu doğru girdiğinizden emin olun.")
