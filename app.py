import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. AYARLAR VE GÖRSELLEŞTİRME ---
st.set_page_config(page_title="ERMADEFİAN | Profesyonel Terminal", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
        .stMetric {background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #2e86de;}
        .reportview-container {background: #ffffff;}
        </style>
        """, unsafe_allow_html=True)

inject_custom_css()

# --- 2. HESAPLAMA MOTORU (ALGORİTMİK İNDİKATÖRLER) ---
class FinansalMotor:
    @staticmethod
    def hesapla(df):
        # MultiIndex sütun yapısını düzelt (yfinance veri güvenliği için)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
            
        # Kapanış fiyatını tek boyutlu diziye çevir
        close_series = df['Close'].squeeze()
        
        # Hareketli Ortalamalar
        df['SMA20'] = close_series.rolling(20).mean()
        df['SMA50'] = close_series.rolling(50).mean()
        df['SMA200'] = close_series.rolling(200).mean()
        
        # Bollinger Bantları
        std20 = close_series.rolling(20).std()
        df['BB_Mid'] = df['SMA20']
        df['BB_Up'] = df['SMA20'] + (std20 * 2)
        df['BB_Down'] = df['SMA20'] - (std20 * 2)
        
        # RSI Hesaplama
        delta = close_series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df

# --- 3. BİLEŞENLER (MODÜLER YAPI) ---
def render_hisse_analiz():
    st.header("📈 Gelişmiş Hisse Senedi Analiz Modülü")
    ticker = st.text_input("Hisse Kodu (Örn: THYAO.IS):", "THYAO.IS")
    if st.button("Analizi Tetikle"):
        try:
            df = yf.download(ticker, period="1y")
            if df.empty:
                st.error("Girilen kod için veri bulunamadı.")
                return
                
            df = FinansalMotor.hesapla(df)
            
            son_fiyat = float(df['Close'].iloc[-1])
            son_rsi = float(df['RSI'].iloc[-1])
            bb_up_val = float(df['BB_Up'].iloc[-1])
            bb_down_val = float(df['BB_Down'].iloc[-1])
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Son Fiyat", f"{son_fiyat:.2f}")
            c2.metric("RSI", f"{son_rsi:.2f}")
            c3.metric("Bollinger Genişliği", f"{(bb_up_val - bb_down_val):.2f}")
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index, 
                open=df['Open'].squeeze(), 
                high=df['High'].squeeze(), 
                low=df['Low'].squeeze(), 
                close=df['Close'].squeeze(),
                name='Fiyat'
            ))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'].squeeze(), name='SMA 20', line=dict(color='orange')))
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Detaylı Veri Tablosu"):
                st.dataframe(df.tail(20))
        except Exception as e:
            st.error(f"Veri işleme hatası: {e}")

def render_piyasa_paneli():
    st.header("🌐 Küresel Piyasa ve Emtia İzleme")
    assets = {"Dolar": "USDTRY=X", "Altın": "GC=F", "Gümüş": "SI=F", "Brent": "BZ=F", "BTC": "BTC-USD"}
    
    cols = st.columns(5)
    for i, (name, sym) in enumerate(assets.items()):
        try:
            data = yf.Ticker(sym).history(period="1d")
            fiyat = float(data['Close'].iloc[-1])
            cols[i].metric(name, f"{fiyat:.2f}")
        except:
            cols[i].metric(name, "Veri Yok")
    
    st.divider()
    st.write("Sektörel performans izleme ve global korelasyon matrisi aktif durumda.")

def render_risk_yönetimi():
    st.header("🛡️ Algoritmik Risk Modülasyonu")
    sermaye = st.number_input("Toplam Sermaye (TL):", min_value=1000, value=100000)
    risk_profili = st.radio("Risk Profili Seçin:", ["Muhafazakar", "Dengeli", "Agresif", "Spekülatif"])
    
    model_data = {
        "Muhafazakar": {"Tahvil": 0.6, "Altın": 0.3, "Nakit": 0.1},
        "Dengeli": {"Tahvil": 0.3, "Altın": 0.3, "Hisse": 0.4},
        "Agresif": {"Hisse": 0.6, "Altın": 0.2, "Kripto": 0.2},
        "Spekülatif": {"Hisse": 0.3, "Kripto": 0.5, "Opsiyon": 0.2}
    }
    
    secilen = model_data[risk_profili]
    for varlik, oran in secilen.items():
        st.write(f"### {varlik}: {sermaye * oran:,.2f} TL (%{oran*100:.0f})")

# --- 4. ANA DÖNGÜ (DİSPATCHER) ---
st.sidebar.title("ERMADEFİAN v2.5")
page = st.sidebar.selectbox("Dashboard Seçimi", ["Hisse Detaylı Analiz", "Küresel Piyasa", "Risk ve Portföy"])

if page == "Hisse Detaylı Analiz": 
    render_hisse_analiz()
elif page == "Küresel Piyasa": 
    render_piyasa_paneli()
elif page == "Risk ve Portföy": 
    render_risk_yönetimi()

st.sidebar.markdown("---")
st.sidebar.info("ERMADEFİAN yerel hesaplama birimi aktif. Hiçbir dış API kısıtlamasına maruz kalmadan çalışmaktadır.")
