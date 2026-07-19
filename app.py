import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PROFESYONEL AYARLAR ---
st.set_page_config(page_title="ERMADEFİAN | Profesyonel Finans Terminali", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .main {background-color: #f5f7f9;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

# --- SİDEBAR NAVİGASYON ---
st.sidebar.title("ERMADEFİAN Terminal")
page = st.sidebar.radio("Dashboard", ["Gelişmiş Hisse Analizi", "Küresel Piyasa Paneli", "Portföy & Risk Yönetimi"])

# --- GÜÇLÜ ANALİZ MOTORU ---
def get_technical_indicators(df):
    # MA Hesaplamaları
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    
    # RSI Hesaplama
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD Hesaplama
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bantları
    df['BB_Mid'] = df['Close'].rolling(20).mean()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['Close'].rolling(20).std()
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['Close'].rolling(20).std()
    return df

# --- MODÜL 1: HİSSE ANALİZİ ---
if page == "Gelişmiş Hisse Analizi":
    st.title("📈 Profesyonel Hisse Senedi Analiz İstasyonu")
    ticker = st.text_input("Sembol (Örn: THYAO.IS, AAPL):", "THYAO.IS").upper()
    
    if st.button("Verileri Çek ve Analiz Et"):
        try:
            df = yf.download(ticker, period="1y", interval="1d")
            df = get_technical_indicators(df)
            
            # Dashboard Görünümü
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Son Fiyat", f"{df['Close'].iloc[-1]:.2f}")
            c2.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.2f}")
            c3.metric("50 Günlük MA", f"{df['MA50'].iloc[-1]:.2f}")
            c4.metric("200 Günlük MA", f"{df['MA200'].iloc[-1]:.2f}")
            
            # Profesyonel Grafik
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Fiyat'))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20', line=dict(color='orange')))
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("### Teknik Sinyaller")
            signal = "AL" if df['RSI'].iloc[-1] < 30 else ("SAT" if df['RSI'].iloc[-1] > 70 else "BEKLE")
            st.info(f"RSI Değerine Göre Sinyal: **{signal}**")
            
        except Exception as e:
            st.error(f"Hisse verisi çekilemedi: {e}")

# --- MODÜL 2: KÜRESEL PİYASA ---
elif page == "Küresel Piyasa Paneli":
    st.title("🌐 Küresel Piyasa İzleme")
    assets = {"Dolar/TL": "USDTRY=X", "Euro/TL": "EURTRY=X", "Altın (Ons)": "GC=F", "Gümüş": "SI=F", "BIST 100": "^XU100.IS"}
    
    cols = st.columns(3)
    for i, (name, sym) in enumerate(assets.items()):
        data = yf.Ticker(sym).history(period="1d")
        fiyat = data['Close'].iloc[-1]
        cols[i % 3].metric(name, f"{fiyat:.2f}")

# --- MODÜL 3: RİSK YÖNETİMİ ---
elif page == "Portföy & Risk Yönetimi":
    st.title("🛡️ Algoritmik Risk Modülasyonu")
    capital = st.number_input("Sermaye (TL):", 50000)
    risk_level = st.select_slider("Strateji Seviyesi:", ["Muhafazakar", "Dengeli", "Agresif"])
    
    weights = {"Muhafazakar": [0.7, 0.2, 0.1], "Dengeli": [0.4, 0.3, 0.3], "Agresif": [0.2, 0.3, 0.5]}
    w = weights[risk_level]
    
    st.write(f"### {risk_level} Portföy Dağılımı")
    st.write(f"- Tahvil/Faiz: {capital * w[0]:,.2f} TL")
    st.write(f"- Altın/Değerli Metal: {capital * w[1]:,.2f} TL")
    st.write(f"- Hisse/Kripto: {capital * w[2]:,.2f} TL")
    
    st.markdown("---")
    st.write("ERMADEFİAN - Sürüm 2.0 | Yerel İşlem Gücü")
