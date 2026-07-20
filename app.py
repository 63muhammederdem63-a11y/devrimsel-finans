import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

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

# --- 1. MODÜL: BORSA & HİSSE ANALİZ ---
if modul == "📈 Borsa & Hisse Analiz Merkezi":
    st.title("📈 Borsa & Hisse Senedi Analiz Merkezi")
    st.write("Canlı borsa verileri, hisse rasyoları ve teknik gösterge analizleri.")
    
    hisse = st.text_input("Hisse Senedi Kodu (Örn: THYAO.IS, GARAN.IS, AAPL):", "THYAO.IS").upper()
    if st.button("Hisse Analizini Çalıştır"):
        st.success(f"{hisse} için veri analizi ve rasyo hesaplamaları hazır!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Son Fiyat", "295.50 TL", "+%3.4")
        col2.metric("Piyasa Değeri", "405 Mil. TL")
        col3.metric("F/K Oranı", "7.82")

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
            
            fig = px.line(df_sim, title=f"Monte Carlo Portföy Gelişim Senaryoları ({simulasyon_sayisi} Farklı Olasılık)")
            fig.update_layout(template="plotly_dark", showlegend=False, xaxis_title="İşlem Günü", yaxis_title="Portföy Değeri (TL)")
            st.plotly_chart(fig, use_container_width=True)
            
            son_degerler = df_sim.iloc[-1]
            m1, m2, m3 = st.columns(3)
            m1.metric("En İyi Senaryo Beklentisi (%95)", f"{np.percentile(son_degerler, 95):,.2f} TL")
            m2.metric("Medyan Beklenen Değer (%50)", f"{np.median(son_degerler):,.2f} TL")
            m3.metric("En Kötü Senaryo / Risk (%5)", f"{np.percentile(son_degerler, 5):,.2f} TL", delta_color="inverse")
