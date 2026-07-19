import streamlit as st
import yfinance as yf
import requests

st.set_page_config(page_title="ERMADEFİAN AI Analiz", layout="wide")

st.title("ERMADEFİAN: Profesyonel Finansal Analiz Sistemi")
hisse_kodu = st.text_input("Analiz edilecek hisse:", "AAPL")

if st.button("Detaylı Analiz Et"):
    try:
        hisse = yf.Ticker(hisse_kodu)
        hist = hisse.history(period="1mo")
        
        if not hist.empty:
            son_fiyat = hist['Close'].iloc[-1]
            st.success(f"Güncel Fiyat: ${son_fiyat:.2f}")
            st.line_chart(hist['Close'])
            
            with st.spinner("YZ Derinlemesine Analiz Yapılıyor..."):
                # Gemini için optimize edilmiş sistem mesajı
                prompt = f"""
                Hisse: {hisse_kodu}, Güncel Fiyat: {son_fiyat:.2f}.
                Lütfen bu veriyi kullanarak:
                1. Teknik analiz (Trend, momentum).
                2. Temel beklentiler ve piyasa algısı.
                3. Yatırımcılar için 3 maddelik stratejik öneri listesi oluştur.
                Analiz profesyonel, detaylı ve Türkçe olsun.
                """
                
                # Google AI Studio'dan aldığın anahtarı Streamlit Secrets'ta 'GEMINI_API_KEY' olarak tanımla
                api_key = st.secrets["GEMINI_API_KEY"]
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    analiz = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.subheader("🤖 Detaylı AI Raporu")
                    st.write(analiz)
                else:
                    st.error("API hatası oluştu, lütfen anahtarını kontrol et.")
        else:
            st.error("Veri bulunamadı.")
    except Exception as e:
        st.error(f"Sistem hatası: {e}")
