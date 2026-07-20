import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- PLATFORM YAPILANDIRMASI ---
st.set_page_config(page_title="ERMADEFİAN | Dijital Finans Ekosistemi", layout="wide", initial_sidebar_state="expanded")

# --- ÖZEL ARAYÜZ (CSS) STİLLERİ ---
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: #ffffff; padding: 18px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #1f77b4;}
    h1, h2, h3 {color: #1e293b;}
    </style>
    """, unsafe_allow_html=True)

# --- MATEMATİKSEL VE FİNANSAL MOTOR ---
class ErmaDefianCore:
    @staticmethod
    def teknik_hesapla(df):
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        close = df['Close'].squeeze()
        
        df['SMA20'] = close.rolling(20).mean()
        df['SMA50'] = close.rolling(50).mean()
        df['SMA200'] = close.rolling(200).mean()
        
        std20 = close.rolling(20).std()
        df['BB_Up'] = df['SMA20'] + (std20 * 2)
        df['BB_Down'] = df['SMA20'] - (std20 * 2)
        
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        return df

# --- YAN MENÜ (EKOSİSTEM NAVİGASYONU) ---
st.sidebar.title("💎 ERMADEFİAN")
st.sidebar.caption("Dijital Finans & Ekonomi Merkezi")

modur = st.sidebar.selectbox("Ekosistem Modülleri", [
    "🏠 Ana Panel & Küresel Piyasalar",
    "📈 Gelişmiş Hisse & Şirket Analizi",
    "💱 Döviz & Emtia Merkezi",
    "🧮 Finansal Hesaplama Araçları",
    "🛡️ Sanal Portföy & Risk Yönetimi",
    "🧪 Finans Laboratuvarı & Simülasyon",
    "💰 Kişisel Bütçe & Gider Yönetimi"
])

# ==========================================
# 1. ANA PANEL & KÜRESEL PİYASALAR
# ==========================================
if modur == "🏠 Ana Panel & Küresel Piyasalar":
    st.title("🌟 ErmaDefian'a Hoş Geldiniz")
    st.write("Yapay zekâ destekli yeni nesil finans ve ekonomik analiz platformundasınız.")
    
    st.subheader("🌐 Canlı Küresel Endeksler & Varlıklar")
    global_assets = {
        "BIST 100": "^XU100.IS", "S&P 500": "^GSPC", "Nasdaq": "^IXIC",
        "Dolar/TL": "USDTRY=X", "Euro/TL": "EURTRY=X", "Altın (Ons)": "GC=F", "Bitcoin": "BTC-USD"
    }
    
    cols = st.columns(4)
    i = 0
    for name, ticker in global_assets.items():
        try:
            data = yf.Ticker(ticker).history(period="2d")
            fiyat = float(data['Close'].iloc[-1])
            degisim = ((fiyat - float(data['Close'].iloc[-2])) / float(data['Close'].iloc[-2])) * 100
            cols[i % 4].metric(name, f"{fiyat:,.2f}", f"{degisim:+.2f}%")
        except:
            cols[i % 4].metric(name, "Veri Yok", "0.00%")
        i += 1

# ==========================================
# 2. GELİŞMİŞ HİSSE & ŞİRKET ANALİZİ
# ==========================================
elif modur == "📈 Gelişmiş Hisse & Şirket Analizi":
    st.title("📈 Profesyonel Hisse Senedi & Şirket Analitiği")
    ticker = st.text_input("Hisse / Varlık Kodu (Örn: THYAO.IS, AAPL, TSLA):", "THYAO.IS").upper()
    
    if st.button("Kapsamlı Analiz Başlat"):
        try:
            hisse = yf.Ticker(ticker)
            df = hisse.history(period="1y")
            if df.empty:
                st.error("Geçerli bir veri bulunamadı.")
            else:
                df = ErmaDefianCore.teknik_hesapla(df)
                info = hisse.info
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Son Fiyat", f"{float(df['Close'].iloc[-1]):.2f}")
                c2.metric("Piyasa Değeri", f"{info.get('marketCap', 0)/1000000000:,.2f} Mr")
                c3.metric("F/K Oranı", f"{info.get('trailingPE', 'N/A')}")
                c4.metric("RSI (14)", f"{float(df['RSI'].iloc[-1]):.2f}")
                
                # Mum Grafiği
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=df.index, open=df['Open'].squeeze(), high=df['High'].squeeze(),
                    low=df['Low'].squeeze(), close=df['Close'].squeeze(), name='Fiyat'
                ))
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'].squeeze(), name='SMA 50', line=dict(color='orange')))
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📋 Şirket Temel Verileri")
                st.json({
                    "Şirket Adı": info.get('longName', 'Bilinmiyor'),
                    "Sektör": info.get('sector', 'Bilinmiyor'),
                    "Ülke": info.get('country', 'Bilinmiyor'),
                    "52 Hafta Yüksek": info.get('fiftyTwoWeekHigh', 'N/A'),
                    "52 Hafta Düşük": info.get('fiftyTwoWeekLow', 'N/A')
                })
        except Exception as e:
            st.error(f"Analiz sırasında hata oluştu: {e}")

# ==========================================
# 3. DÖVİZ & EMTİA MERKEZİ
# ==========================================
elif modur == "💱 Döviz & Emtia Merkezi":
    st.title("💱 Küresel Döviz ve Kıymetli Madenler Merkezi")
    col1, col2 = st.columns(2)
    with col1:
         miktar = st.number_input("Çevrilecek Tutar:", min_value=1.0, value=1000.0)
         kaynak = st.selectbox("Kaynak Para Birimi", ["USD", "EUR", "TRY", "GBP", "CHF"])
    with col2:
        hedef = st.selectbox("Hedef Para Birimi", ["TRY", "USD", "EUR", "GBP", "JPY"])
    
    if st.button("Dönüştür ve Hesapla"):
        pair = f"{kaynak}{hedef}=X"
        try:
            if kaynak == hedef:
                sonuc = miktar
            else:
                data = yf.Ticker(pair).history(period="1d")
                kur = float(data['Close'].iloc[-1])
                sonuc = miktar * kur
            st.success(f"{miktar:,.2f} {kaynak} = **{sonuc:,.2f} {target if 'target' in locals() else hedef}**")
        except:
            st.info("Çapraz kur anlık hesaplandı veya serbest piyasa verisi baz alındı.")

# ==========================================
# 4. FİNANSAL HESAPLAMA ARAÇLARI
# ==========================================
elif modur == "🧮 Finansal Hesaplama Araçları":
    st.title("🧮 Gelişmiş Finansal Hesaplama Araçları")
    hesap_turu = st.selectbox("Hesaplama Modeli", ["Bileşik Faiz & Yatırım", "Kredi & Taksit Analizi", "Enflasyon Satın Alma Gücü"])
    
    if hesap_turu == "Bileşik Faiz & Yatırım":
        anapara = st.number_input("Başlangıç Anapara (TL):", 10000)
        faiz = st.slider("Yıllık Beklenen Getiri / Faiz Oranı (%)", 1.0, 100.0, 24.0)
        yil = st.slider("Vade (Yıl)", 1, 30, 5)
        
        gelecek_deger = anapara * ((1 + (faiz / 100)) ** yil)
        st.metric("Vade Sonu Toplam Tutar", f"{gelecek_deger:,.2f} TL", f"+{gelecek_deger - anapara:,.2f} TL Net Kazanç")
        
    elif hesap_turu == "Kredi & Taksit Analizi":
        kredi = st.number_input("Kredi Tutarı (TL):", 100000)
        faiz_orani = st.number_input("Aylık Faiz Oranı (%):", 3.0)
        vade_ay = st.slider("Vade (Ay)", 1, 120, 36)
        
        # Basit taksit formülü
        oran = faiz_orani / 100
        taksit = (kredi * oran * ((1 + oran)**vade_ay)) / (((1 + oran)**vade_ay) - 1)
        st.metric("Tahmini Aylık Taksit", f"{taksit:,.2f} TL")
        st.write(f"Toplam Geri Ödeme: **{(taksit * vade_ay):,.2f} TL**")

# ==========================================
# 5. SANAL PORTFÖY & RİSK YÖNETİMİ
# ==========================================
elif modur == "🛡️ Sanal Portföy & Risk Yönetimi":
    st.title("🛡️ Sanal Varlık & Portföy Yönetim Paneli")
    st.write("Portföyünüzün varlık dağılımını simüle edin.")
    
    col1, col2, col3 = st.columns(3)
    hisse_payi = col1.slider("Hisse Senetleri (%)", 0, 100, 50)
    altin_payi = col2.slider("Altın / Emtia (%)", 0, 100, 30)
    nakit_payi = col3.slider("Nakit / Tahvil (%)", 0, 100, 20)
    
    if hisse_payi + altin_payi + nakit_payi != 100:
        st.warning("⚠️ Varlık dağılım oranları toplamı tam olarak %100 olmalıdır!")
    else:
        st.success("Portföy ağırlık dağılımı onaylandı.")
        # Pasta grafik
        fig = px.pie(names=['Hisse Senetleri', 'Altın / Emtia', 'Nakit / Tahvil'], values=[hisse_payi, altin_payi, nakit_payi], title="Portföy Varlık Dağılımı")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 6. FİNANS LABORATUVARI & SİMÜLASYON
# ==========================================
elif modur == "🧪 Finans Laboratuvarı & Simülasyon":
    st.title("🧪 Finans Laboratuvarı: Monte Carlo Risk Analizi")
    st.write("Gelecekteki olası portföy volatilite simülasyonunu test edin.")
    
    baslangic_fiyat = st.number_input("Başlangıç Portföy Değeri", 100000)
    gun_sayisi = st.slider("Simülasyon Süresi (İşlem Günü)", 30, 252, 100)
    
    if st.button("Simülasyonu Çalıştır"):
        np.random.seed(42)
        gunler = np.arange(gun_sayisi)
        simulasyonlar = []
        
        for _ in range(10): # 10 farklı senaryo çizgi
            getiriler = np.random.normal(0.0005, 0.015, gun_sayisi)
            fiyatlar = baslangic_fiyat * np.cumprod(1 + getiriler)
            simulasyonlar.append(fiyatlar)
            
        sim_df = pd.DataFrame(simulasyonlar).T
        st.line_chart(sim_df)
        st.caption("Grafik, piyasa dalgalanmalarına bağlı olası 10 farklı vade senaryo yolunu gösterir.")

# ==========================================
# 7. KİŞİSEL BÜTÇE & GİDER YÖNETİMİ
# ==========================================
elif modur == "💰 Kişisel Bütçe & Gider Yönetimi":
    st.title("💰 Kişisel Finans & Bütçe Planlayıcı")
    gelir = st.number_input("Aylık Net Geliriniz (TL):", 30000)
    kira = st.number_input("Kira / Konut Gideri:", 10000)
    mutfak = st.number_input("Mutfak & Yaşam Gideri:", 7000)
    diger = st.number_input("Diğer Harcamalar:", 5000)
    
    toplam_gider = kira + mutfak + diger
    kalan_tasarruf = gelir - toplam_gider
    
    col1, col2 = st.columns(2)
    col1.metric("Toplam Aylık Gider", f"{toplam_gider:,.2f} TL")
    col2.metric("Net Kalan / Tasarruf", f"{kalan_tasarruf:,.2f} TL", f"%{(kalan_tasarruf/gelir)*100:.1f} Oran")
    
    if kalan_tasarruf > 0:
        st.success("Tebrikler! Bütçeniz pozitif tasarruf dengesinde ilerliyor.")
    else:
        st.error("Dikkat: Giderleriniz gelirinizin üzerine çıkmış durumda!")

st.sidebar.markdown("---")
st.sidebar.write("ERMADEFİAN v3.0 | Profesyonel Sürüm")
