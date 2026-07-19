import streamlit as st
import yfinance as yf
import requests

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
                    
                    # Tüm yeni ve taze API key'lerde 404 hatasını kesin olarak önleyen kararlı evrensel endpoint
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                    
                    response = requests.post(url, json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data['candidates'][0]['content']['parts'][0]['text']
                        st.write(ai_response)
                    elif response.status_code == 404:
                        # Sunucuda alternatif olarak en temel modeli (gemini-pro) zorla
                        fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                        fallback_resp = requests.post(fallback_url, json=payload, headers=headers)
                        if fallback_resp.status_code == 200:
                            data = fallback_resp.json()
                            st.write(data['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error("Model Bağlantı Hatası: Sunucu modele yanıt vermedi. Lütfen biraz bekleyip tekrar deneyin.")
                    elif response.status_code == 429:
                        st.error("Kota Sınırı: Çok fazla istek yapıldı, lütfen 15 saniye bekleyip butona tekrar basın.")
                    else:
                        st.error(f"Gemini API Hatası: {response.status_code} - {response.text}")
                        
            else:
                st.error("Hisse verisi bulunamadı. Lütfen kodu doğru girdiğinizden emin olun.")
        except Exception as e:
            st.error(f"Veri çekilirken bir hata oluştu: {e}")
