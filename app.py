import streamlit as st
import yfinance as yf
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Devrimsel Finans Platformu", layout="wide")

st.title("Devrimsel Finans ve Analiz Platformu")
st.subheader("Açık Kaynak Llama AI ile Gerçek Zamanlı Yapay Zeka Analizi")

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
                with st.spinner("Yapay Zeka analizi yapıyor..."):
                    prompt = (
                        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
                        f"Sen profesyonel bir finans analistisin. Verilen hisse verilerini analiz edip Türkçe yanıt veriyorsun.<|eot_id|>\n"
                        f"<|start_header_id|>user<|end_header_id|>\n"
                        f"{hisse_kodu} kodlu hissenin son 1 aylık verilerine göre güncel fiyatı {guncel_fiyat:.2f} seviyesindedir. "
                        f"Bu hisse hakkında yatırımcılar için Türkçe, kısa, teknik ve temel bir özet analiz yap. "
                        f"Destek/direnç durumlarını ve genel piyasa algısını yorumlayarak önerilerini listele.<|eot_id|>\n"
                        f"<|start_header_id|>assistant<|end_header_id|>\n"
                    )
                    
                    # Hugging Face Ücretsiz Sunucusuz API Endpoint (Meta Llama 3)
                    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
                    
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 500,
                            "temperature": 0.7,
                            "return_full_text": False
                        }
                    }
                    
                    # Herhangi bir token sınırı olmadan çalışması için istek atıyoruz
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # Hugging Face yanıt formatına göre text'i çekiyoruz
                        if isinstance(data, list) and len(data) > 0:
                            ai_response = data[0].get('generated_text', 'Analiz üretilemedi.')
                            st.write(ai_response)
                        else:
                            st.write(str(data))
                    elif response.status_code == 503:
                        st.warning("Model şu an sunucuda yükleniyor (Hugging Face uyanıyor). Lütfen 10 saniye sonra butona tekrar basın.")
                    else:
                        st.error(f"Yapay Zeka Hatası: {response.status_code} - {response.text}")
                        
            else:
                st.error("Hisse verisi bulunamadı. Lütfen kodu doğru girdiğinizden emin olun.")
        except Exception as e:
            st.error(f"Veri çekilirken bir hata oluştu: {e}")
