*import streamlit as st
import cv2
import numpy as np
from PIL import Image
import xgboost as xgb
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import joblib
from sklearn.ensemble import IsolationForest

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Beranda"

# CSS untuk mengatur teks subheader di tengah dan tombol kirim
css = """
<style>
.centered-subheader {
    text-align: center;
}
.full-width-button {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 0 auto;
}
.full-width-button .stButton>button {
    width: 100%;
    max-width: 1200px;
    padding: 10px;
    font-size: 16px;
    background-color: #1a2b3c;
    color: white;
    border: none;
    border-radius: 5px;
    box-sizing: border-box;
}
.stForm {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}
</style>
"""

# Menyisipkan CSS di aplikasi
st.markdown(css, unsafe_allow_html=True)

# Load the XGBoost model from JSON
try:
    model = xgb.Booster()
    model.load_model("model_xgboost_81.json")
except FileNotFoundError:
    st.error("XGBoost model file 'model_xgboost_81.json' not found.")
    model = None
except Exception as e:
    st.error(f"Error loading XGBoost model: {str(e)}")
    model = None

# Load the Isolation Forest model and scaler
try:
    isolation_forest = joblib.load("model_isolation_forest.pkl")
    scaler = joblib.load("scaler.joblib")
except FileNotFoundError:
    st.error("Isolation Forest model or scaler file not found. Please ensure 'model_isolation_forest.pkl' and 'scaler.joblib' are in the correct directory.")
    isolation_forest = None
    scaler = None
except Exception as e:
    st.error(f"Error loading Isolation Forest model or scaler: {str(e)}")
    isolation_forest = None
    scaler = None

# Load MobileNetV2 for feature extraction
try:
    base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224, 224, 3))
except Exception as e:
    st.error(f"Error loading MobileNetV2: {str(e)}")
    base_model = None

# Manual mapping for gender
gender_mapping = {
    "Perempuan": 0,
    "Laki-laki": 1,
    "Tidak Diketahui": 2
}

# Translation from Indonesian to English for location
location_translation = {
    "Punggung": "back",
    "Ekstrimitas Bawah": "lower extremity",
    "Torso": "trunk",
    "Ekstrimitas Atas": "upper extremity",
    "Perut": "abdomen",
    "Wajah": "face",
    "Dada": "chest",
    "Kaki": "foot",
    "Tidak Diketahui": "unknown",
    "Leher": "neck",
    "Kulit Kepala": "scalp",
    "Tangan": "hand",
    "Telinga": "ear",
    "Alat Kelamin": "genital",
    "Ujung Jari Kaki dan Tangan": "acral"
}

# Manual mapping for location
location_mapping = {
    "abdomen": 0,
    "acral": 1,
    "back": 2,
    "chest": 3,
    "ear": 4,
    "face": 5,
    "foot": 6,
    "genital": 7,
    "hand": 8,
    "lower extremity": 9,
    "neck": 10,
    "scalp": 11,
    "trunk": 12,
    "unknown": 13,
    "upper extremity": 14
}

# Mapping for prediction classes (kode)
class_mapping = {
    0: "akiec",
    1: "bcc",
    2: "bkl",
    3: "df",
    4: "mel",
    5: "nv",
    6: "vasc"
}

# Mapping untuk nama lengkap jenis kanker kulit
full_name_mapping = {
    "akiec": "Keratosis Aktinik / Karsinoma Intraepitelial",
    "bcc": "Karsinoma Sel Basal",
    "bkl": "Lesion Mirip Keratosis Jinak",
    "df": "Dermatofibroma",
    "mel": "Melanoma",
    "nv": "Nevi Melanositik",
    "vasc": "Lesion Vaskular"
}

# Saran tindakan untuk pasien berdasarkan jenis kanker kulit
advice_mapping = {
    "akiec": """
    Saran Tindakan:  
    Keratosis Aktinik dapat berkembang menjadi kanker kulit jika tidak ditangani. Segera konsultasikan dengan dokter kulit untuk evaluasi lebih lanjut. Dokter mungkin merekomendasikan krioterapi, terapi topikal (seperti fluorouracil atau imiquimod), atau biopsi untuk memastikan diagnosis. Lindungi kulit Anda dari paparan sinar matahari berlebih dengan menggunakan tabir surya SPF tinggi dan pakaian pelindung.
    """,
    "bcc": """
    Saran Tindakan:  
    Karsinoma Sel Basal adalah jenis kanker kulit yang umum, biasanya tidak menyebar tetapi dapat merusak jaringan di sekitarnya. Segera temui dokter kulit untuk pemeriksaan lebih lanjut. Pengobatan dapat meliputi eksisi bedah, terapi radiasi, atau krioterapi, tergantung pada ukuran dan lokasi. Pastikan untuk memantau perubahan pada kulit Anda dan gunakan tabir surya setiap hari.
    """,
    "bkl": """
    Saran Tindakan:  
    Lesion Mirip Keratosis Jinak biasanya tidak berbahaya, tetapi penting untuk memastikan diagnosis yang tepat. Konsultasikan dengan dokter kulit untuk memastikan lesion ini jinak. Jika ada perubahan warna, ukuran, atau bentuk, segera periksakan. Gunakan tabir surya untuk mencegah kerusakan kulit lebih lanjut.
    """,
    "df": """
    Saran Tindakan:  
    Dermatofibroma umumnya jinak dan tidak memerlukan pengobatan kecuali menyebabkan ketidaknyamanan atau perubahan yang mencurigakan. Namun, untuk memastikan diagnosis, konsultasikan dengan dokter kulit. Jika diperlukan, dokter mungkin merekomendasikan eksisi kecil. Pantau lesion untuk setiap perubahan yang tidak biasa.
    """,
    "mel": """
    Saran Tindakan:  
    Melanoma adalah jenis kanker kulit yang serius dan dapat menyebar ke bagian tubuh lain jika tidak diobati. Segera temui dokter kulit atau onkologis untuk evaluasi lebih lanjut. Dokter mungkin akan merekomendasikan biopsi, eksisi bedah, atau pemeriksaan lebih lanjut untuk menentukan stadium kanker. Jangan tunda pengobatan, dan hindari paparan sinar matahari langsung.
    """,
    "nv": """
    Saran Tindakan:  
    Nevi Melanositik biasanya jinak, tetapi beberapa dapat berkembang menjadi melanoma. Konsultasikan dengan dokter kulit untuk memastikan tidak ada tanda-tanda keganasan (perubahan warna, bentuk, atau ukuran). Pantau tahi lalat Anda secara rutin menggunakan metode ABCDE (Asymmetry, Border, Color, Diameter, Evolving) dan gunakan tabir surya untuk perlindungan.
    """,
    "vasc": """
    Saran Tindakan:  
    Lesion Vaskular biasanya jinak, tetapi penting untuk memastikan diagnosis. Konsultasikan dengan dokter kulit untuk mengevaluasi lesion ini. Jika tidak menyebabkan masalah, mungkin tidak memerlukan pengobatan. Namun, jika ada perubahan atau ketidaknyamanan, dokter mungkin merekomendasikan laser atau prosedur kecil lainnya.
    """
}

# Function to extract features from an image
def extract_image_features(img, model):
    try:
        img = img.resize((224, 224))
        img_array = np.array(img)
        if len(img_array.shape) == 2:
            img_array = np.stack([img_array] * 3, axis=-1)
        elif img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        features = model.predict(img_array, verbose=0)
        return features.flatten()
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

# Function to detect anomalies using Isolation Forest
def detect_anomalies(isolation_forest, data, scaler):
    data_scaled = scaler.transform(data)
    predictions = isolation_forest.predict(data_scaled)
    anomalies = predictions == -1
    scores = isolation_forest.score_samples(data_scaled)
    return scores, anomalies

# Page rendering based on session state
if st.session_state.page == "Beranda":
    st.header("Selamat Datang di Aplikasi Prediksi Kanker Kulit")
    st.write("""
    Aplikasi ini membantu memprediksi jenis kanker kulit berdasarkan gambar dan informasi pasien.
    Silakan klik tombol di bawah untuk memulai prediksi.
    """)
    st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
    if st.button("Ke Halaman Prediksi"):
        st.session_state.page = "Prediction"
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Prediction":
    st.header("Informasi Pasien dan Input Gambar")
    with st.form(key="patient_form"):
        st.markdown('<h3 class="centered-subheader">Identitas Pasien</h3>', unsafe_allow_html=True)
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan", "Tidak Diketahui"])
        age = st.number_input("Usia (dalam tahun)", min_value=0, max_value=100, step=1)
        location = st.selectbox(
            "Lokasi Kanker Kulit",
            ["Punggung", "Ekstrimitas Bawah", "Torso", "Ekstrimitas Atas", "Perut", "Wajah",
             "Dada", "Kaki", "Tidak Diketahui", "Leher", "Kulit Kepala", "Tangan", "Telinga",
             "Alat Kelamin", "Ujung Jari Kaki dan Tangan"]
        )
        st.info("""
        Berikut adalah penjelasan singkat untuk setiap lokasi kanker kulit:
        - Punggung: Area punggung sering terpapar sinar matahari, meningkatkan risiko kanker kulit.
        - Ekstrimitas Bawah: Termasuk kaki dan paha, rentan jika sering terpapar matahari tanpa perlindungan.
        - Torso: Bagian tengah tubuh, termasuk perut dan sisi, bisa terkena kanker akibat paparan UV.
        - Ekstrimitas Atas: Termasuk lengan dan bahu, sering terkena sinar matahari langsung.
        - Perut: Area yang kurang terpapar tapi bisa terkena jika tidak dilindungi.
        - Wajah: Salah satu area paling rentan karena sering terpapar sinar matahari.
        - Dada: Rentan terutama pada pria karena paparan sinar matahari tanpa perlindungan.
        - Kaki: Termasuk telapak kaki, bisa terkena jika sering berjalan tanpa alas kaki di luar.
        - Tidak Diketahui: Pilih jika lokasi tidak dapat ditentukan dengan pasti.
        - Leher: Area yang sering terpapar sinar matahari, meningkatkan risiko kanker.
        - Kulit Kepala: Rentan terutama pada orang botak karena paparan langsung sinar matahari.
        - Tangan: Termasuk jari, sering terkena paparan lingkungan dan sinar matahari.
        - Telinga: Area kecil tapi sangat rentan terhadap kanker kulit akibat sinar UV.
        - Alat Kelamin: Jarang, tetapi perlu diperiksa jika ada perubahan kulit.
        - Ujung Jari Kaki dan Tangan: Area akral, bisa terkena jika ada trauma atau paparan kimia.
        """)

        st.markdown('<h3 class="centered-subheader">Input Gambar</h3>', unsafe_allow_html=True)
        image_input_method = st.radio("Pilih Metode Input Gambar:", ["Unggah Gambar", "Ambil Foto"])
        selected_image = None
        if image_input_method == "Unggah Gambar":
            uploaded_file = st.file_uploader("Pilih Gambar...", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                selected_image = Image.open(uploaded_file)
                st.image(selected_image, caption="Gambar yang Diunggah", use_column_width=True)
        else:
            picture = st.camera_input("Ambil Foto")
            if picture is not None:
                selected_image = Image.open(picture)
                st.image(selected_image, caption="Foto yang Diambil", use_column_width=True)

        st.markdown('<h3 class="centered-subheader">Kirim Data</h3>', unsafe_allow_html=True)
        st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="Kirim")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        st.success("Data berhasil dikirim")
        st.write(f"Jenis Kelamin: {gender}")
        st.write(f"Usia: {age}")
        st.write(f"Lokasi Kanker Kulit: {location}")

        if selected_image is None:
            st.warning("Tolong unggah gambar dengan salah satu dari kedua metode tersebut.")
            st.stop()

        if model is None or base_model is None or isolation_forest is None or scaler is None:
            st.error("Cannot proceed with prediction due to missing model(s) or scaler.")
            st.stop()

        with st.spinner("Processing image and predicting..."):
            image_features = extract_image_features(selected_image, base_model)
            if image_features is None:
                st.stop()

            encoded_gender = gender_mapping[gender]
            location_english = location_translation[location]
            encoded_location = location_mapping[location_english]

            feature_names = [f"{i}" for i in range(image_features.shape[0])] + ["age", "sex", "localization"]
            combined_features = np.concatenate([image_features, [age, encoded_gender, encoded_location]])
            input_data = pd.DataFrame([combined_features], columns=feature_names)

            scores, anomalies = detect_anomalies(isolation_forest, input_data, scaler)

            if anomalies[0]:
                st.markdown(f"""
                Peringatan: Gambar mungkin bukan gambar kanker kulit (skor anomali: {scores[0]:.4f}).
                Pastikan gambar yang diunggah adalah gambar kulit yang jelas dan sesuai.
                Jika Anda memiliki kekhawatiran, konsultasikan dengan dokter kulit.
                """)
            else:
                dmatrix = xgb.DMatrix(input_data)
                prediction = model.predict(dmatrix)[0]
                result_code = class_mapping[int(prediction)]
                result_name = full_name_mapping[result_code]
                st.subheader("Hasil Prediksi")
                st.write(f"Prediksi Tipe Kanker Kulit: {result_name}")
                st.markdown(advice_mapping[result_code])

        st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
        if st.button("Kembali ke Beranda"):
            st.session_state.page = "Beranda"
        st.markdown('</div>', unsafe_allow_html=True)*
