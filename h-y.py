import streamlit as st
import pandas as pd
import math

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Solar Optimizer Pro - muhbbtanwi_21",
    layout="wide",
    page_icon="☀️"
)

# --- CUSTOM CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
        background-attachment: fixed;
    }
    .stMarkdown, .stMetric, h1, h2, h3, p, label { color: #f8fafc !important; }
    div[data-testid="stMetricValue"] { color: #fbbf24 !important; text-shadow: 0px 0px 10px rgba(251, 191, 36, 0.4); }
    div[data-testid="stMetric"] {
        background: rgba(30, 58, 138, 0.2);
        border: 1px solid #1e40af;
        border-radius: 12px;
        padding: 20px;
    }
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding:30px; border-radius:20px; text-align:center;
        border-bottom: 4px solid #fbbf24; box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= HEADER =================
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size:36px; letter-spacing: 2px;">⚡SISTEM OPTIMASI & SIMULASI PLTS TERPADU⚙️</h1>
    <div style="font-size:16px; color:#cbd5e1; margin-top:10px;">
        Sistem Perancangan Teknis & Penghematan listrik | By: muhbbtanwi_21
     <div style="font-size:13px; color:#cbd5e1; margin-top:10px;">
     (investasi matahari-pangkas uang setiap hari)
</div>
""", unsafe_allow_html=True)

# ================= SECTION 1: KONFIGURASI UTAMA =================
st.header("🏗️ 1. Pengaturan Lokasi & Sistem")
col_cfg1, col_cfg2, col_cfg3 = st.columns(3)

with col_cfg1:
    nama_lokasi = st.text_input("Nama Proyek/Rumah", "Instalasi Rumah Utama")
    tipe_sistem = st.selectbox("Tipe Sistem", ["Off-Grid (Pakai Baterai)", "On-Grid (Tanpa Baterai)", "Hybrid (Cadangan + Baterai)"])
    tarif = st.number_input("Harga Listrik per kWh (Rp)", value=1444)

with col_cfg2:
    tegangan = st.selectbox("Tegangan Sistem (Volt DC)", [12, 24, 48])
    jenis_inverter = st.selectbox("Tipe Inverter", ["Pure Sine Wave (PSW)", "Hybrid Inverter", "String Inverter", "Modified Sine Wave"])
    jenis_baterai = st.selectbox("Jenis Baterai", ["Lithium (Awet & Modern)", "Gel / AGM", "Lead Acid (Standar)"])

with col_cfg3:
    baterai_ah = st.number_input("Kapasitas Baterai (Ah)", 0, 50000, 200)
    sun_hours = st.slider("Lama Matahari Terik (Jam/Hari)", 3.0, 6.0, 4.0)
    # PILIHAN JENIS KABEL (Dropdown)
    jenis_kabel_pv = st.selectbox("Pilih Ukuran Kabel PV (DC)", ["PV1-F 4mm²", "PV1-F 6mm²", "PV1-F 10mm²"])

# ================= SECTION 2: BEBAN & ENERGI =================
st.markdown("---")
st.header("📊 2. Target Pemakaian Listrik")
col_load1, col_load2 = st.columns(2)
with col_load1:
    total_daya_beban = st.number_input("Total Beban Alat Elektronik (Watt)", value=1000)
    energi_harian_kwh = st.number_input("Target Listrik Harian (kWh/Hari)", value=5.0)
with col_load2:
    biaya_pln_bulanan = energi_harian_kwh * 30 * tarif
    st.write("### Potensi Tabungan Bulanan")
    st.metric("Tagihan PLN yang Terpangkas", f"Rp {biaya_pln_bulanan:,.0f} /Bulan")

# ================= SECTION 3: PERANCANGAN TEKNIS PV =================
st.markdown("---")
st.header("☀️ 3. Kebutuhan Panel Surya")
derating = 0.8
kebutuhan_wp = (energi_harian_kwh * 1000) / (sun_hours * derating)
col_pv1, col_pv2 = st.columns(2)
with col_pv1:
    daya_panel_satuan = st.number_input("Ukuran 1 Keping Panel (Wp)", 100, 700, 550)
    jumlah_panel = st.number_input("Jumlah Keping Panel Dipasang", 1, 500, 4)
    panel_terpasang_wp = daya_panel_satuan * jumlah_panel
    st.metric("Total Kapasitas Panel", f"{panel_terpasang_wp} Wp")
with col_pv2:
    status = "✅ Cukup & Aman" if panel_terpasang_wp >= kebutuhan_wp else "⚠️ Perlu Ditambah"
    st.info(f"Saran Minimal: {kebutuhan_wp:.0f} Wp")
    st.success(f"Kondisi Saat Ini: {status}")

# ================= SECTION 4: FINANCIAL & RAB =================
st.markdown("---")
st.header("💰 4. Rincian Biaya (RAB)")
col_fin1, col_fin2 = st.columns(2)
with col_fin1:
    st.subheader("Input Harga Satuan")
    harga_pv_wp = st.number_input("Harga Panel (Rp/Wp)", value=5500)
    def_h_bat = 15000 if "Lithium" in jenis_baterai else 4500
    harga_bat_ah = st.number_input("Harga Baterai (Rp/Ah)", value=def_h_bat)
    harga_inv_unit = st.number_input("Harga Inverter", value=7000000)
    # Harga kabel menyesuaikan pilihan
    harga_kabel_per_m = 15000 if "4mm²" in jenis_kabel_pv else (25000 if "6mm²" in jenis_kabel_pv else 40000)
    biaya_kabel_total = st.number_input("Estimasi Biaya Kabel & Jasa", value=int(harga_kabel_per_m * 20 + 1500000))

biaya_pv_total = panel_terpasang_wp * harga_pv_wp
biaya_bat_total = (baterai_ah * harga_bat_ah) if "On-Grid" not in tipe_sistem else 0
total_rab = biaya_pv_total + biaya_bat_total + harga_inv_unit + biaya_kabel_total

with col_fin2:
    rab_data = {
        "Daftar Barang": ["Panel Surya", "Baterai", "Inverter", f"Kabel ({jenis_kabel_pv}) & Jasa"],
        "Biaya": [f"Rp {biaya_pv_total:,.0f}", f"Rp {biaya_bat_total:,.0f}", f"Rp {harga_inv_unit:,.0f}", f"Rp {biaya_kabel_total:,.0f}"]
    }
    st.table(pd.DataFrame(rab_data))
    st.metric("TOTAL MODAL AWAL", f"Rp {total_rab:,.0f}")

# ================= SECTION 5: ANALISIS TEKNIS KABEL =================
st.markdown("---")
st.header("🔍 5. Analisis Kesesuaian Kabel")

# Perhitungan arus untuk validasi pilihan pengguna
arus_dc = panel_terpasang_wp / tegangan
arus_maks_kabel = 35 if "4mm²" in jenis_kabel_pv else (50 if "6mm²" in jenis_kabel_pv else 70)

col_kbl1, col_kbl2 = st.columns(2)
with col_kbl1:
    st.subheader("Validasi Arus")
    st.write(f"Pilihan Anda: **{jenis_kabel_pv}**")
    st.write(f"Arus Panel ke Inverter: **{arus_dc:.1f} Ampere**")
    
    if arus_dc > arus_maks_kabel:
        st.error(f"⚠️ Bahaya! Arus ({arus_dc:.1f}A) melebihi kapasitas {jenis_kabel_pv}. Silakan pilih ukuran lebih besar.")
    else:
        st.success(f"✅ Aman. Kabel {jenis_kabel_pv} mampu menangani arus {arus_dc:.1f}A.")

with col_kbl2:
    st.subheader("Informasi Material")
    st.write("• Jenis: PV1-F (Double Insulated)")
    st.write("• Standar: TUV/UL Solar Cable")
    st.write("• Ketahanan: Tahan Sinar UV & Suhu Tinggi (Roof-top Ready)")

# ================= SECTION 6: PROYEKSI PENGHEMATAN =================
st.markdown("---")
st.header("📈 6. Analisis Balik Modal")
masa_pakai_thn = 25
kenaikan_listrik = 0.05
biaya_pln_setahun = biaya_pln_bulanan * 12
total_ke_pln = 0
data_proyeksi = []

for t in range(1, masa_pakai_thn + 1):
    total_ke_pln += biaya_pln_setahun
    saving = total_ke_pln - total_rab
    data_proyeksi.append({"Tahun": t, "Tabungan": saving if saving > 0 else 0})
    biaya_pln_setahun *= (1 + kenaikan_listrik)

roi_tahun = total_rab / (biaya_pln_bulanan * 12) if biaya_pln_bulanan > 0 else 0
s1, s2, s3 = st.columns(3)
s1.metric("Kapan Balik Modal?", f"{roi_tahun:.1f} Tahun")
s2.metric("Total Hemat (25 Thn)", f"Rp {total_ke_pln - total_rab:,.0f}")
s3.metric("Keuntungan", f"{(total_ke_pln/total_rab):.1f}x Lipat")

st.area_chart(pd.DataFrame(data_proyeksi).set_index("Tahun"))

# ================= SECTION 7: KESIMPULAN FINAL =================
st.markdown("---")
st.header("📝 Kesimpulan Untuk Klien")
sum1, sum2 = st.columns(2)
with sum1:
    st.info(f"""
    ### 🛡️ Keamanan & Kualitas
    1. **Pilihan Kabel:** Anda telah memilih **{jenis_kabel_pv}**, pastikan spesifikasi fisik sesuai standar TUV.
    2. **Proteksi:** Wajib pasang Arrester Petir mengingat panel berada di titik tertinggi bangunan.
    3. **Durabilitas:** Sistem dirancang untuk bertahan hingga 25 tahun dengan perawatan minimal.
    """)
with sum2:
    st.success(f"""
    ### 💰 Ringkasan Keuntungan
    * **Modal Anda:** Rp {total_rab:,.0f}
    * **Listrik Gratis:** Mulai Tahun ke-{roi_tahun:.1f}
    * **Total Uang Diselamatkan:** **Rp {total_ke_pln - total_rab:,.0f}**
    
    Investasi ini memberikan kebebasan energi dan perlindungan dari kenaikan tarif listrik di masa depan.
    """)

# ================= FOOTER =================
st.markdown("---")
st.markdown(f"""
<div style="background-color:rgba(255, 255, 255, 0.05); padding:30px; border-radius:15px; text-align:center; border: 1px solid #fbbf24;">
    <h3 style="margin:0; color:#fbbf24;">Laporan Analisis: {nama_lokasi}</h3>
    <p style="color:#cbd5e1;">Consultant plts: muhbbtanwi_21 
    <div style="margin-top:10px;">
        <a href="https://wa.me/628563844635" target="_blank" style="background-color:#25d366; color:white; padding:10px 25px; border-radius:50px; text-decoration:none; font-weight:bold; display:inline-block;">
            💬 wa:628563844635
        </a>
    </div>
</div>
""", unsafe_allow_html=True)