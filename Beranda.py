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
    .independent-section {
        margin-top: 20px;
        text-align: center;
    }
    .centered-content {
        text-align: center;
        margin: 10px auto;
        max-width: 800px; /* Membatasi lebar konten untuk tampilan lebih rapi */
        width: 100%; /* Memastikan div menggunakan lebar penuh dalam batasan max-width */
    }
    .centered-content h3 {
        margin: 0 auto; /* Memastikan h3 benar-benar terpusat */
        display: block;
        text-align: center;
    }
    .centered-image {
        display: block;
        margin: 0 auto;
        max-width: 300px; /* Membatasi lebar gambar agar tidak terlalu besar */
        width: 100%; /* Memastikan gambar responsif dalam batasan max-width */
    }
    /* Tambahan untuk memastikan gambar Streamlit terpusat di kolom */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    div[data-testid="stImage"] img {
        display: block;
        margin: 0 auto;
    }
    .centered-caption {
        text-align: center;
        margin-top: 5px;
        font-style: italic;
    }
    .description-text {
        font-size: 14px;
        color: #333;
        text-align: justify;
        margin-top: 10px;
    }
    /* Gaya khusus untuk gambar di Main Section (di bawah SCANCER) */
    div[data-testid="stImage"].main-section-image img {
        max-width: 400px; /* Mengatur ukuran maksimum gambar lebih kecil */
        width: 100%; /* Responsif */
        display: block;
        margin: 0 auto; /* Memastikan gambar tetap terpusat */
    }
    </style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
    <div class="navbar">
        <span style="font-size: 24px; font-weight: bold;">SCANCER</span>
    </div>
""", unsafe_allow_html=True)

# Main Section
col1, col2 = st.columns([1, 1])

with col1:
    # Menggunakan st.image untuk memuat gambar lokal dengan ukuran lebih kecil
    try:
        st.image("Gambar kanker/animasi_scancer.jpg", use_container_width=False, output_format="auto")
    except FileNotFoundError:
        st.error("Gambar 'animasi_scancer.jpg' tidak ditemukan. Pastikan file berada di direktori 'Gambar kanker' relatif terhadap file Python Anda.")

with col2:
    st.markdown('<div class="main-title">AYO CEK KESEHATAN KULITMU</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">SCANCER Hadir Sebagai Solusi untuk Deteksi Dini Penyakit Kanker Kulit</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="description">
            SCANCER adalah layanan kesehatan online terpercaya di Indonesia yang menghadirkan solusi untuk deteksi dini penyakit kanker kulit. Kami percaya bahwa menjaga kesehatan dengan tidak proaktif untuk memeriksakan diri sebelumm terlambat. Dengan deteksi dini, Anda dapat menghindari komplikasi serius yang dapat memengaruhi kualitas hidup.
        </div>
        <div class="description">
        
            Website ini dapat mendeteksi beberapa jenis kanker kulit, yaitu Actinic Keratoses dan Intraepithelial Carcinoma, Basal Cell Carcinoma, Benign Keratosis-like Lesions, Dermatofibroma, Melanoma, Melanocytic Nevi, dan Vascular Lesions.
        </div>
    """, unsafe_allow_html=True)

# Independent Section for Dropdown, Cancer Descriptions, and Button
st.markdown('<div class="independent-section">', unsafe_allow_html=True)

# Add Streamlit selectbox for cancer types
cancer_options = ["Jenis-Jenis Kanker Kulit", "Actinic Keratoses dan Intraepithelial Carcinoma", "Basal Cell Carcinoma", "Benign Keratosis-like Lesions", "Dermatofibroma", "Melanoma", "Melanocytic Nevi", "Vascular Lesions"]
cancer_values = ["", "akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]
selected_cancer_label = st.selectbox("", cancer_options, index=0, label_visibility="hidden")
selected_cancer = cancer_values[cancer_options.index(selected_cancer_label)]

# Update session state when the dropdown changes
if selected_cancer != st.session_state.selected_cancer:
    st.session_state.selected_cancer = selected_cancer

# Jenis-Jenis Kanker Kulit Section (Conditionally displayed based on dropdown selection)
if st.session_state.selected_cancer:
    st.markdown('<div class="centered-content">', unsafe_allow_html=True)
    
    # Actinic Keratoses dan Intraepithelial Carcinoma (AKIEC)
    if st.session_state.selected_cancer == "akiec":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/AKIEC/ISIC_0024539.jpg", caption="Contoh Actinic Keratoses", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024539.jpg' tidak ditemukan di direktori 'Gambar kanker/AKIEC'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Actinic keratoses adalah lesi kulit bersisik atau berkerak yang disebabkan oleh paparan sinar matahari jangka panjang. 
                    Jika tidak diobati, dapat berkembang menjadi intraepithelial carcinoma, yaitu kanker kulit non-invasif yang terbatas pada lapisan kulit atas.
                </div>
            """, unsafe_allow_html=True)

    # Basal Cell Carcinoma (BCC)
    elif st.session_state.selected_cancer == "bcc":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/BCC/ISIC_0024457.jpg", caption="Contoh Basal Cell Carcinoma", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024457.jpg' tidak ditemukan di direktori 'Gambar kanker/BCC'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Kanker sel basal adalah jenis kanker kulit yang paling umum, biasanya muncul sebagai benjolan mengkilap atau luka yang tidak sembuh. 
                    BCC tumbuh lambat dan jarang menyebar, tetapi dapat menyebabkan kerusakan lokal jika tidak diobati.
                </div>
            """, unsafe_allow_html=True)

    # Benign Keratosis-like Lesions (BKL)
    elif st.session_state.selected_cancer == "bkl":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/BKL/ISIC_0024381.jpg", caption="Contoh Benign Keratosis-like Lesions", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024381.jpg' tidak ditemukan di direktori 'Gambar kanker/BKL'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Lesi ini adalah pertumbuhan kulit jinak yang menyerupai keratosis seboroik, sering kali berupa bercak cokelat atau hitam yang tampak seperti kutil. 
                    Meskipun tidak berbahaya, BKL dapat menyerupai kanker kulit sehingga memerlukan pemeriksaan.
                </div>
            """, unsafe_allow_html=True)

    # Dermatofibroma (DF)
    elif st.session_state.selected_cancer == "df":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/DF/ISIC_0024973.jpg", caption="Contoh Dermatofibroma", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024973.jpg' tidak ditemukan di direktori 'Gambar kanker/DF'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Dermatofibroma adalah nodul kulit jinak yang biasanya keras, berwarna cokelat atau kemerahan, dan sering muncul di kaki. 
                    Lesi ini tidak berbahaya tetapi dapat menyebabkan ketidaknyamanan jika teriritasi.
                </div>
            """, unsafe_allow_html=True)

    # Melanoma (MEL)
    elif st.session_state.selected_cancer == "mel":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/MEL/ISIC_0024545.jpg", caption="Contoh Melanoma", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024545.jpg' tidak ditemukan di direktori 'Gambar kanker/MEL'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Melanoma adalah jenis kanker kulit yang paling berbahaya karena dapat menyebar ke bagian tubuh lain. 
                    Biasanya muncul sebagai tahi lalat asimetris dengan warna tidak seragam, batas tidak teratur, atau perubahan ukuran.
                </div>
            """, unsafe_allow_html=True)

    # Melanocytic Nevi (NV)
    elif st.session_state.selected_cancer == "nv":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/NV/ISIC_0024319.jpg", caption="Contoh Melanocytic Nevi", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024319.jpg' tidak ditemukan di direktori 'Gambar kanker/NV'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Melanocytic nevi, atau tahi lalat, adalah pertumbuhan kulit jinak yang disebabkan oleh sel melanosit. 
                    Meskipun sebagian besar tidak berbahaya, perubahan pada tahi lalat perlu dipantau karena dapat menyerupai melanoma.
                </div>
            """, unsafe_allow_html=True)

    # Vascular Lesions (VASC)
    elif st.session_state.selected_cancer == "vasc":
        col_img, col_desc = st.columns([1, 1])
        with col_img:
            try:
                st.image("Gambar kanker/VASC/ISIC_0024662.jpg", caption="Contoh Vascular Lesions", use_container_width=False, output_format="auto")
            except FileNotFoundError:
                st.error("Gambar 'ISIC_0024662.jpg' tidak ditemukan di direktori 'Gambar kanker/VASC'.")
        with col_desc:
            st.markdown("""
                <div class="description-text">
                    Lesi vaskular adalah pertumbuhan kulit yang berhubungan dengan pembuluh darah, seperti hemangioma atau angioma. 
                    Lesi ini biasanya jinak tetapi dapat menyerupai lesi kulit lain sehingga memerlukan evaluasi.
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Place the "CHECK SEKARANG" button centered
st.markdown('<div class="centered-content"><button class="check-button">CEK SEKARANG</button></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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
