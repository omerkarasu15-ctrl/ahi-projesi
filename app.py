import streamlit as st
import base64
from fpdf import FPDF

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ahi-AI Değerlendirme v2", page_icon="⚖️")

st.title("⚖️ Ahi-AI: Kriter Bazlı Değerlendirme")
st.markdown("**Turizm ve Otelcilik - Ahilik Değerleri Davranış Göstergeleri**")

# --- SOL MENÜ: ÖĞRENCİ BİLGİLERİ ---
with st.sidebar:
    st.header("Öğrenci Bilgileri")
    ad = st.text_input("Ad Soyad")
    no = st.text_input("Okul No")
    sinif = st.selectbox("Sınıf", ["9-A", "10-B", "11-C", "12-D"])

# --- FONKSİYON: SORU SOR VE PUAN HESAPLA ---
def soru_sor(soru_metni):
    secim = st.radio(
        soru_metni,
        ["Tam Gösteriyor (100p)", "Kısmen Gösteriyor (50p)", "Geliştirilmeli (0p)"],
        key=soru_metni
    )
    if "Tam" in secim: return 100
    elif "Kısmen" in secim: return 50
    else: return 0

# --- ANA FORM: DETAYLI KRİTERLER ---
if ad and no:
    st.markdown("---")
    
    # 1. BÖLÜM: DÜRÜSTLÜK VE GÜVEN
    st.subheader("1. Dürüstlük ve İş Ahlakı (El)")
    p1_a = soru_sor("Hata yaptığında dürüstçe kabul edip sorumluluk alıyor mu?")
    p1_b = soru_sor("Kurumun malzemesini (demirbaş/gıda) israf etmeden kullanıyor mu?")
    p1 = (p1_a + p1_b) / 2 

    st.markdown("---")

    # 2. BÖLÜM: CÖMERTLİK VE HİZMET
    st.subheader("2. Cömertlik ve Hizmet Bilinci (Sofrası Açık)")
    p2_a = soru_sor("Bilgisini ve tecrübesini arkadaşlarıyla paylaşıyor mu?")
    p2_b = soru_sor("Misafire/Müşteriye karşılık beklemeden güler yüzle hizmet ediyor mu?")
    p2 = (p2_a + p2_b) / 2

    st.markdown("---")

    # 3. BÖLÜM: SAYGI VE HİYERARŞİ
    st.subheader("3. Saygı ve Hiyerarşi (Usta-Çırak)")
    p3_a = soru_sor("Usta öğreticilerine ve şeflerine karşı saygılı mı?")
    p3_b = soru_sor("Verilen talimatları eksiksiz ve zamanında yerine getiriyor mu?")
    p3 = (p3_a + p3_b) / 2

    st.markdown("---")

    # 4. BÖLÜM: SABIR VE SEBAT
    st.subheader("4. Sabır ve Kriz Yönetimi")
    p4_a = soru_sor("Yoğun iş temposunda veya zor müşteride sakinliğini koruyor mu?")
    p4_b = soru_sor("Başladığı işi yarım bırakmadan sonuna kadar götürüyor mu?")
    p4 = (p4_a + p4_b) / 2

    st.markdown("---")

    # SONUÇ HESAPLAMA (100'lük Sistem)
    genel_ort = (p1 + p2 + p3 + p4) / 4

    # Renkli Sonuç Kutusu
    if genel_ort >= 85: 
        st.success(f"🏆 MÜKEMMEL - Usta Adayı (Puan: {genel_ort:.0f})")
        sonuc_mesaji = "USTA ADAYI (Mukemmel)"
    elif genel_ort >= 60: 
        st.warning(f"🔨 GELİŞİYOR - Kalfa Adayı (Puan: {genel_ort:.0f})")
        sonuc_mesaji = "KALFA ADAYI (Iyi)"
    else: 
        st.error(f"🌱 BAŞLANGIÇ - Yamak (Puan: {genel_ort:.0f})")
        sonuc_mesaji = "YAMAK (Gelisim Gerekli)"

    # PDF OLUŞTURMA
    yorum = f"Sayin {ad} ({no}), Ahi-AI Degerlendirme Sonucu:\n\n"
    yorum += f"Genel Ahilik Puani: {genel_ort:.0f} / 100\n"
    yorum += f"Durustluk: {p1:.0f} - Comertlik: {p2:.0f}\n"
    yorum += f"Saygi: {p3:.0f} - Sabir: {p4:.0f}\n\n"
    yorum += f"SONUC: {sonuc_mesaji}\n"

    if st.button("Sonuç Raporunu PDF İndir"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="AHI-AI DEGERLENDIRME RAPORU", ln=True, align='C')
        pdf.cell(200, 10, txt="------------------------------------------------", ln=True, align='C')
        pdf.multi_cell(0, 10, txt=yorum)
        
        pdf_content = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_content).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Ahi_Rapor_{no}.pdf">📄 PDF Dosyasını İndir</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.info("👈 Lütfen sol menüden öğrenci bilgilerini giriniz.")
