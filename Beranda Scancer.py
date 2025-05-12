import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Scancer", page_icon="🩺", layout="wide")

# Judul utama
st.title("Selamat Datang di Scancer")
st.markdown("---")

# Deskripsi singkat website
st.header("Tentang Website Ini")
st.write("""
Website ini dirancang untuk membantu mendeteksi potensi kanker kulit melalui analisis gambar kulit menggunakan teknologi kecerdasan buatan. 
Dengan mengunggah gambar lesi kulit, sistem akan memberikan prediksi terkait jenis kanker kulit berdasarkan model pembelajaran mesin yang telah dilatih. 
Harap diperhatikan bahwa prediksi ini bukan pengganti diagnosis medis profesional, melainkan alat bantu untuk meningkatkan kesadaran dan deteksi dini.
""")

# Penjelasan jenis-jenis kanker kulit
st.header("Jenis-Jenis Kanker Kulit")
st.markdown("""
Berikut adalah penjelasan singkat mengenai jenis-jenis kanker kulit yang dapat dideteksi oleh sistem ini:
""")

# Membuat dua kolom untuk tampilan yang rapi
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Actinic Keratoses dan Intraepithelial Carcinoma (AKIEC)")
    st.write("""
    Actinic keratoses adalah lesi kulit bersisik atau berkerak yang disebabkan oleh paparan sinar matahari jangka panjang. 
    Jika tidak diobati, dapat berkembang menjadi intraepithelial carcinoma, yaitu kanker kulit non-invasif yang terbatas pada lapisan kulit atas.
    """)

    st.subheader("2. Basal Cell Carcinoma (BCC)")
    st.write("""
    Kanker sel basal adalah jenis kanker kulit yang paling umum, biasanya muncul sebagai benjolan mengkilap atau luka yang tidak sembuh. 
    BCC tumbuh lambat dan jarang menyebar, tetapi dapat menyebabkan kerusakan lokal jika tidak diobati.
    """)

    st.subheader("3. Benign Keratosis-like Lesions (BKL)")
    st.write("""
    Lesi ini adalah pertumbuhan kulit jinak yang menyerupai keratosis seboroik, sering kali berupa bercak cokelat atau hitam yang tampak seperti kutil. 
    Meskipun tidak berbahaya, BKL dapat menyerupai kanker kulit sehingga memerlukan pemeriksaan.
    """)

    st.subheader("4. Dermatofibroma (DF)")
    st.write("""
    Dermatofibroma adalah nodul kulit jinak yang biasanya keras, berwarna cokelat atau kemerahan, dan sering muncul di kaki. 
    Lesi ini tidak berbahaya tetapi dapat menyebabkan ketidaknyamanan jika teriritasi.
    """)

with col2:
    st.subheader("5. Melanoma (MEL)")
    st.write("""
    Melanoma adalah jenis kanker kulit yang paling berbahaya karena dapat menyebar ke bagian tubuh lain. 
    Biasanya muncul sebagai tahi lalat asimetris dengan warna tidak seragam, batas tidak teratur, atau perubahan ukuran.
    """)

    st.subheader("6. Melanocytic Nevi (NV)")
    st.write("""
    Melanocytic nevi, atau tahi lalat, adalah pertumbuhan kulit jinak yang disebabkan oleh sel melanosit. 
    Meskipun sebagian besar tidak berbahaya, perubahan pada tahi lalat perlu dipantau karena dapat menyerupai melanoma.
    """)

    st.subheader("7. Vascular Lesions (VASC)")
    st.write("""
    Lesi vaskular adalah pertumbuhan kulit yang berhubungan dengan pembuluh darah, seperti hemangioma atau angioma. 
    Lesi ini biasanya jinak tetapi dapat menyerupai lesi kulit lain sehingga memerlukan evaluasi.
    """)

# Catatan penting
st.markdown("---")
st.write("""
**Catatan:** Jika Anda menemukan lesi kulit yang mencurigakan, segera konsultasikan dengan dokter kulit atau tenaga medis profesional untuk pemeriksaan lebih lanjut. 
Deteksi dini adalah kunci untuk pengobatan yang efektif.
""")

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p>© 2025 Website Prediksi Kanker Kulit. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
