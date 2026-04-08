import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Orchid Whisper", layout="wide")

# Helper: cari file secara case-insensitive untuk publish di Linux
def find_file_case_insensitive(file_path: str) -> str | None:
    if os.path.exists(file_path):
        return file_path

    directory, filename = os.path.split(file_path)
    directory = directory or "."
    try:
        for candidate in os.listdir(directory):
            if candidate.lower() == filename.lower():
                return os.path.join(directory, candidate)
    except FileNotFoundError:
        return None
    return None

# 1. Tampilkan Banner Canva
banner_path = find_file_case_insensitive("anggrekku.png")
if banner_path:
    st.image(banner_path, use_container_width=True)

st.title("🌸 Koleksi Anggrek Mekar Shop")
st.divider()

try:
    if os.path.exists("data_anggrek1.csv"):
        df = pd.read_csv("data_anggrek1.csv", sep=';', dtype={'harga': str})

        if 'foto' not in df.columns:
            raise ValueError("Kolom 'foto' tidak ditemukan di data_anggrek1.csv")

        df = df.dropna(subset=['foto'])
        df['harga'] = (
            df['harga']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .astype(float)
            .astype(int)
        )
        
        daftar_kategori = df['kategori'].unique()
        
        for kat in daftar_kategori:
            st.header(f"🌿 Anggrek Jenis {kat.capitalize()} {'⭐ Best Seller' if kat.lower() == 'cattleya' else ''}")
            data_per_kat = df[df['kategori'] == kat]
            
            cols = st.columns(4)
            
            for index, row in data_per_kat.reset_index().iterrows():
                nama_foto = str(row['foto']).strip()
                
                with cols[index % 4]:
                    foto_path = find_file_case_insensitive(nama_foto)
                    if foto_path:
                        st.image(foto_path, use_container_width=True)
                        st.subheader(row['nama'])
                        
                        # --- HARGA & STATUS DENGAN FONT LEBIH BESAR ---
                        harga_formatted = f"{row['harga']:,}".replace(',', '.')
                        st.markdown(f"### **Rp {harga_formatted}**")
                        st.markdown(f"**Status:** {'🟢 ' if row['status'].lower() == 'tersedia' else ('🔴 ' if row['status'].lower() == 'tidak tersedia' else '')}{row['status']}")
                        if row['status'].lower() == 'tersedia':
                            st.markdown(f"**Stok:** {int(float(row['stok']))}")
                            pesan_wa = f"Halo, saya tertarik dengan {row['nama']}"
                            link_wa = f"https://wa.me/6289630516019?text={pesan_wa.replace(' ', '%20')}"
                            st.link_button("📱 Pesan Sekarang", link_wa, key=f"wa_{index}")
                        elif row['status'].lower() == 'tidak tersedia':
                            st.markdown("**Stok: Habis**")
                    else:
                        st.warning(f"Foto {nama_foto} tidak ditemukan")
            st.divider()
            
    else:
        st.error("File 'data_anggrek1.csv' tidak ditemukan!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

# --- BAGIAN KONTAK & ALAMAT (FOOTER) ---
st.write("") # Memberi ruang kosong
st.write("")
st.divider()
st.subheader("📍 Hubungi Kami")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    **Alamat Galeri:** MAN 1 YOGYAKARTA, Jl. C. Simanjuntak No.60, Terban, Kec. Gondokusuman, Kota Yogyakarta, Daerah Istimewa Yogyakarta 55223
    """)

with col_info2:
    # Ganti nomor HP di bawah ini dengan nomor Anda (gunakan format 62)
    no_hp = "6282134952220" 
    pesan_wa = "Halo, saya tertarik memesan anggrek di katalog Anda."
    link_wa = f"https://wa.me/6282134952220?text={pesan_wa.replace(' ', '%20')}"
    
    st.markdown(f"**WhatsApp: +6282134952220**")
    st.link_button("📱 Pesan Sekarang via WhatsApp", link_wa)

st.caption("© 2026 Toko green orchid - Semua Hak Dilindungi")