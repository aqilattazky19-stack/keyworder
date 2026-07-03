import streamlit as st
import google.generativeai as genai
from PIL import Image

# Konfigurasi Halaman UI
st.set_page_config(page_title="Stock Keyworder AI", layout="centered")

st.title("📸 AI Keyworder untuk Adobe Stock")
st.write("Aplikasi ini secara otomatis menghasilkan Judul, Kategori, dan Keyword (dipisahkan koma) untuk foto microstock Anda.")

# Input API Key
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")
    st.markdown("[Dapatkan API Key gratis di sini](https://aistudio.google.com/app/apikey)")
    st.info("Kunci API tidak disimpan dan hanya digunakan selama sesi aplikasi ini berjalan.")

# Area Upload Gambar
uploaded_file = st.file_uploader("Pilih gambar atau ilustrasi Anda...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Menampilkan gambar
    image = Image.open(uploaded_file)
    st.image(image, caption="Preview Gambar", use_column_width=True)

    if st.button("Generate Metadata", type="primary"):
        if not api_key:
            st.error("⚠️ Silakan masukkan API Key di menu samping (sidebar) terlebih dahulu.")
        else:
            try:
                # Konfigurasi AI
                genai.configure(api_key=api_key)
                # Menggunakan model flash yang cepat dan mendukung gambar
                model = genai.GenerativeModel('gemini-1.5-flash')

                # Instruksi khusus untuk format Adobe Stock
                prompt = """
                Act as an expert microstock photography contributor for Adobe Stock.
                Analyze this image and provide the following metadata in English (since English is the global standard for stock search):

                1. Title: A highly accurate and descriptive title for the image (maximum 200 characters).
                2. Category: Select exactly ONE of the most relevant Adobe Stock categories from this list: Animals, Buildings and Architecture, Business, Drinks, Environment, Food, Graphic Resources, Hobbies and Leisure, Industry, Landscapes, Lifestyle, People, Plants and Flowers, Culture and Religion, Science, Social Issues, Sports, Technology, Transport, Travel.
                3. Keywords: Provide between 30 to 50 highly relevant keywords. Order them from most important to least important. Separate them strictly with commas. Do NOT use hashtags (#). Do not use bullet points.

                Format the exact output like this:
                **Title:** [Your Title]
                
                **Category:** [Your Category]
                
                **Keywords:** [keyword1, keyword2, keyword3, ...]
                """

                with st.spinner("AI sedang menganalisis gambar Anda..."):
                    response = model.generate_content([prompt, image])

                st.success("Metadata berhasil dibuat!")
                
                # Menampilkan Hasil Utama
                st.markdown("### Hasil Analisis")
                st.markdown(response.text)

                # Ekstraksi khusus untuk Keyword agar mudah di-copy
                st.markdown("---")
                st.markdown("### 📋 Copy Keywords")
                st.write("Gunakan kotak di bawah ini untuk menyalin (*copy*) langsung ke kolom keyword Adobe Stock (klik ikon copy di sudut kanan atas kotak).")
                
                # Memisahkan bagian teks untuk mendapatkan hanya keyword
                if "**Keywords:**" in response.text:
                    keywords_only = response.text.split("**Keywords:**")[-1].strip()
                    st.code(keywords_only, language="text")
                else:
                    st.warning("Gagal mengekstrak blok keywords secara spesifik. Silakan copy dari teks di atas.")

            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi server: {e}")