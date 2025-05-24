import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Scancer", page_icon="🩺", layout="wide")

# Initialize session state to track the selected cancer type
if 'selected_cancer' not in st.session_state:
    st.session_state.selected_cancer = None

# Custom CSS untuk styling
st.markdown("""
    <style>
    .navbar {
        background-color: #FF4B4B;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        font-family: Arial, sans-serif;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        margin: 0 15px;
        font-size: 16px;
    }
    .navbar div {
        display: flex;
        align-items: center;
    }
    .custom-selectbox {
        background-color: white;
        color: #FF4B4B;
        border: 1px solid #FF4B4B;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 16px;
    }
    .main-title {
        color: #FF4B4B;
        font-size: 48px;
        font-weight: bold;
        margin-top: 20px;
    }
    .sub-title {
        color: #00A6A6;
        font-size: 24px;
        font-weight: bold;
    }
    .description {
        font-size: 14px;
        color: #333;
        text-align: justify;
    }
    .check-button {
        background-color: #00A6A6;
        color: white;
        border: none;
        padding: 10px 30px;
        border-radius: 25px;
        font-size: 16px;
        cursor: pointer;
    }
    /* Style for Streamlit selectbox */
    div[data-testid="stSelectbox"] > div {
        background-color: white;
        color: #FF4B4B;
        border: 1px solid #FF4B4B;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 16px;
    }
    div[data-testid="stSelectbox"] > div > div {
        color: #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
    <div class="navbar">
        <span style="font-size: 24px; font-weight: bold;">SCANCER</span>
        <div>
            <a href="#">Beranda</a>
            <a href="#">Prediksi</a>
            <a href="#">FAQ</a>
""", unsafe_allow_html=True)

# Add Streamlit selectbox for cancer types
cancer_options = ["Jenis-Jenis Kanker Kulit", "AKIEC", "BCC", "BKL", "DF", "Melanoma", "Melanocytic Nevi", "Vascular Lesions"]
cancer_values = ["", "akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]
selected_cancer_label = st.selectbox("", cancer_options, index=0, label_visibility="hidden")
selected_cancer = cancer_values[cancer_options.index(selected_cancer_label)]

st.markdown("</div></div>", unsafe_allow_html=True)

# Update session state when the dropdown changes
if selected_cancer != st.session_state.selected_cancer:
    st.session_state.selected_cancer = selected_cancer

# Main Section
col1, col2 = st.columns([1, 1])

with col1:
    # Placeholder for the image (since Streamlit cannot directly render the illustration)
    st.markdown("""
        <div style="text-align: center;">
            <img src="https://via.placeholder.com/400x400.png?text=Illustration" alt="Illustration" style="width: 100%;">
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-title">AYO CHECK KESEHATAN KULITMU</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">SCANCER Hadir Sebagai Solusi untuk Deteksi Dini Penyakit Kanker Kulit</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="description">
            SCANCER adalah layanan kesehatan online terpercaya di Indonesia yang menghadirkan solusi untuk deteksi dini penyakit kanker kulit. Kami percaya bahwa menjaga kesehatan dengan tidak proaktif untuk memeriksakan diri sebelumm terlambat. Dengan deteksi dini, Anda dapat menghindari komplikasi serius yang dapat memengaruhi kualitas hidup.
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<button class="check-button">CHECK SEKARANG</button>', unsafe_allow_html=True)

# Jenis-Jenis Kanker Kulit Section (Conditionally displayed based on dropdown selection)
if st.session_state.selected_cancer:
    st.markdown("---")
    if st.session_state.selected_cancer == "akiec":
        st.subheader("1. Actinic Keratoses dan Intraepithelial Carcinoma (AKIEC)")
        st.image("Gambar kanker/AKIEC/ISIC_0024539.jpg", caption="Contoh Actinic Keratoses", width=300)
        st.markdown("""
            Actinic keratoses adalah lesi kulit bersisik atau berkerak yang disebabkan oleh paparan sinar matahari jangka panjang. 
            Jika tidak diobati, dapat berkembang menjadi intraepithelial carcinoma, yaitu kanker kulit non-invasif yang terbatas pada lapisan kulit atas.
        """)

    elif st.session_state.selected_cancer == "bcc":
        st.subheader("2. Basal Cell Carcinoma (BCC)")
        st.image("Gambar kanker/BCC/ISIC_0024457.jpg", caption="Contoh Basal Cell Carcinoma", width=300)
        st.markdown("""
            Kanker sel basal adalah jenis kanker kulit yang paling umum, biasanya muncul sebagai benjolan mengkilap atau luka yang tidak sembuh. 
            BCC tumbuh lambat dan jarang menyebar, tetapi dapat menyebabkan kerusakan lokal jika tidak diobati.
        """)

    elif st.session_state.selected_cancer == "bkl":
        st.subheader("3. Benign Keratosis-like Lesions (BKL)")
        st.image("Gambar kanker/BKL/ISIC_0024381.jpg", caption="Contoh Benign Keratosis-like Lesions", width=300)
        st.markdown("""
            Lesi ini adalah pertumbuhan kulit jinak yang menyerupai keratosis seboroik, sering kali berupa bercak cokelat atau hitam yang tampak seperti kutil. 
            Meskipun tidak berbahaya, BKL dapat menyerupai kanker kulit sehingga memerlukan pemeriksaan.
        """)

    elif st.session_state.selected_cancer == "df":
        st.subheader("4. Dermatofibroma (DF)")
        st.image("Gambar kanker/DF/ISIC_0024973.jpg", caption="Contoh Dermatofibroma", width=300)
        st.markdown("""
            Dermatofibroma adalah nodul kulit jinak yang biasanya keras, berwarna cokelat atau kemerahan, dan sering muncul di kaki. 
            Lesi ini tidak berbahaya tetapi dapat menyebabkan ketidaknyamanan jika teriritasi.
        """)

    elif st.session_state.selected_cancer == "mel":
        st.subheader("5. Melanoma (MEL)")
        st.image("Gambar kanker/MEL/ISIC_0024545.jpg", caption="Contoh Melanoma", width=300)
        st.markdown("""
            Melanoma adalah jenis kanker kulit yang paling berbahaya karena dapat menyebar ke bagian tubuh lain. 
            Biasanya muncul sebagai tahi lalat asimetris dengan warna tidak seragam, batas tidak teratur, atau perubahan ukuran.
        """)

    elif st.session_state.selected_cancer == "nv":
        st.subheader("6. Melanocytic Nevi (NV)")
        st.image("Gambar kanker/NV/ISIC_0024319.jpg", caption="Contoh Melanocytic Nevi", width=300)
        st.markdown("""
            Melanocytic nevi, atau tahi lalat, adalah pertumbuhan kulit jinak yang disebabkan oleh sel melanosit. 
            Meskipun sebagian besar tidak berbahaya, perubahan pada tahi lalat perlu dipantau karena dapat menyerupai melanoma.
        """)

    elif st.session_state.selected_cancer == "vasc":
        st.subheader("7. Vascular Lesions (VASC)")
        st.image("Gambar kanker/VASC/ISIC_0024662.jpg", caption="Contoh Vascular Lesions", width=300)
        st.markdown("""
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
    <p>© 2025 Scancer.</p>
</div>
""", unsafe_allow_html=True)
