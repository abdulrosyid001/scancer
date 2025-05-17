import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Scancer", page_icon="🩺", layout="wide")

# Judul utama
st.title("Selamat Datang di Scancer")
st.markdown("---")

# Deskripsi singkat website
st.header("Tentang Website Ini")
st.markdown("""
<div style='text-align: justify;'>
    Website ini dirancang untuk membantu mendeteksi potensi kanker kulit melalui analisis gambar kulit menggunakan teknologi kecerdasan buatan. 
    Dengan mengunggah gambar lesi kulit, sistem akan memberikan prediksi terkait jenis kanker kulit berdasarkan model pembelajaran mesin yang telah dilatih. 
    Harap diperhatikan bahwa prediksi ini bukan pengganti diagnosis medis profesional, melainkan alat bantu untuk meningkatkan kesadaran dan deteksi dini.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Penjelasan jenis-jenis kanker kulit
st.header("Jenis-Jenis Kanker Kulit")
st.markdown("""
Berikut adalah penjelasan singkat mengenai jenis-jenis kanker kulit yang dapat dideteksi oleh sistem ini:
""")

# Membuat dua kolom untuk tampilan yang rapi
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Actinic Keratoses dan Intraepithelial Carcinoma (AKIEC)")
    st.image("Gambar kanker/AKIEC/ISIC_0024539.jpg", caption="Contoh Actinic Keratoses", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Actinic keratoses adalah lesi kulit bersisik atau berkerak yang disebabkan oleh paparan sinar matahari jangka panjang. 
        Jika tidak diobati, dapat berkembang menjadi intraepithelial carcinoma, yaitu kanker kulit non-invasif yang terbatas pada lapisan kulit atas.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("2. Basal Cell Carcinoma (BCC)")
    st.image("Gambar kanker/BCC/ISIC_0024457.jpg", caption="Contoh Basal Cell Carcinoma", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Kanker sel basal adalah jenis kanker kulit yang paling umum, biasanya muncul sebagai benjolan mengkilap atau luka yang tidak sembuh. 
        BCC tumbuh lambat dan jarang menyebar, tetapi dapat menyebabkan kerusakan lokal jika tidak diobati.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("3. Benign Keratosis-like Lesions (BKL)")
    st.image("Gambar kanker/BKL/ISIC_0024381.jpg", caption="Contoh Benign Keratosis-like Lesions", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Lesi ini adalah pertumbuhan kulit jinak yang menyerupai keratosis seboroik, sering kali berupa bercak cokelat atau hitam yang tampak seperti kutil. 
        Meskipun tidak berbahaya, BKL dapat menyerupai kanker kulit sehingga memerlukan pemeriksaan.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("4. Dermatofibroma (DF)")
    st.image("Gambar kanker/DF/ISIC_0024973.jpg", caption="Contoh Dermatofibroma", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Dermatofibroma adalah nodul kulit jinak yang biasanya keras, berwarna cokelat atau kemerahan, dan sering muncul di kaki. 
        Lesi ini tidak berbahaya tetapi dapat menyebabkan ketidaknyamanan jika teriritasi.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("5. Melanoma (MEL)")
    st.image("Gambar kanker/MEL/ISIC_0024545.jpg", caption="Contoh Melanoma", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Melanoma adalah jenis kanker kulit yang paling berbahaya karena dapat menyebar ke bagian tubuh lain. 
        Biasanya muncul sebagai tahi lalat asimetris dengan warna tidak seragam, batas tidak teratur, atau perubahan ukuran.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("6. Melanocytic Nevi (NV)")
    st.image("Gambar kanker/NV/ISIC_0024319.jpg", caption="Contoh Melanocytic Nevi", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Melanocytic nevi, atau tahi lalat, adalah pertumbuhan kulit jinak yang disebabkan oleh sel melanosit. 
        Meskipun sebagian besar tidak berbahaya, perubahan pada tahi lalat perlu dipantau karena dapat menyerupai melanoma.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("7. Vascular Lesions (VASC)")
    st.image("images/vascular_lesions.jpg", caption="Contoh Vascular Lesions", use_container_width=True)
    st.markdown("""
    <div style='text-align: justify;'>
        Lesi vaskular adalah pertumbuhan kulit yang berhubungan dengan pembuluh darah, seperti hemangioma atau angioma. 
        Lesi ini biasanya jinak tetapi dapat menyerupai lesi kulit lain sehingga memerlukan evaluasi.
    </div>
    """, unsafe_allow_html=True)

# Catatan penting
st.markdown("---")
st.write("""
**Catatan:** Jika Anda menemukan lesi kulit yang mencurigakan, segera konsultasikan dengan dokter kulit atau tenaga medis profesional untuk pemeriksaan lebih lanjut. 
Deteksi dini adalah kunci untuk pengobatan yang efektif.
""")

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p>© 2025 Scancer.</p>
</div>
""", unsafe_allow_html=True)
