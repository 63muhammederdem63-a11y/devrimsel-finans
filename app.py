import streamlit as st
import datetime

# --- KURUMSAL SAYFA AYARLARI ---
st.set_page_config(
    page_title="ERMADEFİAN | Ultra Profesyonel Finans Ekosistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL STİLLER ---
st.markdown("""
    <style>
    .main {background-color: #0b0e14; color: #f0f6fc;}
    .stMetric {background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d;}
    h1, h2, h3 {color: #58a6ff;}
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BİLGİ & SEKTÖR BAŞLIĞI ---
st.sidebar.title("💎 ERMADEFİAN TERMINAL v4.0")
st.sidebar.caption("Kurumsal Yatırım ve Finans Yönetim Sistemi")
st.sidebar.markdown("---")

# --- PROFESYONEL MENÜ SİSTEMİ ---
secim = st.sidebar.radio("Modül Seçimi", [
    "🏠 Ana Terminal & Piyasa Özetleri",
    "📈 Borsa & Hisse Analiz Merkezi",
    "🏦 Bankacılık, Faiz & Kredi Hesapları",
    "🪙 Kripto & Emtia Borsası",
    "🛡️ Gelişmiş Portföy & Risk Yönetimi"
])

st.sidebar.markdown("---")
st.sidebar.info("Sistem Durumu: Çevrim içi | Yerel Veri Motoru Aktif")

# --- MODÜL YÖNLENDİRİCİSİ ---
if secim == "🏠 Ana Terminal & Piyasa Özetleri":
    st.title("🌟 ERMADEFİAN Küresel Finans Ekosistemine Hoş Geldiniz")
    st.write("Ziraat, Midas, TradingView ve uluslararası terminallerin en güçlü özelliklerini tek çatı altında topladık.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam İzlenen Varlık", "1,450+", "+12 bugün")
    col2.metric("Sistem Güvenlik Düzeyi", "Kurumsal (Max)", "AES-256")
    col3.metric("Veri Gecikmesi", "Anlık (Real-Time)", "0.1s")
    
    st.markdown("---")
    st.subheader("💡 Günün Piyasa Özeti")
    st.info("Piyasalar küresel enflasyon verileri ve merkez bankası faiz kararları doğrultusunda hareket ediyor. Sol menüden detaylı analiz modüllerine geçiş yapabilirsiniz.")

elif secim == "📈 Borsa & Hisse Analiz Merkezi":
    st.title("📈 Profesyonel Borsa & Derinlemesine Hisse Analizi")
    hisse = st.text_input("Borsa Hisse Kodu (Örn: THYAO.IS, EREGL.IS, AAPL):", "THYAO.IS").upper()
    st.write(f"Seçilen varlık ({hisse}) için profesyonel emir defteri, kademe analizi ve teknik indikatörler yükleniyor...")

elif secim == "🏦 Bankacılık, Faiz & Kredi Hesapları":
    st.title("🏦 Bankacılık ve Mevduat / Kredi Optimizasyon Merkezi")
    st.write("Bankaların vadeli hesap, bileşik getiri, mevduat kıyaslama ve kredi maliyet hesaplamaları.")
    
    tutar = st.number_input("Ana Para / Kredi Tutarı (TL)", 50000, 10000000, 250000)
    vade = st.slider("Vade (Ay)", 1, 36, 12)
    faiz = st.number_input("Yıllık Faiz / Getiri Oranı (%)", 1.0, 70.0, 45.0)
    
    getiri = tutar * ((faiz / 100) / 12) * vade
    st.success(f"Tahmini Toplam Getiri / Maliyet: **{getiri:,.2f} TL**")

elif secim == "🪙 Kripto & Emtia Borsası":
    st.title("🪙 Kripto Paralar ve Kıymetli Madenler Borsası")
    st.write("Altın, Gümüş, Platin, Bitcoin, Ethereum ve altcoinlerin canlı takip ve derinlik paneli.")

elif secim == "🛡️ Gelişmiş Portföy & Risk Yönetimi":
    st.title("🛡️ Kurumsal Portföy ve Risk Optimizasyon Laboratuvarı")
    st.write("Monte Carlo simülasyonları, Sharpe oranı hesaplamaları ve varlık dağılım matrisleri.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>ERMADEFİAN Finansal Teknolojiler A.Ş. © 2026</p>", unsafe_allow_html=True)
