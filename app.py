import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Konfigurasi Halaman UI
st.set_page_config(page_title="Multi-Stock Keyworder AI", layout="wide")

st.title("📸 AI Multi-Keyworder Adobe Stock")
st.write("Unggah banyak gambar sekaligus dan dapatkan metadata khusus untuk masing-masing foto.")

# Sidebar untuk Konfigurasi
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")
    st.markdown("[Dapatkan API Key baru di sini](https://aistudio.google.com/app/apikey)")
    
    # Pilihan Model (Gunakan 1.5 Flash karena paling cepat untuk gambar)
    model_name = 'gemini-3.5-flash' 
    
    st.info("Saran: Gunakan API Key yang baru saja Anda buat ulang.")

# Area Upload Multi-Gambar
uploaded_files = st.file_uploader(
    "Pilih satu atau beberapa gambar...", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Total gambar diunggah: {len(uploaded_files)}")
    
    # Tombol untuk memproses semua gambar sekaligus
    start_all = st.button("Generate Metadata untuk Semua Gambar", type="primary")

    if start_all:
        if not api_key:
            st.error("⚠️ Silakan masukkan API Key di sidebar!")
        else:
            try:
                # Inisialisasi AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)

                # Loop melalui setiap file yang diunggah
                for index, uploaded_file in enumerate(uploaded_files):
                    # Membuat baris baru untuk setiap gambar
                    with st.container():
                        st.markdown(f"### Gambar {index + 1}: {uploaded_file.name}")
                        
                        # Membagi layar menjadi 2 kolom (Kiri: Gambar, Kanan: Metadata)
                        col1, col2 = st.columns([1, 2])
                        
                        img = Image.open(uploaded_file)
                        with col1:
                            st.image(img, use_column_width=True)
                        
                        with col2:
                            with st.spinner(f"Menganalisis gambar {index + 1}..."):
                                # Prompt khusus Adobe Stock
                                prompt = """
                                Act as an expert microstock photography curator. Provide metadata in English:
                                1. Title: Descriptive title (max 200 chars).
                                2. Category: Select one (Animals, Buildings, Business, Drinks, Environment, Food, Graphic Resources, Hobbies, Industry, Landscapes, Lifestyle, People, Plants, Culture, Science, Social Issues, Sports, Technology, Transport, Travel).
                                3. Keywords: 30-50 relevant keywords, comma-separated.
                                
                                Format:
                                **Title:** [title]
                                **Category:** [category]
                                **Keywords:** [k1, k2, k3...]
                                """
                                
                                response = model.generate_content([prompt, img])
                                result_text = response.text
                                
                                # Menampilkan Hasil
                                st.markdown(result_text)
                                
                                # Tombol copy khusus keyword untuk gambar ini
                                if "**Keywords:**" in result_text:
                                    kw_only = result_text.split("**Keywords:**")[-1].strip()
                                    st.code(kw_only, language="text")
                        
                        st.markdown("---") # Garis pembatas antar gambar
                        
                        # Beri jeda sedikit agar tidak terkena limit API (Rate Limit)
                        time.sleep(1)

                st.success("✅ Semua gambar selesai diproses!")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
else:
    st.write("Silakan pilih gambar untuk memulai.")
