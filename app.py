import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="ERMADEFİAN Pro Terminal", layout="wide")

st.sidebar.title("ERMADEFİAN")
menu = st.sidebar.radio("Modül Seçin", ["Hisse Detaylı Analiz", "Döviz & Emtia Takip", "Risk & Varlık Yönetimi"])

# --- MODÜL 1: HİSSE DETAYLI ANALİZ (Profesyonel Teknik Analiz) ---
if menu == "Hisse Detaylı Analiz":
    st.title("📈 Profesyonel Hisse Senedi Analizi")
    hisse_kodu = st.text_input("Hisse Kodu Girin (Örn: THYAO.IS):", "THYAO.IS")
    
    if st.button("Derin Analiz Başlat"):
        hisse = yf.Ticker(hisse_kodu)
        df = hisse.history(period="1y")
        
        # Teknik İndikatörler (Daha Detaylı)
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Son Fiyat", f"{df['Close'].iloc[-1]:.2f}")
        col2.metric("Günlük Değişim", f"{((df['Close'].iloc[-1]/df['Close'].iloc[-2])-1)*100:.2f}%")
        col3.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.2f}")
        col4.metric("Hacim Ort.", f"{df['Volume'].mean():,.0f}")
        
        st.line_chart(df[['Close', 'MA20', 'MA50']])
        st.write("### 50 Günlük Trend Yorumu:", "Boğa" if df['Close'].iloc[-1] > df['MA50'].iloc[-1] else "Ayı")

# --- MODÜL 2: DÖVİZ & EMTİA TAKİP (Emtia Entegrasyonu) ---
elif menu == "Döviz & Emtia Takip":
    st.title("💱 Canlı Piyasa Verileri")
    assets = {
        "USD/TRY": "USDTRY=X", "EUR/TRY": "EURTRY=X", 
        "Altın (Ons)": "GC=F", "Gümüş (Ons)": "SI=F"
    }
    
    cols = st.columns(len(assets))
    for i, (name, ticker) in enumerate(assets.items()):
        data = yf.Ticker(ticker).history(period="1d")
        fiyat = data['Close'].iloc[-1]
        cols[i].metric(name, f"{fiyat:.2f}")

# --- MODÜL 3: RİSK & VARLIK YÖNETİMİ (Kapsamlı Portföy Modeli) ---
elif menu == "Risk & Varlık Yönetimi":
    st.title("🛡️ Stratejik Portföy Yönetimi")
    tutar = st.number_input("Toplam Sermaye (TL):", 10000)
    risk = st.select_slider("Risk Toleransı:", ["Çok Düşük", "Düşük", "Orta", "Yüksek", "Çok Yüksek"])
    
    if st.button("Portföyü Dağıt"):
        st.write(f"### {risk} Risk için Önerilen Dağılım:")
        if risk == "Orta":
            dagilim = {"Hisse Senetleri": 0.4, "Altın/Emtia": 0.3, "Tahvil/Faiz": 0.3}
        elif risk == "Yüksek":
            dagilim = {"Hisse Senetleri": 0.6, "Altın/Emtia": 0.2, "Kripto/Spekülatif": 0.2}
        else:
            dagilim = {"Tahvil/Faiz": 0.6, "Altın": 0.3, "Nakit": 0.1}
            
        for varlik, oran in dagilim.items():
            st.write(f"- {varlik}: {tutar * oran:,.2f} TL (%{oran*100:.0f})")
