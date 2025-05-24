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
        max-width: 600px; /* Membatasi lebar konten untuk tampilan lebih rapi */
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
    }
    .centered-caption {
        text-align: center;
        margin-top: 5px;
        font-style: italic;
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
