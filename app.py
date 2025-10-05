import streamlit as st
import pandas as pd

# ====================== CONFIG PAGE ======================
st.set_page_config(page_title="Drill Blast INDE - PT KPP", page_icon="🚀", layout="centered")

# ====================== HEADER ============================
st.image("logo.png", width=200)
st.markdown("<h1 style='text-align:center; color:#004080;'>DRILL BLAST INDE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>PT KALIMANTAN PRIMA PERSADA</h3>", unsafe_allow_html=True)
st.markdown("---")

# ====================== LOAD DATABASE =====================
try:
    df = pd.read_excel("database_pf.xlsx", sheet_name="database_pf")

    # Normalisasi kolom
    df.columns = df.columns.str.upper()
    for col in ["PIT", "LOKASI", "SEAM"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
except Exception as e:
    st.error(f"⚠️ Gagal membaca file database_pf.xlsx: {e}")
    st.stop()

# ====================== FORM INPUT ========================
st.subheader("📝 INPUT")

# PIT
pit = st.selectbox("Pilih PIT", sorted(df["PIT"].unique()))

# LOKASI
lokasi_options = sorted(df[df["PIT"] == pit]["LOKASI"].unique())
lokasi = st.selectbox("Pilih LOKASI", lokasi_options)

# SEAM
seam_options = sorted(df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi)]["SEAM"].unique())
seam = st.selectbox("Pilih SEAM", seam_options)

# JUMLAH LUBANG & KEDALAMAN
jumlah_lubang = st.number_input("Jumlah Lubang", min_value=1, step=1)
kedalaman = st.number_input("Kedalaman (m)", min_value=1.0, step=0.1)

# ====================== HITUNG ============================
if st.button("🚀 AUTO GENERATE"):
    row = df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi) & (df["SEAM"] == seam)]
    if row.empty:
        st.error("⚠️ Data tidak ditemukan di database!")
    else:
        pf = float(row["PF"].iloc[0])
        spasi = float(row["SPASI"].iloc[0])
        burden = float(row["BURDEN"].iloc[0])
        volume = spasi * burden * kedalaman * jumlah_lubang

        st.markdown("---")
        st.success("✅ Perhitungan Berhasil")
        st.markdown(f"""
        <div style="font-size:22px; line-height:1.6;">
        <b>PIT</b> : {pit}<br>
        <b>LOKASI</b> : {lokasi} {seam}<br><br>
        <b>PF</b> : {pf}<br>
        <b>SPASI</b> : {spasi}<br>
        <b>BURDEN</b> : {burden}<br><br>
        <b>VOLUME</b> : <span style="color:#E94560;">{volume:,.2f} m³</span>
        </div>
        """, unsafe_allow_html=True)
