import streamlit as st
import cv2
import numpy as np
from PIL import Image
import xgboost as xgb
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.ensemble import IsolationForest  # Impor Isolation Forest

# CSS untuk mengatur teks subheader di tengah dan tombol kirim
css = """
<style>
.centered-subheader {
    text-align: center;
}
.full-width-button {
    width: 100%;  /* Mengisi lebar penuh halaman */
    display: flex;
    justify-content: center;  /* Menjaga tombol terpusat */
    margin: 0 auto;  /* Memastikan posisi terpusat */
}
.full-width-button .stButton>button {
    width: 100%;  /* Tombol mengisi lebar elemen induk */
    max-width: 1200px;  /* Lebar maksimum lebih besar untuk mengisi kotak besar */
    padding: 10px;
    font-size: 16px;
    background-color: #1a2b3c;  /* Warna latar gelap seperti gambar */
    color: white;  /* Warna teks putih */
    border: none;
    border-radius: 5px;
    box-sizing: border-box;  /* Memastikan padding tidak menambah lebar */
}
/* Mengatur lebar formulir agar lebih lebar dan terpusat */
.stForm {
    width: 100%;
    max-width: 1200px;  /* Lebar maksimum lebih besar untuk formulir */
    margin: 0 auto;  /* Pusatkan formulir */
    padding: 0 20px;
}
</style>
"""

# Set page configuration
st.set_page_config(page_title="Scancer", layout="wide")

# Menyisipkan CSS di aplikasi
st.markdown(css, unsafe_allow_html=True)

# Title
st.title("Scancer: Deteksi Kanker Kulit")

# Load the XGBoost model from JSON
try:
    model = xgb.Booster()
    model.load_model("model_xgboost_81.json")
except FileNotFoundError:
    st.error("XGBoost model file 'model_xgboost_81.json' not found. Please ensure the file is in the correct directory.")
    model = None
except Exception as e:
    st.error(f"Error loading XGBoost model: {str(e)}")
    model = None

# Load the Isolation Forest model and scaler
try:
    isolation_forest = joblib.load("model_isolation_forest.pkl")
except FileNotFoundError:
    st.error("Isolation Forest model or scaler file not found. Please ensure 'model_isolation_forest.pkl' and 'scaler.joblib' are in the correct directory.")
    isolation_forest = None
    scaler = None
except Exception as e:
    st.error(f"Error loading Isolation Forest model or scaler: {str(e)}")
    isolation_forest = None
    scaler = None

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

# Mapping for prediction classes
class_mapping = {
    0: "akiec",
    1: "bcc",
    2: "bkl",
    3: "df",
    4: "mel",
    5: "nv",
    6: "vasc"
}

# Load MobileNetV2 for feature extraction
try:
    base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224, 224, 3))
except Exception as e:
    st.error(f"Error loading MobileNetV2: {str(e)}")
    base_model = None

# Function to extract features from an image
def extract_image_features(img, model):
    img = img.resize((224, 224))  # Resize to 224x224
    img_array = np.array(img)
    
    # Ensure image has 3 channels (RGB)
    if len(img_array.shape) == 2:  # Grayscale
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = img_array[:, :, :3]
    
    # Preprocessing
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)
    
    # Extract features
    features = model.predict(img_array, verbose=0)
    return features.flatten()

# Function to detect anomalies using Isolation Forest
def detect_anomalies(isolation_forest, data):
    # Prediksi anomali: -1 untuk anomali, 1 untuk normal
    predictions = isolation_forest.predict(data_scaled)
    anomalies = predictions == -1
    # Skor anomali: semakin rendah (lebih negatif), semakin anomali
    scores = isolation_forest.score_samples(data_scaled)
    return scores, anomalies

# Data Input Section
st.header("Informasi Pasien dan Input Gambar")

# Satu formulir yang mencakup semua elemen
with st.form(key="patient_form"):
    # Bagian Identitas Pasien
    st.markdown('<h3 class="centered-subheader">Identitas Pasien</h3>', unsafe_allow_html=True)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan", "Tidak Diketahui"])
    age = st.number_input("Usia", min_value=0, max_value=100, step=1)
    location = st.selectbox(
        "Lokasi Kanker Kulit",
        ["Punggung", "Ekstrimitas Bawah", "Torso", "Ekstrimitas Atas", "Perut", "Wajah", 
         "Dada", "Kaki", "Tidak Diketahui", "Leher", "Kulit Kepala", "Tangan", "Telinga", 
         "Alat Kelamin", "Ujung Jari Kaki dan Tangan"]
    )

    # Pemisah visual
    st.markdown("---")

    # Bagian Input Gambar
    st.markdown('<h3 class="centered-subheader">Input Gambar</h3>', unsafe_allow_html=True)
    image_input_method = st.radio("Pilih Metode Input Gambar:", ["Unggah Gambar", "Ambil Foto"])

    selected_image = None
    if image_input_method == "Unggah Gambar":
        uploaded_file = st.file_uploader("Pilih Gambar...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            selected_image = Image.open(uploaded_file)
            st.image(selected_image, caption="Gambar yang Diunggah", use_column_width=True)
    else:  # Capture from Camera
        picture = st.camera_input("Ambil Foto")
        if picture is not None:
            selected_image = Image.open(picture)
            st.image(selected_image, caption="Foto yang Diambil", use_column_width=True)

    # Pemisah visual
    st.markdown("---")

    # Tombol Kirim
    st.markdown('<h3 class="centered-subheader">Kirim Data</h3>', unsafe_allow_html=True)
    st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="Kirim")
    st.markdown('</div>', unsafe_allow_html=True)

# Form submission handling
if submit_button:
    st.success("Data berhasil dikirim")
    st.write(f"Jenis Kelamin: {gender}")
    st.write(f"Usia: {age}")
    st.write(f"Lokasi Kanker Kulit: {location}")
    
    # Check for image input
    if selected_image is not None:
        st.write("Anda berhasil mengirimkan gambar.")
    else:
        st.warning("Tolong unggah gambar dengan salah satu dari kedua metode tersebut.")

    # Proceed with prediction if all models and image are available
    if model is not None and base_model is not None and isolation_forest is not None:
        try:
            # Encode categorical variables using manual mapping
            encoded_gender = gender_mapping[gender]
            location_english = location_translation[location]
            encoded_location = location_mapping[location_english]
            
            # Extract image features
            image_features = extract_image_features(selected_image, base_model)
            
            # Combine features
            feature_names = [f"{i}" for i in range(image_features.shape[0])] + ["age", "sex", "localization"]
            combined_features = np.concatenate([image_features, [age, encoded_gender, encoded_location]])
            input_data = pd.DataFrame([combined_features], columns=feature_names)
            
            # Check for anomaly using Isolation Forest
            scores, anomalies = detect_anomalies(isolation_forest, input_data, scaler)
            
            if anomalies[0]:  # Data is an anomaly
                st.error(f"Gambar yang Anda masukkan bukan gambar kanker kulit (Anomaly Score: {-scores[0]:.4f}).")
            else:  # Data is not an anomaly, proceed to XGBoost
                st.write(f"Anomaly Score: {-scores[0]:.4f} (Data dianggap normal)")
                # Convert to DMatrix for XGBoost Booster
                dmatrix = xgb.DMatrix(input_data)
                
                # Make prediction
                prediction = model.predict(dmatrix)[0]
                result = class_mapping[int(prediction)]  # Map class index to class name
                st.subheader("Hasil Prediksi")
                st.write(f"Prediksi Tipe Kanker Kulit: **{result}**")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Cannot make prediction due to missing model(s) or image.")
