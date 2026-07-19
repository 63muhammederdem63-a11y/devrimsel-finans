import streamlit as st
import yfinance as yf
import google.generativeai as genai

st.set_page_config(page_title="ERMADEFİAN AI Analiz", layout="wide")

st.title("ERMADEFİAN: Profesyonel Finansal Analiz Sistemi")
hisse_kodu = st.text_input("Analiz edilecek hisse:", "AAPL")

# Google Generative AI Yapılandırması
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Anahtarı yapılandırma hatası. Lütfen Secrets ayarlarını kontrol edin.")

if st.button("Detaylı Analiz Et"):
    if not hisse_kodu:
        st.warning("Lütfen bir hisse kodu girin.")
    else:
        try:
            hisse = yf.Ticker(hisse_kodu)
            hist = hisse.history(period="1mo")
            
            if not hist.empty:
                son_fiyat = hist['Close'].iloc[-1]
                st.success(f"Güncel Fiyat: ${son_fiyat:.2f}")
                st.line_chart(hist['Close'])
                
                with st.spinner("YZ Derinlemesine Analiz Yapılıyor..."):
                    prompt = f"""
                    Hisse: {hisse_kodu}, Güncel Fiyat: {son_fiyat:.2f}.
                    Son 1 aylık verileri teknik ve temel açıdan analiz et.
                    1. Teknik trend yorumu.
                    2. Piyasa algısı ve risk faktörleri.
                    3. Yatırımcılar için 3 stratejik öneri.
                    Analiz profesyonel, detaylı ve Türkçe olmalıdır.
                    """
                    
                    # Resmi kütüphane ile analiz
                    response = model.generate_content(prompt)
                    st.subheader("🤖 Detaylı AI Raporu")
                    st.write(response.text)
            else:
                st.error("Veri bulunamadı. Lütfen geçerli bir hisse kodu girin.")
        except Exception as e:
            st.error(f"Analiz sırasında bir hata oluştu: {str(e)}")
