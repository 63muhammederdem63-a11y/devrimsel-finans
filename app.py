import streamlit as str
import yfinance as yf
import requests
import json

str.title("Devrimsel Finans ve Analiz Platformu")
str.write("Yerel Llama 3 ile Gerçek Zamanlı Yapay Zeka Analizi")

# Kullanıcıdan hisse senedi kodu alma
hisse = str.text_input("Analiz edilecek hisse kodunu girin (Örn: AAPL, TSLA, THYAO.IS):", "AAPL")

if str.button("Verileri Çek ve Analiz Et"):
    # 1. Finansal Verileri Çekme
    str.info(f"{hisse} için güncel veriler çekiliyor...")
    data = yf.Ticker(hisse)
    hist = data.history(period="7d")
    
    if not hist.empty:
        kapanis = hist['Close'].iloc[-1]
        str.success(f"Güncel Kapanış Fiyatı: ${kapanis:.2f}")
        str.line_chart(hist['Close'])
        
        # 2. Yapay Zekaya Gönderilecek Soruyu Hazırlama
        prompt = f"{hisse} kodlu hissenin son 7 günlük kapanış fiyatları sırasıyla şöyledir: {list(hist['Close'].round(2))}. Bu verilere göre teknik bir analiz yap ve kısa bir yatırım tavsiyesi içermeyen yorum üret."
        
        # 3. Yerel Llama 3'e İstek Atma
        str.info("Yerel Llama 3 yapay zeka analizi yapıyor...")
        url = "http://localhost:11434/api/generate"
        payload = {"model": "llama3", "prompt": prompt, "stream": False}
        
        try:
            response = requests.post(url, json=payload)
            analiz = response.json().get("response", "Analiz alınamadı.")
            str.subheader("Yapay Zeka Analiz Raporu")
            str.write(analiz)
        except Exception as e:
            str.error(f"Ollama bağlantı hatası: {e}. Arka planda Ollama uygulamasının açık olduğundan emin olun.")
    else:
        str.error("Hisse verisi bulunamadı. Kodu doğru girdiğinizden emin olun.")