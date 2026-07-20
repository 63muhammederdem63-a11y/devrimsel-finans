import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

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
st.sidebar.caption("Canlı Kurumsal Finans Sistemi v6.0")
st.sidebar.markdown("---")

modul = st.sidebar.radio("Modül Seçimi", [
    "📈 Borsa & Canlı Hisse Analizi",
    "🏦 Bankacılık & Mevduat Optimizasyonu",
    "🛡️ Algoritmik Risk & Portföy"
])

st.sidebar.markdown("---")
st.sidebar.info("Canlı Veri API Entegrasyonu Aktif")

# --- 1. MODÜL: CANLI BORSA & HİSSE ANALİZİ (YFINANCE) ---
if modul == "📈 Borsa & Canlı Hisse Analiz Merkezi":
    st.title("📈 Canlı Borsa & Hisse Senedi Analiz Merkezi")
    st.write("Yahoo Finance altyapısı ile anlık borsa verileri, hacim bilgileri ve profesyonel mum grafikleri.")
    
    col_input1, col_input2 = st.columns([2, 1])
    hisse_kodu = col_input1.text_input("Hisse Senedi Kodu (BIST için .IS ekleyin, örn: THYAO.IS, GARAN.IS, AAPL):", "THYAO.IS").upper()
    periyot = col_input2.selectbox("Veri Periyodu", ["1mo", "3mo", "6mo", "1y", "ytd"], index=3)
    
    if st.button("Canlı Veriyi Çek ve Analiz Et"):
        with st.spinner(f"{hisse_kodu} verileri borsa sunucularından çekiliyor..."):
            try:
                hisse_verisi = yf.Ticker(hisse_kodu)
                hist = hisse_verisi.history(period=periyot)
                
                if hist.empty:
                    st.error(f"'{hisse_kodu}' koduna ait veri bulunamadı. Lütfen kodu kontrol edin (Örn: THYAO.IS).")
                else:
                    guncel_fiyat = hist['Close'].iloc[-1]
                    onceki_fiyat = hist['Close'].iloc[-2]
                    degisim = ((guncel_fiyat - onceki_fiyat) / onceki_fiyat) * 100
                    hacim = hist['Volume'].iloc[-1]
                    
                    # Metrikler
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Son İşlem Fiyatı", f"{guncel_fiyat:,.2f} TL", f"%{degisim:.2f}")
                    m2.metric("Günlük İşlem Hacmi", f"{hacim:,.0f}")
                    m3.metric("Veri Periyodu", periyot.upper())
                    
                    # Profesyonel Mum Grafiği (Candlestick)
                    fig = go.Figure(data=[go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name="Mum Grafiği"
                    )])
                    
                    fig.update_layout(
                        title=f"{hisse_kodu} Profesyonel Fiyat Grafiği",
                        template="plotly_dark",
                        xaxis_title="Tarih",
                        yaxis_title="Fiyat (TL)",
                        xaxis_rangeslider_visible=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Veri çekilirken bir hata oluştu: {e}")

# --- 2. MODÜL: BANKACILIK & MEVDUAT ---
elif modul == "🏦 Bankacılık & Mevduat Optimizasyonu":
    st.title("🏦 Bankacılık & Mevduat Optimizasyonu")
    st.write("Mevduat getirileri, bileşik faiz ve kredi ödeme planı simülasyonları.")
    
    anapara = st.number_input("Ana Para (TL):", min_value=1000, value=250000, step=10000)
    faiz_orani = st.slider("Yıllık Faiz Oranı (%):", 10.0, 70.0, 45.0, 0.5)
    vade_gun = st.slider("Vade (Gün):", 30, 365, 90, 30)
    
    if st.button("Getiri Hesapla"):
        net_getiri = anapara * (faiz_orani / 100) * (vade_gun / 365)
        toplam_para = anapara + net_getiri
        
        c1, c2 = st.columns(2)
        c1.metric("Net Tahmini Getiri", f"{net_getiri:,.2f} TL")
        c2.metric("Vade Sonu Toplam Tutar", f"{toplam_para:,.2f} TL")

# --- 3. MODÜL: RİSK & MONTE CARLO ---
elif modul == "🛡️ Algoritmik Risk & Portföy":
    st.title("🛡️ Kurumsal Portföy & Monte Carlo Risk Laboratuvarı")
    st.write("Yatırım sepetinin gelecekteki olası risklerini ve volatilite oranlarını test edin.")
    
    col1, col2, col3 = st.columns(3)
    baslangic_portfoy = col1.number_input("Başlangıç Portföy Değeri (TL):", min_value=10000, value=1000000, step=50000)
    beklenen_getiri = col2.number_input("Yıllık Beklenen Ortalama Getiri (%):", min_value=1.0, max_value=100.0, value=35.0, step=1.0) / 100
    volatilite = col3.number_input("Yıllık Risk / Volatilite (%):", min_value=1.0, max_value=100.0, value=25.0, step=1.0) / 100
    
    simulasyon_gunu = st.slider("Simülasyon Vadesi (İşlem Günü)", min_value=30, max_value=500, value=252)
    simulasyon_sayisi = st.slider("Simülasyon Senaryo Sayısı", min_value=10, max_value=500, value=100, step=10)
    
    if st.button("Monte Carlo Simülasyonunu Başlat"):
        with st.spinner("Binlerce olasılık senaryosu hesaplanıyor..."):
            dt = 1 / 252
            simulasyonlar = np.zeros((simulasyon_gunu, simulasyon_sayisi))
            simulasyonlar[0] = baslangic_portfoy
            
            for t in range(1, simulasyon_gunu):
                rastgele_soklar = np.random.standard_normal(simulasyon_sayisi)
                simulasyonlar[t] = simulasyonlar[t-1] * np.exp((beklenen_getiri - 0.5 * volatilite**2) * dt + volatilite * np.sqrt(dt) * rastgele_soklar)
                
            df_sim = pd.DataFrame(simulasyonlar)
            st.success("Simülasyon başarıyla tamamlandı!")
            
            fig = go.Figure()
            for col in df_sim.columns:
                fig.add_trace(go.Scatter(y=df_sim[col], mode='lines', line=dict(width=1), opacity=0.3, showlegend=False))
                
            fig.update_layout(
                title=f"Monte Carlo Portföy Gelişim Senaryoları ({simulasyon_sayisi} Farklı Olasılık)",
                template="plotly_dark",
                xaxis_title="İşlem Günü",
                yaxis_title="Portföy Değeri (TL)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            son_degerler = df_sim.iloc[-1]
            m1, m2, m3 = st.columns(3)
            m1.metric("En İyi Senaryo Beklentisi (%95)", f"{np.percentile(son_degerler, 95):,.2f} TL")
            m2.metric("Medyan Beklenen Değer (%50)", f"{np.median(son_degerler):,.2f} TL")
            m3.metric("En Kötü Senaryo / Risk (%5)", f"{np.percentile(son_degerler, 5):,.2f} TL", delta_color="inverse")
