import streamlit as st
import yfinance as yf
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Devrimsel Finans Platformu", layout="wide")

st.title("Devrimsel Finans ve Analiz Platformu")
st.subheader("Gemini AI ile Gerçek Zamanlı Yapay Zeka Analizi")

# Gemini API Bağlantısı
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Anahtarı yapılandırılamadı. Lütfen Streamlit Secrets ayarlarını kontrol edin.")

# Kullanıcı Girişi
hisse_kodu = st.text_input("Analiz edilecek hisse kodunu girin (Örn: AAPL, TSLA, THYAO.IS):", "AAPL")

if st.button("Verileri Çek ve Analiz Et"):
    if hisse_kodu:
        st.info(f"{hisse_kodu} için güncel veriler çekiliyor...")
        
        try:
            # yfinance ile veri çekme
            hisse = yf.Ticker(hisse_kodu)
            veri = hisse.history(period="1mo")
            
            if not veri.empty:
                guncel_fiyat = veri['Close'].iloc[-1]
                st.success(f"Güncel Kapanış Fiyatı: ${guncel_fiyat:.2f}")
                
                # Grafik Çizimi
                st.line_chart(veri['Close'])
                
                # Yapay Zeka Analizi
                st.subheader("Yapay Zeka Analiz Raporu")
                with st.spinner("Gemini Yapay Zeka analizi yapıyor..."):
                    prompt = (
                        f"{hisse_kodu} kodlu hissenin son 1 aylık verilerine göre güncel fiyatı {guncel_fiyat:.2f} dolar/TL seviyesindedir. "
                        f"Bu hisse hakkında yatırımcılar için Türkçe, kısa, teknik ve temel bir özet analiz yap. "
                        f"Destek/direnç durumlarını ve genel piyasa algısını yorumlayarak önerilerini listele."
                    )
                    response = model.model.generate_content(prompt) if hasattr(model, 'model') else model.generate_content(prompt)
                    st.write(response.text)
            else:
                st.error("Hisse verisi bulunamadı. Lütfen kodu doğru girdiğinizden emin olun.")
        except Exception as e:
            st.error(f"Veri çekilirken bir hata oluştu: {e}")
