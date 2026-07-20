import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def risk_simulasyon_ekrani():
    st.title("🛡️ Kurumsal Portföy & Monte Carlo Risk Laboratuvarı")
    st.write("Yatırım sepetinin gelecekteki olası risklerini, volatilite oranlarını ve Monte Carlo olasılık simülasyonlarını test edin.")
    
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
