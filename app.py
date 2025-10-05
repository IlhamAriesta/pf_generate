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
    df.columns = df.columns.str.upper()
    for col in ["PIT", "LOKASI", "SEAM"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
except Exception as e:
    st.error(f"⚠️ Gagal membaca file database_pf.xlsx: {e}")
    st.stop()

# ====================== MENU =============================
menu = st.radio("Pilih Menu", ["PF Generator", "PF Generator Massal", "Perhitungan Hole"])

# ====================== PF GENERATOR =====================
if menu == "PF Generator":
    st.subheader("📝 INPUT PF GENERATOR")

    pit = st.selectbox("Pilih PIT", sorted(df["PIT"].unique()))
    lokasi_options = sorted(df[df["PIT"] == pit]["LOKASI"].unique())
    lokasi = st.selectbox("Pilih LOKASI", lokasi_options)
    seam_options = sorted(df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi)]["SEAM"].unique())
    seam = st.selectbox("Pilih SEAM", seam_options)

    jumlah_lubang = st.number_input("Jumlah Lubang", min_value=1, step=1)
    kedalaman = st.number_input("Kedalaman (m)", min_value=1.0, step=0.1)

    if st.button("🚀 AUTO GENERATE PF"):
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

# ====================== PF GENERATOR MASSAL =====================
elif menu == "PF Generator Massal":
    st.subheader("📝 PF GENERATOR MASSAL (MULTI PIT/LOKASI/SEAM)")

    # Multiselect PIT
    pit_selected = st.multiselect("Pilih PIT", sorted(df["PIT"].unique()))
    
    # Loop per PIT untuk pilih LOKASI dan SEAM
    selection_list = []
    for pit in pit_selected:
        lokasi_options = sorted(df[df["PIT"] == pit]["LOKASI"].unique())
        lokasi_selected = st.multiselect(f"Pilih LOKASI untuk {pit}", lokasi_options)

        for lokasi in lokasi_selected:
            seam_options = sorted(df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi)]["SEAM"].unique())
            seam_selected = st.multiselect(f"Pilih SEAM untuk {pit} - {lokasi}", seam_options)

            for seam in seam_selected:
                selection_list.append((pit, lokasi, seam))

    if st.button("🚀 GENERATE MASSAL"):
        results = []
        for pit, lokasi, seam in selection_list:
            row_db = df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi) & (df["SEAM"] == seam)]
            if not row_db.empty:
                pf = float(row_db["PF"].iloc[0])
                spasi = float(row_db["SPASI"].iloc[0])
                burden = float(row_db["BURDEN"].iloc[0])
                results.append([pit, lokasi, seam, spasi, burden, pf])
            else:
                results.append([pit, lokasi, seam, "-", "-", "-"])

        df_result = pd.DataFrame(results, columns=["PIT","LOKASI","SEAM","SPASI","BURDEN","PF"])
        st.success("✅ Perhitungan Massal Berhasil!")
        st.dataframe(df_result)

        # Copy/Share
        csv_text = df_result.to_csv(index=False)
        st.text_area("Copy hasil di bawah untuk WhatsApp", csv_text, height=300)



# ====================== PERHITUNGAN HOLE =====================
else:
    st.subheader("📝 INPUT PERHITUNGAN HOLE")

    pit = st.selectbox("Pilih PIT", sorted(df["PIT"].unique()))
    panjang = st.number_input("Panjang Lokasi (m)", min_value=1.0, step=1.0)
    lebar = st.number_input("Lebar Lokasi (m)", min_value=1.0, step=1.0)
    fleet_unit = st.selectbox("Plan Fleet Loading", ["PC1250", "PC2000", "PC2600"])
    kedalaman = st.number_input("Kedalaman Rata-rata (m)", min_value=1.0, step=0.1)

    if st.button("🚀 HITUNG HOLE"):
        row = df[df["PIT"] == pit]
        if row.empty:
            st.error("⚠️ Data Pit tidak ditemukan!")
        else:
            spasi = float(row["SPASI"].mean())
            burden = float(row["BURDEN"].mean())

            jumlah_row = lebar / burden
            jumlah_lubang = (lebar * panjang) / (spasi * burden)

            fleet_vol = {"PC1250": 23940, "PC2000": 36540, "PC2600": 56700}
            kebutuhan_lubang_fleet = fleet_vol[fleet_unit] / (spasi * burden * kedalaman)

            st.markdown("---")
            st.success("✅ Perhitungan Hole Berhasil")
            st.markdown(f"""
            <div style="font-size:20px; line-height:1.6;">
            <b>PIT</b> : {pit}<br>
            <b>Panjang Lokasi</b> : {panjang} m<br>
            <b>Lebar Lokasi</b> : {lebar} m<br>
            <b>Fleet Unit</b> : {fleet_unit}<br><br>
            <b>Spasi</b> : {spasi} m<br>
            <b>Burden</b> : {burden} m<br>
            <b>Jumlah Row</b> : {jumlah_row:.2f} row<br>
            <b>Jumlah Lubang</b> : {jumlah_lubang:.2f} lubang<br>
            <b>Kebutuhan Lubang untuk Fleet</b> : {kebutuhan_lubang_fleet:.2f} lubang
            </div>
            """, unsafe_allow_html=True)


