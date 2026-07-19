import streamlit as st
import yfinance as yf
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="ERMADEFİAN Terminal", layout="wide")

# Sidebar - Menü
st.sidebar.title("ERMADEFİAN Kontrol")
menu = st.sidebar.radio("Modül Seçin", ["Hisse Analizi", "Döviz Kurları", "Portföy Risk Hesaplayıcı"])

# --- HİSSE ANALİZİ MODÜLÜ ---
if menu == "Hisse Analizi":
    st.title("📊 Profesyonel Hisse Senedi Analizi")
    hisse_kodu = st.text_input("Hisse Kodu (Örn: THYAO.IS):", "THYAO.IS")
    
    if st.button("Analiz Et"):
        try:
            hisse = yf.Ticker(hisse_kodu)
            df = hisse.history(period="6mo")
            info = hisse.info
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Fiyat", f"{df['Close'].iloc[-1]:.2f}")
            col2.metric("Piyasa Değeri", f"{info.get('marketCap', 0)/1000000000:.2f} Milyar")
            col3.metric("52 Hafta Zirve", f"{info.get('fiftyTwoWeekHigh', 0):.2f}")
            
            # Göstergeler
            df['MA20'] = df['Close'].rolling(20).mean()
            st.line_chart(df[['Close', 'MA20']])
            
            st.write("### Temel Veriler")
            st.json({"Sektör": info.get('sector'), "F/K Oranı": info.get('trailingPE')})
        except:
            st.error("Veri alınamadı, kodu kontrol edin.")

# --- DÖVİZ KURLARI MODÜLÜ ---
elif menu == "Döviz Kurları":
    st.title("💱 Canlı Döviz Takibi")
    kurlar = ['USDTRY=X', 'EURTRY=X', 'GBPTRY=X']
    for kod in kurlar:
        kur = yf.Ticker(kod)
        data = kur.history(period="1d")
        fiyat = data['Close'].iloc[-1]
        st.info(f"{kod.replace('=X', '')} : {fiyat:.4f} TL")

# --- PORTFÖY RİSK HESAPLAYICI ---
elif menu == "Portföy Risk Hesaplayıcı":
    st.title("🛡️ Portföy Risk Analizi")
    st.write("Yatırım tutarınızı ve risk algınızı girin:")
    tutar = st.number_input("Yatırım Tutarı (TL):", min_value=1000)
    risk_seviyesi = st.slider("Risk Algınız (1: Düşük, 5: Çok Yüksek)", 1, 5)
    
    if st.button("Strateji Önerisi"):
        if risk_seviyesi <= 2:
            st.success("Strateji: %70 Tahvil/Altın, %30 Temettü Hisseleri")
        else:
            st.warning("Strateji: %40 Teknoloji Hisseleri, %30 Kripto, %30 Borsa Yatırım Fonları")

st.sidebar.markdown("---")
st.sidebar.write("ERMADEFİAN v1.0 - Yerel Analiz Sistemi")
