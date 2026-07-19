import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="ERMADEFİAN Pro", layout="wide")
st.title("📈 ERMADEFİAN: Profesyonel Finans Terminali")

hisse_kodu = st.sidebar.text_input("Hisse Kodu (Örn: THYAO.IS):", "THYAO.IS")

if st.sidebar.button("Analiz Et"):
    try:
        # Veri çekme
        hisse = yf.Ticker(hisse_kodu)
        df = hisse.history(period="6mo")
        
        if df.empty:
            st.error("Hisse bulunamadı!")
        else:
            # --- TEKNİK GÖSTERGELER (Hesaplamalar yerel yapılır, API gerektirmez) ---
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            
            # RSI Hesaplama
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Ana Ekran
            st.success(f"{hisse_kodu} Güncel Verileri")
            col1, col2, col3 = st.columns(3)
            col1.metric("Son Fiyat", f"{df['Close'].iloc[-1]:.2f}")
            col2.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")
            col3.metric("Trend", "Pozitif" if df['Close'].iloc[-1] > df['MA20'].iloc[-1] else "Negatif")
            
            # Grafik
            st.line_chart(df[['Close', 'MA20', 'MA50']])
            
            # Detaylı Analiz Paneli
            st.subheader("🤖 Profesyonel Teknik Analiz Özeti")
            
            # Yerel Mantıksal Karar Motoru (API'siz)
            rsi = df['RSI'].iloc[-1]
            if rsi < 30:
                analiz = "Hisse AŞIRI SATIM bölgesinde. Tepki yükselişi beklenebilir (Alım sinyali olabilir)."
            elif rsi > 70:
                analiz = "Hisse AŞIRI ALIM bölgesinde. Düzeltme gelebilir, dikkatli olunmalı."
            else:
                analiz = "Hisse nötr bölgede. Trend takibi önerilir."
            
            st.write(f"**RSI Yorumu:** {analiz}")
            
            # Pivot Seviyeleri
            pivot = (df['High'].iloc[-1] + df['Low'].iloc[-1] + df['Close'].iloc[-1]) / 3
            st.write(f"**Pivot Noktası:** {pivot:.2f} (Destek/Direnç için referans seviyeniz)")
            
            # Veri Tablosu
            with st.expander("Son 10 Günlük Veri"):
                st.table(df.tail(10))

    except Exception as e:
        st.error(f"Sistem Hatası: {e}")
