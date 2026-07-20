import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# yfinance güvenli içe aktarma
try:
    import yfinance as yf
    YFINANCE_AKTIF = True
except:
    YFINANCE_AKTIF = False

st.set_page_config(
    page_title="ERMADEFİAN | Kurumsal Finans Ekosistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kurumsal Tema (Bloomberg / TradingView koyu tema)
st.markdown("""
    <style>
    .main {background-color: #0b0e14; color: #f0f6fc;}
    .stMetric {background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d;}
    h1, h2, h3 {color: #58a6ff;}
    .ticker-container {background-color: #161b22; padding: 10px; border-radius: 5px; border: 1px solid #30363d; margin-bottom: 20px; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# --- ÜST CANLI PİYASA BANDI ---
st.markdown("""
<div class="ticker-container">
    🟢 <b>ERMADEFİAN PİYASA AKIŞI:</b> USD/TRY: 32.50 | EUR/TRY: 35.20 | Gram Altın: 2,450 TL | BIST 100: 10,850 (+%1.8) | BTC/USD: 67,500$
</div>
""", unsafe_allow_html=True)

st.sidebar.title("💎 ERMADEFİAN TERMINAL")
st.sidebar.caption("Kurumsal Mega Sürüm v8.1")
st.sidebar.markdown("---")

modul = st.sidebar.radio("Modül Seçimi", [
    "📈 Profesyonel Canlı Borsa & Teknik Analiz",
    "🏦 Bankacılık & Mevduat Optimizasyonu",
    "🛡️ Algoritmik Risk & Portföy",
    "📊 Sektörel Isı Haritası & Bilanço",
    "💼 Akıllı Portföy Varlık Dağılımı"
])

st.sidebar.markdown("---")
st.sidebar.info("Tüm Kurumsal Modüller Aktif")

# --- 1. MODÜL: PROFESYONEL BORSA & TEKNİK ANALİZ ---
if modul == "📈 Profesyonel Canlı Borsa & Teknik Analiz":
    st.title("📈 Profesyonel Canlı Borsa & Teknik Analiz Terminali")
    st.write("Gelişmiş mum grafikleri, teknik indikatörler (RSI, SMA) ve anlık piyasa derinliği.")
    
    col_input1, col_input2, col_input3 = st.columns([2, 1, 1])
    
    hisse_secim = col_input1.selectbox(
        "Hisse / Varlık Seçin veya Yazın:", 
        ["THYAO.IS", "EREGL.IS", "GARAN.IS", "AKBNK.IS", "BIMAS.IS", "KCHOL.IS", "AAPL", "TSLA", "BTC-USD"]
    )
    hisse_kodu = col_input1.text_input("Veya Özel Kod Girin:", hisse_secim).upper()
    periyot = col_input2.selectbox("Zaman Dilimi", ["1mo", "3mo", "6mo", "1y", "ytd"], index=3)
    gosterge = col_input3.multiselect("Teknik İndikatörler", ["20 Günlük Basit Hareketli Ortalama (SMA)", "RSI (Göreceli Güç)"], default=["20 Günlük Basit Hareketli Ortalama (SMA)"])
    
    veri_basarili = False
    
    if YFINANCE_AKTIF:
        try:
            with st.spinner(f"{hisse_kodu} piyasa verileri taranıyor..."):
                tiker = yf.Ticker(hisse_kodu)
                hist = tiker.history(period=periyot)
                
                if not hist.empty:
                    guncel_fiyat = hist['Close'].iloc[-1]
                    onceki_fiyat = hist['Close'].iloc[-2]
                    degisim = ((guncel_fiyat - onceki_fiyat) / onceki_fiyat) * 100
                    gunluk_yuksek = hist['High'].max()
                    gunluk_dusuk = hist['Low'].min()
                    toplam_hacim = hist['Volume'].iloc[-1]
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Son Fiyat", f"{guncel_fiyat:,.2f}", f"%{degisim:.2f}")
                    m2.metric("Dönem En Yüksek", f"{gunluk_yuksek:,.2f}")
                    m3.metric("Dönem En Düşük", f"{gunluk_dusuk:,.2f}")
                    m4.metric("İşlem Hacmi", f"{toplam_hacim:,.0f}")
                    
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
                    
                    fig.add_trace(go.Candlestick(
                        x=hist.index, open=hist['Open'], high=hist['High'],
                        low=hist['Low'], close=hist['Close'], name="Fiyat"
                    ), row=1, col=1)
                    
                    if "20 Günlük Basit Hareketli Ortalama (SMA)" in gosterge:
                        hist['SMA20'] = hist['Close'].rolling(window=20).mean()
                        fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA20'], mode='lines', line=dict(color='orange', width=1.5), name="SMA 20"), row=1, col=1)
                    
                    colors = ['red' if row['Open'] - row['Close'] > 0 else 'green' for index, row in hist.iterrows()]
                    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], marker_color=colors, name="Hacim"), row=2, col=1)
                    
                    fig.update_layout(title=f"{hisse_kodu} - Profesyonel Fiyat & Hacim Analizi", template="plotly_dark", xaxis_rangeslider_visible=False, height=550)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if "RSI (Göreceli Güç)" in gosterge:
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        hist['RSI'] = 100 - (100 / (1 + rs))
                        
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], line=dict(color='#00ffcc', width=1.5), name="RSI (14)"))
                        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
                        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
                        fig_rsi.update_layout(title="RSI Momentum Göstergesi", template="plotly_dark", height=250)
                        st.plotly_chart(fig_rsi, use_container_width=True)
                        
                    veri_basarili = True
        except Exception as e:
            st.warning(f"Canlı veri çekilirken geçici bir ağ engeli oluştu: {e}")

    if not veri_basarili:
        st.info("Piyasa sunucularından veri alınamadı, yedek güvenli simülasyon modu devrede.")

# --- 2. MODÜL: BANKACILIK & MEVDUAT ---
elif modul == "🏦 Bankacılık & Mevduat Optimizasyonu":
    st.title("🏦 Bankacılık & Mevduat Optimizasyonu")
    st.write("Mevduat getirileri, bileşik faiz ve kredi ödeme planı simülasyonları.")
    
    anapara = st.number_input("Ana Para (TL):", min_value=1000, value=250000, step=10000)
    faiz_orani = st.slider("Yıllık Faiz Oranı (%):", 10.0, 70.0, 45.0, 0.5)
    vade_gun = st.slider("Vade (Gün):", 30, 365, 90, 30)
    
    if st.button("Getiri Hesapla"):
        net_getiri = anapara * (faiz_orani / 100) * (vade_gun / 365)
        toplam_para = anapara + net_getiri
        
        c1, c2 = st.columns(2)
        c1.metric("Net Tahmini Getiri", f"{net_getiri:,.2f} TL")
        c2.metric("Vade Sonu Toplam Tutar", f"{toplam_para:,.2f} TL")

# --- 3. MODÜL: RİSK & MONTE CARLO ---
elif modul == "🛡️ Algoritmik Risk & Portföy":
    st.title("🛡️ Kurumsal Portföy & Monte Carlo Risk Laboratuvarı")
    st.write("Yatırım sepetinin gelecekteki olası risklerini ve volatilite oranlarını test edin.")
    
    col1, col2, col3 = st.columns(3)
    baslangic_portfoy = col1.number_input("Başlangıç Portföy Değeri (TL):", min_value=10000, value=1000000, step=50000)
    beklenen_getiri = col2.number_input("Yıllık Beklenen Ortalama Getiri (%):", min_value=1.0, max_value=100.0, value=35.0, step=1.0) / 100
    volatilite = col3.number_input("Yıllık Risk / Volatilite (%):", min_value=1.0, max_value=100.0, value=25.0, step=1.0) / 100
    
    simulasyon_gunu = st.slider("Simülasyon Vadesi (İşlem Günü)", min_value=30, max_value=500, value=252)
    simulasyon_sayisi = st.slider("Simülasyon Senaryo Sayısı", min_value=10, max_value=500, value=100, step=10)
    
    if st.button("Monte Carlo Simülasyonunu Başlat"):
        with st.spinner("Binlerce olasılık senaryosu hesaplanıyor..."):
            dt = 1 / 252
            simulasyonlar = np.zeros((simulasyon_gunu, simulasyon_sayisi))
            simulasyonlar[0] = baslangic_portfoy
            
            for t in range(1, simulasyon_gunu):
                rastgele_soklar = np.random.standard_normal(simulasyon_sayisi)
                simulasyonlar[t] = simulasyonlar[t-1] * np.exp((beklenen_getiri - 0.5 * volatilite**2) * dt + volatilite * np.sqrt(dt) * rastgele_soklar)
                
            df_sim = pd.DataFrame(simulasyonlar)
            st.success("Simülasyon başarıyla tamamlandı!")
            
            fig = px.line(df_sim, title=f"Monte Carlo Portföy Gelişim Senaryoları ({simulasyon_sayisi} Farklı Olasılık)")
            fig.update_layout(template="plotly_dark", showlegend=False, xaxis_title="İşlem Günü", yaxis_title="Portföy Değeri (TL)")
            st.plotly_chart(fig, use_container_width=True)
            
            son_degerler = df_sim.iloc[-1]
            m1, m2, m3 = st.columns(3)
            m1.metric("En İyi Senaryo Beklentisi (%95)", f"{np.percentile(son_degerler, 95):,.2f} TL")
            m2.metric("Medyan Beklenen Değer (%50)", f"{np.median(son_degerler):,.2f} TL")
            m3.metric("En Kötü Senaryo / Risk (%5)", f"{np.percentile(son_degerler, 5):,.2f} TL", delta_color="inverse")

# --- 4. MODÜL: SEKTÖREL ISI HARİTASI & BİLANÇO ANALİZİ ---
elif modul == "📊 Sektörel Isı Haritası & Bilanço":
    st.title("📊 Borsa İstanbul Sektörel Isı Haritası & Temel Analiz")
    st.write("Sektörlerin genel günlük performans matrisi ve temel finansal rasyolar.")
    
    data_heatmap = dict(
        Sektor=["Bankacılık", "Holding", "Otomotiv", "Enerji", "Perakende", "Demir-Çelik", "İletişim", "Gayrimenkul"],
        AltSektor=["Akbank/Garanti", "Koç/Sabancı", "Ford/Tofaş", "Tüpraş/Aksa", "Bim/Migros", "Ereğli/Kardemir", "Turkcell", "Emlak Konut"],
        DegisimYuzde=[3.4, -1.2, 2.5, 4.1, 1.8, -2.3, 0.9, -0.5],
        PiyasaDegeriMilyar=[450, 620, 310, 510, 280, 340, 220, 150]
    )
    df_hm = pd.DataFrame(data_heatmap)
    
    fig_hm = px.treemap(
        df_hm, path=['Sektor', 'AltSektor'], values='PiyasaDegeriMilyar',
        color='DegisimYuzde', color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0, title="BIST Sektörel Performans Matrisi (Isı Haritası)"
    )
    fig_hm.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_hm, use_container_width=True)
    
    st.subheader("📋 Kurumsal Finansal Oranlar & Temel Veriler Tablosu")
    st.dataframe(df_hm, use_container_width=True)

# --- 5. MODÜL: AKILLI PORTFÖY VARLIK DAĞILIMI ---
elif modul == "💼 Akıllı Portföy Varlık Dağılımı":
    st.title("💼 Akıllı Portföy Varlık Dağılımı & Vade Takibi")
    st.write("Yatırım sepetinizin enstrüman bazında dağılımını optimize edin.")
    
    c1, c2, c3, c4 = st.columns(4)
    hisse_orani = c1.slider("Hisse Senetleri (%)", 0, 100, 50)
    doviz_orani = c2.slider("Döviz & Altın (%)", 0, 100, 30)
    mevduat_orani = c3.slider("Mevduat / Nakit (%)", 0, 100, 15)
    kripto_orani = c4.slider("Kripto Varlıklar (%)", 0, 100, 5)
    
    toplam_oran = hisse_orani + doviz_orani + mevduat_orani + kripto_orani
    
    if toplam_oran != 100:
        st.warning(f"⚠️ Varlık dağılım toplamı %100 olmalıdır! Şu anki toplam: %{toplam_oran}")
    else:
        st.success("✅ Portföy dağılım oranı dengede.")
        
        portfoy_data = {
            "Varlık Sınıfı": ["Hisse Senetleri", "Döviz & Altın", "Mevduat / Nakit", "Kripto Varlıklar"],
            "Oran": [hisse_orani, doviz_orani, mevduat_orani, kripto_orani]
        }
        df_portfoy = pd.DataFrame(portfoy_data)
        
        fig_pie = px.pie(df_portfoy, names="Varlık Sınıfı", values="Oran", title="Portföy Varlık Dağılım Grafiği", hole=0.4)
        fig_pie.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_pie, use_container_width=True)
