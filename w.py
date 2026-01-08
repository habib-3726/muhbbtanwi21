import streamlit as st
import pandas as pd
import math

# =================================================================
# 1. (MUHAMMAD HABIB THANTAWI) NGERI WAH POKOK NA 
# =================================================================

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Dashboard Listrik & PLTS - muhbbtanwi_21",
    layout="wide",
    page_icon="⚡"
)

# --- TEMA LATAR BELAKANG: SOLAR NIGHT BLUE ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
        background-attachment: fixed;
    }
    .stMarkdown, .stMetric, h1, h2, h3, p, label {
        color: #f8fafc !important;
    }
    div[data-testid="stMetricValue"] {
        color: #fbbf24 !important;
        text-shadow: 0px 0px 10px rgba(251, 191, 36, 0.4);
    }
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid #1e40af;
    }
    div[data-testid="stMetric"] {
        background: rgba(30, 58, 138, 0.3);
        border: 1px solid #1e40af;
        border-radius: 12px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= HEADER (NGERI WAH) =================
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
padding:25px;border-radius:20px;
text-align:center;border-bottom: 4px solid #fbbf24;
box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
<h1 style="margin:0; font-size:32px; color:white;">⚡ Dashboard Konsumsi Listrik & PLTS ⚙️</h1>
<div style="font-size:16px;font-weight:400;color:#cbd5e1; margin-top:5px;">
Lengkap • Fleksibel • Edukatif • Dijamin puas | By: muhbbtanwi_21
</div>
<div style="font-size:13px;font-weight:600;color:#fbbf24; letter-spacing:1px;">
(Investasi Matahari, Pangkas Tagihan Tiap Hari)
</div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🏷️ Identitas Lokasi")
    nama_lokasi = st.text_input("Nama lokasi (bebas)", "Rumah Pak Budi")

    st.header("🏗️ Tipe Sistem")
    tipe_sistem = st.selectbox("Pilih Tipe PLTS", ["Off-Grid (Baterai Full)", "On-Grid (Tanpa Baterai)", "Hybrid (Backup)"])

    st.header("⚙️ Sistem Listrik")
    tegangan = st.selectbox("Tegangan sistem (V)", [12, 24, 48])
    tarif = st.number_input("Tarif listrik PLN (Rp/kWh)", value=1444)

    st.header("🔋 Baterai")
    baterai_ah = st.number_input("Kapasitas baterai (Ah)", 0, 50000, 200)
    dod = st.slider("Depth of Discharge (aman)", 0.3, 0.8, 0.5)

    st.header("🌞 Matahari & Sistem")
    sun_hours = st.slider("Jam matahari efektif (jam/hari)", 3.0, 6.0, 4.0)
    derating = st.slider("Derating sistem", 0.6, 0.9, 0.8)

    st.header("🧩 Preset Cepat")
    preset_mode = st.selectbox(
        "Isi otomatis alat",
        ["Tidak pakai preset", "Rumah", "Masjid", "Kantor", "Fasilitas Umum", "Toko"]
    )

# ================= PRESET DATA =================
preset_data = {
    "Rumah": [
        {"nama": "Lampu", "watt": 10, "jam": 8},
        {"nama": "TV", "watt": 100, "jam": 5},
        {"nama": "Kulkas", "watt": 150, "jam": 24},
    ],
    "Masjid": [
        {"nama": "Lampu", "watt": 10, "jam": 10},
        {"nama": "Speaker", "watt": 200, "jam": 5},
        {"nama": "Kipas", "watt": 60, "jam": 6},
    ],
    "Kantor": [
        {"nama": "Lampu", "watt": 15, "jam": 9},
        {"nama": "AC", "watt": 800, "jam": 8},
        {"nama": "Komputer", "watt": 200, "jam": 8},
    ],
    "Fasilitas Umum": [
        {"nama": "Lampu Jalan PJU", "watt": 60, "jam": 12},
        {"nama": "CCTV Sistem", "watt": 25, "jam": 24},
        {"nama": "Wifi Public", "watt": 15, "jam": 24},
    ],
    "Toko": [
        {"nama": "Showcase Cooler", "watt": 250, "jam": 24},
        {"nama": "Lampu Toko", "watt": 100, "jam": 12},
        {"nama": "Mesin Kasir", "watt": 40, "jam": 12},
    ],
}

# ================= SESSION =================
if "alat" not in st.session_state:
    st.session_state.alat = []

if preset_mode != "Tidak pakai preset" and st.session_state.alat == []:
    st.session_state.alat = preset_data[preset_mode].copy()

# ================= INPUT ALAT =================
st.header("📋 Daftar Alat Listrik")

for i, alat in enumerate(st.session_state.alat):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    alat["nama"] = c1.text_input("Nama", alat["nama"], key=f"n{i}")
    alat["watt"] = c2.number_input("Watt", 1, 30000, alat["watt"], key=f"w{i}")
    alat["jam"] = c3.number_input("Jam/hari", 0.1, 24.0, float(alat["jam"]), key=f"j{i}")
    if c4.button("❌", key=f"d{i}"):
        st.session_state.alat.pop(i)
        st.rerun()

st.button(
    "➕ Tambah Alat",
    on_click=lambda: st.session_state.alat.append(
        {"nama": "Alat Baru", "watt": 100, "jam": 1}
    )
)

# ================= PERHITUNGAN ENERGI =================
energi_harian_wh = sum(a["watt"] * a["jam"] for a in st.session_state.alat)
energi_harian_kwh = energi_harian_wh / 1000
energi_bulanan_kwh = energi_harian_kwh * 30
energi_tahunan_kwh = energi_bulanan_kwh * 12

# ================= BIAYA PLN =================
biaya_harian = energi_harian_kwh * tarif
biaya_bulanan = energi_bulanan_kwh * tarif
biaya_tahunan = energi_tahunan_kwh * tarif

# ================= OUTPUT ENERGI =================
st.markdown("---")
st.header("⚡ Konsumsi Energi")

e1, e2, e3 = st.columns(3)
e1.metric("Per Hari", f"{energi_harian_kwh:.2f} kWh")
e2.metric("Per Bulan", f"{energi_bulanan_kwh:.1f} kWh")
e3.metric("Per Tahun", f"{energi_tahunan_kwh:.0f} kWh")

# ================= OUTPUT BIAYA =================
st.markdown("---")
st.header("💰 Biaya Listrik PLN")

b1, b2, b3 = st.columns(3)
b1.metric("Per Hari", f"Rp {biaya_harian:,.0f}")
b2.metric("Per Bulan", f"Rp {biaya_bulanan:,.0f}")
b3.metric("Per Tahun", f"Rp {biaya_tahunan:,.0f}")

# ================= SIMULASI PLN MATI =================
st.markdown("---")
st.header("🔌 Simulasi PLN Mati")

total_daya = sum(a["watt"] for a in st.session_state.alat)
energi_baterai = baterai_ah * tegangan * dod

backup_jam = energi_baterai / total_daya if total_daya > 0 else 0
st.success(f"Baterai bertahan ± *{backup_jam:.1f} jam* saat PLN mati.")

# ================= KEBUTUHAN PANEL =================
st.markdown("---")
st.header("🌞 Kebutuhan Panel Surya")

kebutuhan_wp = energi_harian_wh / (sun_hours * derating)
st.metric("Kebutuhan Panel Total", f"{kebutuhan_wp:.0f} Wp")

# ================= PANEL DIGUNAKAN =================
st.markdown("---")
st.header("🟦 Panel Surya yang Digunakan")

daya_panel = st.number_input("Daya 1 panel (Wp)", 100, 1000, 550)
jumlah_panel = st.number_input("Jumlah panel", 1, 200, 4)

panel_terpasang_wp = daya_panel * jumlah_panel
energi_panel_harian = panel_terpasang_wp * sun_hours * derating

status = "❌ Kurang"
if panel_terpasang_wp >= kebutuhan_wp:
    status = "✅ Cukup"
elif panel_terpasang_wp >= kebutuhan_wp * 0.9:
    status = "⚠️ Hampir cukup"

st.metric("Total Panel Terpasang", f"{panel_terpasang_wp} Wp")
st.metric("Energi Panel / Hari", f"{energi_panel_harian:.0f} Wh")
st.info(f"Status kapasitas panel: *{status}*")

# ================= ESTIMASI BIAYA PLTS =================
st.markdown("---")
st.header("🔧 Estimasi Biaya Sistem PLTS")

harga_panel_wp = st.number_input("Harga panel (Rp/Wp)", value=5500)
harga_baterai_ah = st.number_input("Harga baterai (Rp/Ah)", value=2000)
harga_inverter = st.number_input("Harga inverter (Rp)", value=5000000)
harga_scc = st.number_input("Harga SCC (Rp)", value=2000000)

biaya_panel = panel_terpasang_wp * harga_panel_wp
biaya_baterai = baterai_ah * harga_baterai_ah
total_plts = biaya_panel + biaya_baterai + harga_inverter + harga_scc

st.metric("Total Estimasi Investasi PLTS", f"Rp {total_plts:,.0f}")

payback = total_plts / biaya_tahunan if biaya_tahunan > 0 else 0
st.info(f"⏱️ Estimasi balik modal: *{payback:.1f} tahun*")

# ================= TABEL =================
st.markdown("---")
st.header("📊 Ringkasan Alat")

df = pd.DataFrame(st.session_state.alat)
if not df.empty:
    df["Energi Harian (Wh)"] = df["watt"] * df["jam"]
    st.dataframe(df, use_container_width=True)
    
    # --- TAMBAHAN 1: RINGKASAN TOTAL ALAT ---
    c_tot1, c_tot2, c_tot3 = st.columns(3)
    c_tot1.metric("Total Daya", f"{df['watt'].sum()} W")
    c_tot2.metric("Total Jam", f"{df['jam'].sum():.1f} Jam")
    c_tot3.metric("Total Wh/Hari", f"{df['Energi Harian (Wh)'].sum():.0f} Wh")

# ================= KESIMPULAN =================
st.markdown("---")
st.success(f"""
### 📌 Kesimpulan Sistem

- Lokasi: *{nama_lokasi}*
- Konsumsi: *{energi_bulanan_kwh:.1f} kWh/bulan*
- Biaya PLN: *Rp {biaya_bulanan:,.0f}/bulan*
- Panel terpasang: *{panel_terpasang_wp} Wp*
- Status panel: *{status}*
- Backup PLN mati: *{backup_jam:.1f} jam*
- Investasi PLTS: *Rp {total_plts:,.0f}*
""")

# --- TAMBAHAN 2: PROYEKSI 10 TAHUN & TOTAL HEMAT ---
st.markdown("---")
st.header("📈 Proyeksi Finansial 10 Tahun")
tahun_list = list(range(1, 11))
akum_pln = [biaya_tahunan * t * (1.03**(t-1)) for t in tahun_list]
akum_plts = [total_plts + (total_plts * 0.01 * t) for t in tahun_list]
df_pro = pd.DataFrame({"Tahun": tahun_list, "Tagihan PLN": akum_pln, "Investasi PLTS": akum_plts})
st.line_chart(df_pro.set_index("Tahun"))

# METRIK TAMBAHAN: TOTAL PROYEKSI 10 TAHUN
c_pro1, c_pro2, c_pro3 = st.columns(3)
total_pln_10th = sum([biaya_tahunan * (1.03**i) for i in range(10)])
total_hemat_10th = total_pln_10th - total_plts
c_pro1.metric("Total PLN (10 Thn)", f"Rp {total_pln_10th:,.0f}")
c_pro2.metric("Investasi PLTS", f"Rp {total_plts:,.0f}")
c_pro3.metric("Total Hemat (10 Thn)", f"Rp {total_hemat_10th:,.0f}")

# ================= RAB DINAMIS =================
st.markdown("---")
st.header(f"🧾 Rincian Anggaran (RAB) - {tipe_sistem}")

if "On-Grid" in tipe_sistem:
    biaya_baterai_final = 0
    kapasitas_baterai_tampil = "0 Ah (On-Grid)"
    biaya_scc_final = 0
    inverter_type = "On-Grid Tie Inverter"
else:
    biaya_baterai_final = biaya_baterai
    kapasitas_baterai_tampil = f"{baterai_ah} Ah"
    biaya_scc_final = harga_scc
    inverter_type = "Off-Grid/Hybrid Inverter"

# --- TAMBAHAN 3: BARIS TOTAL RAB ---
total_seluruh_rab = biaya_panel + biaya_baterai_final + harga_inverter + biaya_scc_final + 1500000
rab_data = {
    "Komponen": ["Panel Surya", "Baterai", "Inverter", "SCC", "Kabel & Jasa", "TOTAL INVESTASI"],
    "Spesifikasi": [f"{jumlah_panel}x {daya_panel}Wp", kapasitas_baterai_tampil, inverter_type, "MPPT Controller", "Sistem Set", "-"],
    "Harga": [f"Rp {biaya_panel:,.0f}", f"Rp {biaya_baterai_final:,.0f}", f"Rp {harga_inverter:,.0f}", f"Rp {biaya_scc_final:,.0f}", "Rp 1,500,000", f"Rp {total_seluruh_rab:,.0f}"]
}
st.table(pd.DataFrame(rab_data))

# ================= DETAIL RANGKAIAN TEKNIS =================
st.markdown("---")
st.header("🔍 Detail Teknis Rangkaian")

c_t1, c_t2 = st.columns(2)
with c_t1:
    s_bat = math.ceil(tegangan / 3.2) # Contoh sel LFP 3.2V
    st.subheader("🔋 Rangkaian Baterai")
    st.write(f"Untuk tegangan **{tegangan}V**, gunakan rangkaian: **{s_bat} Seri**.")
    st.info("Pastikan menggunakan BMS untuk memantau kesehatan tiap sel.")

with c_t2:
    arus_mppt = (panel_terpasang_wp / tegangan) * 1.25
    st.subheader("📟 Rekomendasi SCC")
    st.write(f"Kapasitas arus minimal: **{arus_mppt:.1f} Ampere**.")
    st.write(f"Saran: Gunakan SCC MPPT **{math.ceil(arus_mppt/10)*10}A**.")

# ================= ANALISIS TAMBAHAN =================
st.markdown("---")
st.header("📊 Detail Analisis Tambahan")

total_jam_nyala = sum(a["jam"] for a in st.session_state.alat)

c1_ext, c2_ext = st.columns(2)
with c1_ext:
    st.subheader("⏱️ Durasi Penggunaan")
    st.metric("Total Waktu Nyala Seluruh Alat", f"{total_jam_nyala:.1f} Jam/Hari")

with c2_ext:
    saran_watt_inverter = math.ceil((total_daya * 1.3) / 100) * 100
    st.subheader("📟 Rekomendasi Perangkat")
    st.success(f"Gunakan Inverter minimal: **{saran_watt_inverter} Watt**")

# ================= GRAFIK & EDUKASI =================
if not df.empty:
    st.markdown("---")
    st.subheader("📈 Grafik Beban per Alat (Wh)")
    
    # --- TAMBAHAN BAGIAN GRAFIK ---
    c_graph1, c_graph2 = st.columns(2)
    total_beban = df['watt'].sum()
    total_biaya_per_jam_grafik = (total_beban / 1000) * tarif
    
    c_graph1.metric("Total Beban Keseluruhan", f"{total_beban} Watt")
    c_graph2.metric("Estimasi Biaya PLN/Jam", f"Rp {total_biaya_per_jam_grafik:,.0f}/jam")

    df_chart = df.copy()
    df_chart["Wh"] = df_chart["watt"] * df_chart["jam"]
    st.bar_chart(data=df_chart, x="nama", y="Wh")

st.markdown("---")
st.header("📖 Edukasi & Skema")



col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    st.write("**On-Grid**")
    st.caption("Tanpa baterai. Listrik panel langsung dipakai atau dijual ke PLN. Hemat biaya bulanan.")
with col_e2:
    st.write("**Off-Grid**")
    st.caption("Pakai baterai. Mandiri tanpa PLN. Cocok untuk kebun atau daerah pelosok.")
with col_e3:
    st.write("**Hybrid**")
    st.caption("Pakai baterai + PLN. Tetap nyala saat mati lampu dan tetap hemat tagihan.")

# ================= FOOTER IDENTITAS =================
st.markdown("---")
st.markdown(f"""
<div style="background-color:rgba(255, 255, 255, 0.05); padding:20px; border-radius:15px; text-align:center; border: 1px solid #fbbf24; margin-top:50px; margin-bottom:50px;">
    <h3 style="margin:0; color:#fbbf24;">🛠️ Dikelola oleh: muhbbtanwi_21</h3>
    <p style="margin:5px 0; color:#e6f1ff;">Ahli Konsultan Energi & PLTS</p>
    <a href="https://wa.me/628563844635" style="text-decoration:none;">
        <div style="background-color:#25d366; color:white; padding:10px 20px; border-radius:10px; display:inline-block; font-weight:bold; margin-top:10px;">
            💬 Hubungi saya (WA): 0856-3844-635
        </div>
    </a>
</div>
""", unsafe_allow_html=True)