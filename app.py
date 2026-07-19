import streamlit as st
import yfinance as yf

st.set_page_config(page_title="ERMADEFİAN Yerel", layout="wide")
st.title("ERMADEFİAN: API'siz Yerel Analiz Motoru")

hisse_kodu = st.text_input("Hisse kodu:", "AAPL")

if st.button("Analiz Et"):
    try:
        hisse = yf.Ticker(hisse_kodu)
        hist = hisse.history(period="3mo")
        
        if not hist.empty:
            fiyatlar = hist['Close']
            son_fiyat = fiyatlar.iloc[-1]
            degisim = ((son_fiyat - fiyatlar.iloc[0]) / fiyatlar.iloc[0]) * 100
            hareketli_ortalama = fiyatlar.rolling(window=20).mean().iloc[-1]
            
            st.success(f"Güncel Fiyat: ${son_fiyat:.2f}")
            st.line_chart(fiyatlar)
            
            # Tamamen kod tabanlı mantıksal analiz (API gerektirmez)
            st.subheader("📊 Algoritmik Durum Raporu")
            
            durum = "Yükseliş Trendi" if son_fiyat > hareketli_ortalama else "Düşüş Trendi"
            volatilite = "Yüksek" if (fiyatlar.std() / son_fiyat) > 0.02 else "Düşük"
            
            st.write(f"- **Trend Analizi:** Hisse şu an {hareketli_ortalama:.2f} olan 20 günlük ortalamanın üzerinde/altında olduğu için {durum} içerisindedir.")
            st.write(f"- **Fiyat Değişimi:** Son 3 ayda %{degisim:.2f} değişim göstermiştir.")
            st.write(f"- **Risk Seviyesi:** Fiyat oynaklığına göre volatilite durumu: {volatilite}.")
            st.write("- **Özet:** Bu veriler tamamen teknik istatistiksel hesaplamalardır.")
        else:
            st.error("Hisse verisi bulunamadı.")
    except Exception as e:
        st.error(f"İşlem hatası: {e}")
