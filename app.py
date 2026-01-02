import streamlit as st
import base64
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import io

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ahi-AI Pro v3.1", page_icon="🧿")

st.title("🧿 Ahi-AI: Gelişmiş Ahilik Envanteri")
st.markdown("**Turizm ve Otelcilik - Mesleki Değerler Analizi**")

# --- SOL MENÜ ---
with st.sidebar:
    st.header("👤 Öğrenci Kimliği")
    ad = st.text_input("Ad Soyad")
    no = st.text_input("Okul No")
    sinif = st.selectbox("Sınıf", ["9-A", "10-B", "11-C", "12-D", "MESEM"])
    st.info("Bu sistem, Ahilik kültüründeki 'Eline, Beline, Diline Sahip Ol' ilkesi temel alınarak hazırlanmıştır.")

# --- FONKSİYON: RADAR GRAFİĞİ ÇİZ ---
def create_radar_chart(categories, values):
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=1, linestyle='solid', color='red')
    ax.fill(angles, values, 'red', alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=8)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color="grey", size=7)
    ax.set_ylim(0, 100)
    return fig

# --- FONKSİYON: PUANLAMA ---
def soru_sor(soru_metni):
    secim = st.radio(
        soru_metni,
        ["Tam Gösteriyor (100p)", "Geliştirilmeli (50p)", "Zayıf (0p)"],
        horizontal=True,
        key=soru_metni
    )
    if "Tam" in secim: return 100
    elif "Geliştirilmeli" in secim: return 50
    else: return 0

# --- ANA FORM ---
if ad and no:
    st.markdown("---")
    
    # KATEGORİ 1: ELİNE SAHİP OL
    st.subheader("1. Eline Sahip Ol (Dürüstlük & Güven)")
    p1_a = soru_sor("Hata yaptığında dürüstçe kabul edip sorumluluk alıyor mu?")
    p1_b = soru_sor("Kurumun malzemesini (demirbaş/gıda) israf etmeden kullanıyor mu?")
    p1 = (p1_a + p1_b) / 2 

    # KATEGORİ 2: DİLİNE SAHİP OL
    st.subheader("2. Diline Sahip Ol (Nezaket & İletişim)")
    p2_a = soru_sor("Müşteri ve arkadaşlarıyla konuşurken üslubuna dikkat ediyor mu?")
    p2_b = soru_sor("Dedikodu yapmaktan ve kırıcı sözlerden kaçınıyor mu?")
    p2 = (p2_a + p2_b) / 2

    # KATEGORİ 3: SOFRASI AÇIK OL
    st.subheader("3. Sofrası Açık Ol (Hizmet & Paylaşım)")
    p3_a = soru_sor("Bilgisini ve tecrübesini arkadaşlarıyla paylaşıyor mu?")
    p3_b = soru_sor("Hizmet ederken karşılık beklemeden güler yüz gösteriyor mu?")
    p3 = (p3_a + p3_b) / 2

    # KATEGORİ 4: SADAKAT VE SEBAT
    st.subheader("4. Kapısı Açık Ol (Misafirperverlik & Sebat)")
    p4_a = soru_sor("Zor müşterilere karşı sabrını koruyabiliyor mu?")
    p4_b = soru_sor("Mesleğin zorluklarına karşı pes etmeden çalışıyor mu?")
    p4 = (p4_a + p4_b) / 2

    st.markdown("---")

    # --- HESAPLAMA VE GÖRSELLEŞTİRME ---
    genel_ort = (p1 + p2 + p3 + p4) / 4
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(label="Genel Ahilik Puanı", value=f"{genel_ort:.0f}")
        if genel_ort >= 85: st.success("🌟 USTA ADAYI")
        elif genel_ort >= 60: st.warning("🛠️ KALFA ADAYI")
        else: st.error("🌱 YAMAK")

    with col2:
        st.write("**Gelişim Grafiği:**")
        categories = ['Durustluk', 'Iletisim', 'Comertlik', 'Sebat']
        values = [p1, p2, p3, p4]
        fig = create_radar_chart(categories, values)
        st.pyplot(fig)

    # --- AYRINTILI RAPOR OLUŞTURMA ---
    
    # Dinamik Tavsiyeler
    tavsiyeler = []
    if p1 < 70: tavsiyeler.append("- 'Eline Sahip Ol': Malzeme israfi kul hakkidir. Demirbaslari korumaya ozen goster.")
    if p2 < 70: tavsiyeler.append("- 'Diline Sahip Ol': Tatli dil yilani deliginden cikarir. Uslubunu yumusatmalisin.")
    if p3 < 70: tavsiyeler.append("- 'Sofrasi Acik Ol': Bilgi paylastikca cogalir. Ekip arkadaslarina yardim et.")
    if p4 < 70: tavsiyeler.append("- 'Sabir': Sabir acidir ama meyvesi tatlidir. Zorluklarda hemen pes etme.")
    
    if not tavsiyeler: tavsiyeler.append("- Tebrikler! Tum Ahilik degerlerini layikiyla tasiyorsun.")

    tavsiye_metni = "\n".join(tavsiyeler)

    yorum = f"Sayin {ad} ({no}), Mesleki Degerler Analizi:\n\n"
    yorum += f"Genel Puan: {genel_ort:.0f} / 100\n"
    yorum += f"--------------------------------------\n"
    yorum += f"Durustluk (Eline Sahip): {p1:.0f}\n"
    yorum += f"Iletisim (Diline Sahip): {p2:.0f}\n"
    yorum += f"Comertlik (Sofrasi Acik): {p3:.0f}\n"
    yorum += f"Sebat (Kapisi Acik): {p4:.0f}\n"
    yorum += f"--------------------------------------\n"
    yorum += f"GELISIM TAVSIYELERI:\n{tavsiye_metni}\n"

    # PDF BUTONU VE TR KARAKTER DÜZELTME
    if st.button("📄 Detaylı Raporu İndir"):
        
        # Bu fonksiyon Türkçe karakterleri İngilizceye çevirir (Hata önleyici)
        def tr_duzelt(text):
            tr_map = {
                'ğ':'g', 'Ğ':'G', 'ş':'s', 'Ş':'S', 'ı':'i', 'İ':'I',
                'ü':'u', 'Ü':'U', 'ö':'o', 'Ö':'O', 'ç':'c', 'Ç':'C'
            }
            for tr, eng in tr_map.items():
                text = text.replace(tr, eng)
            return text

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Başlık ve içeriği temizleyerek yazıyoruz
        pdf.cell(200, 10, txt=tr_duzelt("AHİ-AI GELİŞİM RAPORU"), ln=True, align='C')
        pdf.cell(200, 10, txt="OTELCILIK VE MESLEK AHLAKI", ln=True, align='C')
        pdf.ln(10)
        
        # Yorum metnindeki olası TR karakterleri de temizle
        pdf.multi_cell(0, 10, txt=tr_duzelt(yorum))
        
        # PDF Çıktısı
        pdf_content = pdf.output(dest='S').encode('latin-1', 'replace')
        b64 = base64.b64encode(pdf_content).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Ahi_Rapor_{no}.pdf">Raporu İndir (Hazır)</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.info("👈 Analize başlamak için sol menüden öğrenci seçiniz.")
