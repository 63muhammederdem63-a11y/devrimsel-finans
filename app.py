import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- 1. KURUMSAL SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="ERMADEFİAN | Profesyonel Finans Terminali",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PROFESYONEL TERMINAL STİLLERİ (CSS) ---
st.markdown("""
    <style>
    .main {background-color: #0e1117; color: #fafafa;}
    .stMetric {background-color: #161b22; padding: 20px; border-radius: 8px; border: 1px solid #30363d;}
    .stTextInput input {background-color: #161b22; color: white; border: 1px solid #30363d;}
    h1, h2, h3 {color: #58a6ff;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. GÜÇLÜ VERİ VE HESAPLAMA MOTORU ---
@st.cache_data(ttl=300)
def veri_cek_ve_hesapla(ticker_kodu):
    try:
        df = yf.download(ticker_kodu, period="1y", interval="1d", progress=False)
        if df.empty:
            return None
        
        # Çok katmanlı başlık temizliği
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
            
        close = df['Close'].squeeze()
        
        # Teknik İndikatörler
        df['SMA20'] = close.rolling(20).mean()
        df['SMA50'] = close.rolling(50).mean()
        df['SMA200'] = close.rolling(200).mean()
        
        # Bollinger Bantları
        std20 = close.rolling(20).std()
        df['BB_Up'] = df['SMA20'] + (std20 * 2)
        df['BB_Down'] = df['SMA20'] - (std20 * 2)
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    except Exception:
        return None

# --- 4. SOL PANEL: KONTROL VE HİSSE SEÇİM MERKEZİ ---
st.sidebar.title("⚡ ERMADEFİAN TERMINAL")
st.sidebar.markdown("---")

aktif_hisse = st.sidebar.text_input("Ana Varlık / Hisse Kodu", "THYAO.IS").upper()
zaman_dilimi = st.sidebar.selectbox("Veri Periyodu", ["1 Ay", "3 Ay", "6 Ay", "1 Yıl"], index=3)

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Hızlı Araçlar")
kredi_hesapla = st.sidebar.checkbox("Kredi & Taksit Simülatörü Aç")
portfoy_ac = st.sidebar.checkbox("Risk & Varlık Dağılımı Aç")

# --- 5. ANA EKRAN: TEK SAYFA PROFESYONEL DÜZEN ---
st.title("📊 ERMADEFİAN Canlı Finans & Piyasa Ekosistemi")
st.caption(f"Son Güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Mod: Kurumsal Terminal")

# --- BÖLÜM A: CANLI KÜRESEL PİYASA BANTI ---
st.subheader("🌐 Küresel Piyasalar & Emtia Ticker Bandı")
canli_varliklar = {
    "BIST 100": "XU100.IS", "S&P 500": "^GSPC", "Dolar/TL": "USDTRY=X", 
    "Euro/TL": "EURTRY=X", "Altın (Ons)": "GC=F", "Bitcoin": "BTC-USD"
}

cols = st.columns(len(canli_varliklar))
i = 0
for isim, sembol in canli_varliklar.items():
    try:
        t_data = yf.Ticker(sembol).history(period="2d")
        fiyat = float(t_data['Close'].iloc[-1])
        onceki = float(t_data['Close'].iloc[-2])
        fark = ((fiyat - onceki) / onceki) * 100
        cols[i].metric(isim, f"{fiyat:,.2f}", f"{fark:+.2f}%")
    except:
        cols[i].metric(isim, "Veri Akışı Yok", "0.00%")
    i += 1

st.markdown("---")

# --- BÖLÜM B: GELİŞMİŞ GRAFİK VE TEKNİK ANALİZ İSTASYONU ---
st.subheader(f"📈 Derinlemesine Teknik Analiz: {aktif_hisse}")

df = veri_cek_ve_hesapla(aktif_hisse)

if df is not None and not df.empty:
    son_fiyat = float(df['Close'].iloc[-1])
    onceki_fiyat = float(df['Close'].iloc[-2])
    gunluk_fark = ((son_fiyat - onceki_fiyat) / onceki_fiyat) * 100
    rsi_deger = float(df['RSI'].iloc[-1])
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Kapanış Fiyatı", f"{son_fiyat:,.2f}", f"{gunluk_fark:+.2f}%")
    mc2.metric("RSI (14 Güç Endeksi)", f"{rsi_deger:.2f}")
    mc3.metric("20 Günlük Ortalama (SMA)", f"{float(df['SMA20'].iloc[-1]):,.2f}")
    mc4.metric("İşlem Hacmi", f"{float(df['Volume'].iloc[-1]):,.0f}")
    
    # Profesyonel Plotly Candlestick Grafiği (Karanlık Tema Uyumlu)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'].squeeze(),
        high=df['High'].squeeze(),
        low=df['Low'].squeeze(),
        close=df['Close'].squeeze(),
        name='Mum Grafiği'
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'].squeeze(), name='SMA 20', line=dict(color='#ff7f0e', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'].squeeze(), name='SMA 50', line=dict(color='#1f77b4', width=1.5)))
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=10, b=10),
        height=500,
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error(f"'{aktif_hisse'}' sembolü için veri alınamadı. Lütfen geçerli bir borsa kodu girdiğinizden emin olun (Örn: THYAO.IS, GARAN.IS, AAPL).")

st.markdown("---")

# --- BÖLÜM C: İLERİ DÜZEY HESAPLAMA VE RİSK MODÜLLERİ ---
if kredi_hesapla:
    st.subheader("🧮 Profesyonel Kredi & Finansal Maliyet Analizörü")
    kc1, kc2, kc3 = st.columns(3)
    k_tutar = kc1.number_input("Kredi Anapara (TL)", 100000, 10000000, 500000, step=50000)
    k_faiz = kc2.number_input("Aylık Faiz Oranı (%)", 0.1, 10.0, 3.5, step=0.1)
    k_vade = kc3.slider("Vade (Ay)", 3, 120, 36)
    
    oran = k_faiz / 100
    taksit = (k_tutar * oran * ((1 + oran)**k_vade)) / (((1 + oran)**k_vade) - 1)
    toplam_odeme = taksit * k_vade
    
    ko1, ko2 = st.columns(2)
    ko1.metric("Aylık Taksit Tutarı", f"{taksit:,.2f} TL")
    ko2.metric("Toplam Geri Ödeme", f"{toplam_odeme:,.2f} TL", f"Faiz Yükü: {toplam_odeme - k_tutar:,.2f} TL")
    st.markdown("---")

if portfoy_ac:
    st.subheader("🛡️ Algoritmik Varlık Dağılımı ve Risk Simülasyonu")
    p1, p2, p3 = st.columns(3)
    hisse_w = p1.slider("Hisse Senedi Ağırlığı (%)", 0, 100, 50)
    altin_w = p2.slider("Emtia / Altın Ağırlığı (%)", 0, 100, 30)
    nakit_w = p3.slider("Nakit / Likit Ağırlığı (%)", 0, 100, 20)
    
    if hisse_w + altin_w + nakit_w == 100:
        pie_fig = px.pie(
            names=['Hisse Senetleri', 'Altın / Emtia', 'Nakit / Likit'],
            values=[hisse_w, altin_w, nakit_w],
            template="plotly_dark",
            title="Portföy Dağılım Matrisi"
        )
        st.plotly_chart(pie_fig, use_container_width=True)
    else:
        st.warning("⚠️ Varlık dağılım oranlarının toplamı tam olarak %100 olmalıdır.")

# --- BÖLÜM D: VERİ TABLOSU VE DIŞA AKTARIM ---
with st.expander("📂 Ham Piyasa Verileri ve İstatistik Tablosu"):
    if df is not None and not df.empty:
        st.dataframe(df.tail(30), use_container_width=True)
    else:
        st.info("Görüntülenecek veri bulunmuyor.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>ERMADEFİAN Kurumsal Finans Terminali © 2026 | Kesintisiz Yerel İşlem ve Veri Güvenliği</p>", unsafe_allow_html=True)
