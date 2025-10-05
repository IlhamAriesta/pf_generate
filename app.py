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

# ====================== PF GENERATOR MASSAL OPSIONAL =====================
elif menu == "PF Generator Massal":
    st.subheader("📝 PF GENERATOR MASSAL (Tambahkan Lokasi Satu per Satu)")

    # Inisialisasi session state untuk menyimpan lokasi sementara
    if "massal_list" not in st.session_state:
        st.session_state.massal_list = []

    pit = st.selectbox("Pilih PIT", sorted(df["PIT"].unique()))
    lokasi_options = sorted(df[df["PIT"] == pit]["LOKASI"].unique())
    lokasi = st.selectbox("Pilih LOKASI", lokasi_options)
    seam_options = sorted(df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi)]["SEAM"].unique())
    seam = st.selectbox("Pilih SEAM", seam_options)

    if st.button("➕ Tambahkan Lokasi"):
        row_db = df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi) & (df["SEAM"] == seam)]
        if not row_db.empty:
            spasi = float(row_db["SPASI"].iloc[0])
            burden = float(row_db["BURDEN"].iloc[0])
            pf = float(row_db["PF"].iloc[0])
            st.session_state.massal_list.append([pit, lokasi, seam, spasi, burden, pf])
            st.success(f"✅ Lokasi {lokasi} - {seam} ditambahkan!")
        else:
            st.error("⚠️ Data tidak ditemukan di database!")

    if st.session_state.massal_list:
        st.markdown("### Daftar Lokasi yang Ditambahkan")
        df_result = pd.DataFrame(st.session_state.massal_list, columns=["PIT","LOKASI","SEAM","SPASI","BURDEN","PF"])
        st.dataframe(df_result)

        if st.button("🚀 Generate Semua"):
            st.success("✅ Hasil Gabungan")

            # Kelompokkan per PIT
            from collections import defaultdict
            pit_dict = defaultdict(list)
            for row in st.session_state.massal_list:
                pit, lokasi, seam, spasi, burden, pf = row
                # Gabungkan LOKASI + SEAM sebagai nama lokasi
                full_name = f"{seam}"  # bisa juga f"{lokasi} - {seam}" jika mau
                pit_dict[pit].append((full_name, spasi, burden, pf))

            # Format teks copyable
            text_output = ""
            for pit, entries in pit_dict.items():
                text_output += f"*{pit}*\n"
                for full_name, spasi, burden, pf in entries:
                    text_output += f"- {full_name}\n- SPASI: {spasi}\n- BURDEN: {burden}\n- PF: {pf}\n\n"

            st.text_area("Copy hasil di bawah untuk WhatsApp", text_output.strip(), height=400)


# ====================== PF GENERATOR MASSAL OPSIONAL =====================
elif menu == "PF Generator Massal":
    st.subheader("📝 PF GENERATOR MASSAL (Tambahkan Lokasi Satu per Satu)")

    # Inisialisasi session state untuk menyimpan lokasi sementara
    if "massal_list" not in st.session_state:
        st.session_state.massal_list = []

    pit = st.selectbox("Pilih PIT", sorted(df["PIT"].unique()))
    lokasi_options = sorted(df[df["PIT"] == pit]["LOKASI"].unique())
    lokasi = st.selectbox("Pilih LOKASI", lokasi_options)
    seam_options = sorted(df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi)]["SEAM"].unique())
    seam = st.selectbox("Pilih SEAM", seam_options)

    if st.button("➕ Tambahkan Lokasi"):
        row_db = df[(df["PIT"] == pit) & (df["LOKASI"] == lokasi) & (df["SEAM"] == seam)]
        if not row_db.empty:
            spasi = float(row_db["SPASI"].iloc[0])
            burden = float(row_db["BURDEN"].iloc[0])
            pf = float(row_db["PF"].iloc[0])
            st.session_state.massal_list.append([pit, lokasi, seam, spasi, burden, pf])
            st.success(f"✅ Lokasi {lokasi} - {seam} ditambahkan!")
        else:
            st.error("⚠️ Data tidak ditemukan di database!")

    if st.session_state.massal_list:
        st.markdown("### Daftar Lokasi yang Ditambahkan")
        df_result = pd.DataFrame(st.session_state.massal_list, columns=["PIT","LOKASI","SEAM","SPASI","BURDEN","PF"])
        st.dataframe(df_result)

        if st.button("🚀 Generate Semua"):
            st.success("✅ Hasil Gabungan")

            # Kelompokkan per PIT
            from collections import defaultdict
            pit_dict = defaultdict(list)
            for row in st.session_state.massal_list:
                pit, lokasi, seam, spasi, burden, pf = row
                pit_dict[pit].append((seam, spasi, burden, pf))

            # Format teks copyable
            text_output = ""
            for pit, entries in pit_dict.items():
                text_output += f"*{pit}*\n"
                for seam, spasi, burden, pf in entries:
                    text_output += f"- {seam}\n- SPASI: {spasi}\n- BURDEN: {burden}\n- PF: {pf}\n\n"

            st.text_area("Copy hasil di bawah untuk WhatsApp", text_output.strip(), height=400)



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



