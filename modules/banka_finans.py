import streamlit as st
import pandas as pd
import numpy as np

def banka_finans_ekrani():
    st.title("🏦 Bankacılık, Mevduat & Kredi Optimizasyon Merkezi")
    st.write("Ziraat ve diğer kurumsal bankacılık standartlarında net kazanç, stopaj kesintileri ve kredi taksit simülasyonları.")
    
    islem_turu = st.tabs(["📊 Vadeli Mevduat & Getiri", "💳 Kredi Taksit & Maliyet", "📈 Enflasyon & Satın Alma Gücü"])
    
    # 1. SEKME: MEVDUAT
    with islem_turu[0]:
        st.subheader("Kurumsal Vadeli Mevduat Getiri Simülatörü")
        
        c1, c2, c3 = st.columns(3)
        anapara = c1.number_input("Yatırılacak Anapara (TL):", min_value=1000, value=250000, step=10000)
        yillik_faiz = c2.number_input("Yıllık Brüt Faiz Oranı (%):", min_value=1.0, max_value=80.0, value=48.0, step=0.5)
        vade_gun = c3.slider("Vade Süresi (Gün)", min_value=30, max_value=365, value=90, step=30)
        
        stopaj_orani = st.selectbox("Stopaj (Vergi) Oranı Grubu", ["6 Aya Kadar Vadeli (%7.5)", "1yıla Kadar Vadeli (%5)", "1 Yıldan Uzun (%0)"])
        
        if "7.5" in stopaj_orani:
            vergi_yuzdesi = 0.075
        elif "5" in stopaj_orani:
            vergi_yuzdesi = 0.05
        else:
            vergi_yuzdesi = 0.0
            
        brut_getiri = anapara * (yillik_faiz / 100) * (vade_gun / 365)
        stopaj_kesintisi = brut_getiri * vergi_yuzdesi
        net_getiri = brut_getiri - stopaj_kesintisi
        vade_sonu_toplam = anapara + net_getiri
        
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Brüt Faiz Getirisi", f"{brut_getiri:,.2f} TL")
        m2.metric("Kesilen Stopaj (Vergi)", f"-{stopaj_kesintisi:,.2f} TL", delta_color="inverse")
        m3.metric("Net Vade Sonu Tutar", f"{vade_sonu_toplam:,.2f} TL", f"+{net_getiri:,.2f} TL Net Kazanç")
        
    # 2. SEKME: KREDİ
    with islem_turu[1]:
        st.subheader("Profesyonel Kredi Ödeme ve Maliyet Planı")
        
        kc1, kc2, kc3 = st.columns(3)
        kredi_tutar = kc1.number_input("Kredi Tutarı (TL):", min_value=10000, value=500000, step=25000)
        aylik_faiz = kc2.number_input("Aylık Akdi Faiz Oranı (%):", min_value=0.1, max_value=15.0, value=3.8, step=0.1)
        vade_ay = kc3.slider("Vade (Ay Sayısı):", min_value=3, max_value=120, value=36, step=3)
        
        oran = aylik_faiz / 100
        if oran > 0:
            taksit = (kredi_tutar * oran * ((1 + oran)**vade_ay)) / (((1 + oran)**vade_ay) - 1)
        else:
            taksit = kredi_tutar / vade_ay
            
        toplam_geri_odeme = taksit * vade_ay
        toplam_faiz_yuku = toplam_geri_odeme - kredi_tutar
        
        st.markdown("---")
        ko1, ko2, ko3 = st.columns(3)
        ko1.metric("Aylık Taksit Tutarı", f"{taksit:,.2f} TL")
        ko2.metric("Toplam Geri Ödeme", f"{toplam_geri_odeme:,.2f} TL")
        ko3.metric("Toplam Faiz Yükü", f"{toplam_faiz_yuku:,.2f} TL", delta_color="inverse")
        
        if st.button("Detaylı Amortisman (Ödeme) Planını Göster"):
            plan_data = []
            kalan_anapara = kredi_tutar
            for ay in range(1, vade_ay + 1):
                faiz_tutari = kalan_anapara * oran
                anapara_tutari = taksit - faiz_tutari
                kalan_anapara -= anapara_tutari
                plan_data.append({
                    "Ay": ay,
                    "Taksit": round(taksit, 2),
                    "Anapara": round(anapara_tutari, 2),
                    "Faiz": round(faiz_tutari, 2),
                    "Kalan Borç": max(0, round(kalan_anapara, 2))
                })
            df_plan = pd.DataFrame(plan_data)
            st.dataframe(df_plan, use_container_width=True)

    # 3. SEKME: ENFLASYON
    with islem_turu[2]:
        st.subheader("Enflasyonun Paranın Satın Alma Gücüne Etkisi")
        bas_para = st.number_input("Mevcut Para / Sermaye (TL):", 100000, 10000000, 1000000)
        enf_orani = st.slider("Yıllık Beklenen Enflasyon Oranı (%)", 5.0, 100.0, 35.0)
        yil_sayisi = st.slider("Yıl Süresi", 1, 10, 3)
        
        guncel_deger = bas_para / ((1 + (enf_orani / 100)) ** yil_sayisi)
        kayip = bas_para - guncel_deger
        
        st.metric(f"{yil_sayisi} Yıl Sonra Paranızın Reel Satın Alma Gücü", f"{guncel_deger:,.2f} TL", f"-{kayip:,.2f} TL Değer Erimesi", delta_color="inverse")