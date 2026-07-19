import streamlit as st
import yfinance as yf

# Sayfa Yapılandırması
st.set_page_config(page_title="ERMADEFİAN Analiz", layout="wide")

st.title("ERMADEFİAN: Yerel Finansal Analiz Sistemi")

hisse_kodu = st.text_input("Analiz edilecek hisse:", "AAPL")

if st.button("Analiz Et"):
    try:
        hisse = yf.Ticker(hisse_kodu)
        hist = hisse.history(period="1mo")
        
        if not hist.empty:
            son_fiyat = hist['Close'].iloc[-1]
            ilk_fiyat = hist['Close'].iloc[0]
            degisim = ((son_fiyat - ilk_fiyat) / ilk_fiyat) * 100
            
            st.success(f"Güncel Fiyat: {son_fiyat:.2f}")
            st.line_chart(hist['Close'])
            
            st.subheader("Otomatik İstatistiksel Analiz")
            
            # Yerel analiz mantığı (API gerekmez)
            if degisim > 0:
                durum = "YÜKSELİŞ"
                yorum = "Son bir ayda hisse pozitif bir ivme sergiledi."
            else:
                durum = "DÜŞÜŞ"
                yorum = "Son bir ayda hisse değer kaybı yaşadı, dikkatli olunmalı."
            
            st.write(f"**Durum:** {durum} (%{degisim:.2f})")
            st.write(f"**Özet:** {yorum}")
            st.write("Not: Bu analiz teknik veriler üzerinden otomatik hesaplanmıştır.")
            
        else:
            st.error("Hisse verisi alınamadı.")
    except Exception as e:
        st.error("Bir hata oluştu.")
