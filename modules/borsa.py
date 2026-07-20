import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def borsa_analiz_ekrani():
    st.title("📈 Kurumsal Borsa & Derinlemesine Hisse Analiz Merkezi")
    
    col1, col2 = st.columns([3, 1])
    hisse = col1.text_input("Borsa Hisse / Varlık Kodu (Örn: THYAO.IS, AAPL, EREGL.IS):", "THYAO.IS").upper()
    periyot = col2.selectbox("Veri Periyodu", ["1mo", "3mo", "6mo", "1y", "max"], index=3)
    
    with st.spinner(f"'{hisse}' için borsa verileri ve kademe matrisleri yükleniyor..."):
        try:
            df = yf.download(hisse, period=periyot, interval="1d", progress=False)
            if df.empty:
                st.error("Geçerli bir veri bulunamadı. Lütfen sembolü kontrol edin.")
                return
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
                
            close = df['Close'].squeeze()
            
            # Gelişmiş Teknik İndikatörler
            df['SMA20'] = close.rolling(20).mean()
            df['SMA50'] = close.rolling(50).mean()
            df['SMA200'] = close.rolling(200).mean()
            
            # Bollinger Bantları
            std20 = close.rolling(20).std()
            df['BB_Up'] = df['SMA20'] + (std20 * 2)
            df['BB_Down'] = df['SMA20'] - (std20 * 2)
            
            # RSI Hesaplama
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            ticker_obj = yf.Ticker(hisse)
            info = ticker_obj.info
            
            son_fiyat = float(close.iloc[-1])
            onceki_fiyat = float(close.iloc[-2])
            gunluk_degisim = ((son_fiyat - onceki_fiyat) / onceki_fiyat) * 100
            
            # Üst Özet Metrikleri
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Son Fiyat", f"{son_fiyat:,.2f}", f"{gunluk_degisim:+.2f}%")
            m2.metric("RSI (14)", f"{float(df['RSI'].iloc[-1]):.2f}")
            m3.metric("SMA 20", f"{float(df['SMA20'].iloc[-1]):,.2f}")
            m4.metric("52H Yüksek", f"{info.get('fiftyTwoWeekHigh', son_fiyat * 1.2):,.2f}")
            m5.metric("Piyasa Değeri", f"{info.get('marketCap', 0)/1000000000:,.2f} Mr" if info.get('marketCap') else "N/A")
            
            # Profesyonel Mum Grafiği (Candlestick) ve Bollinger Bantları
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index, open=df['Open'].squeeze(), high=df['High'].squeeze(),
                low=df['Low'].squeeze(), close=close, name='Fiyat Mumları'
            ))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'].squeeze(), name='SMA 20', line=dict(color='#ff7f0e', width=1.5)))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'].squeeze(), name='SMA 50', line=dict(color='#1f77b4', width=1.5)))
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Up'].squeeze(), name='Bollinger Üst', line=dict(color='gray', width=1, dash='dot')))
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Down'].squeeze(), name='Bollinger Alt', line=dict(color='gray', width=1, dash='dot')))
            
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=10, r=10, t=10, b=10),
                height=520,
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Şirket Bilgileri ve Ham Veri Tablosu
            col_det1, col_det2 = st.columns(2)
            with col_det1:
                st.subheader("🏢 Şirket / Varlık Künyesi")
                st.json({
                    "Şirket Adı": info.get('longName', hisse),
                    "Sektör": info.get('sector', 'Bilinmiyor'),
                    "Ülke": info.get('country', 'Bilinmiyor'),
                    "F/K Oranı": info.get('trailingPE', 'N/A'),
                    "Temettü Verimi": f"%{info.get('dividendYield', 0)*100:.2f}" if info.get('dividendYield') else "N/A"
                })
            with col_det2:
                st.subheader("📂 Son 30 Günlük İşlem Matrisi")
                st.dataframe(df[['Open', 'High', 'Low', 'Close', 'Volume', 'RSI']].tail(30), use_container_width=True)
                
        except Exception as e:
            st.error(f"Veri işlenirken hata oluştu: {e}")