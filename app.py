import streamlit as st
import yfinance as yf
import requests
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="Devrimsel Finans Platformu", layout="wide")

st.title("Devrimsel Finans ve Analiz Platformu")
st.subheader("Gemini AI ile Gerçek Zamanlı Yapay Zeka Analizi")

# API Anahtarı Kontrolü
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
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
                        f"{hisse_kodu} kodlu hissenin son 1 aylık verilerine göre güncel fiyatı {guncel_fiyat:.2f} seviyesindedir. "
                        f"Bu hisse hakkında yatırımcılar için Türkçe, kısa, teknik ve temel bir özet analiz yap. "
                        f"Destek/direnç durumlarını ve genel piyasa algısını yorumlayarak önerilerini listele."
                    )
                    
                    # Google'ın en güncel ve kararlı 2.5-flash endpoint'i
                    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
                    
                    headers = {
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key
                    }
                    
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                    
                    # 429 Hatalarını aşmak için Döngüsel Yeniden Deneme Mekanizması (Max 3 Deneme)
                    basarili = False
                    for deneme in range(3):
                        response = requests.post(f"{url}?key={api_key}", json=payload, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            ai_response = data['candidates'][0]['content']['parts'][0]['text']
                            st.write(ai_response)
                            basarili = True
                            break
                        elif response.status_code == 429:
                            # 429 durumunda kullanıcıyı bilgilendir ve 5 saniye bekleyip tekrar dene
                            st.warning(f"Sunucu yoğun (Kota 429). {deneme + 1}. deneme başarısız. 5 saniye sonra otomatik tekrar deneniyor...")
                            time.sleep(5)
                        else:
                            st.error(f"Gemini API Hatası: {response.status_code} - {response.text}")
                            basarili = True
                            break
                            
                    if not basarili:
                        st.error("Ücretsiz API kotanız şu an tamamen dolu. Lütfen 30 saniye bekleyip sayfayı yenileyerek tekrar deneyin.")
                        
            else:
                st.error("Hisse verisi bulunamadı. Lütfen kodu doğru girdiğinizden emin olun.")
        except Exception as e:
            st.error(f"Veri çekilirken bir hata oluştu: {e}")
