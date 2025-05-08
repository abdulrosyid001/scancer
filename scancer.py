import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import xgboost as xgb
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

# Set page configuration
st.set_page_config(page_title="Skin Cancer Data Input", layout="wide")

# Title
st.title("Skin Cancer Data Collection and Prediction")

# Load the XGBoost model from JSON
try:
    model = xgb.Booster()
    model.load_model("model_xgboost_81%.json")
except FileNotFoundError:
    st.error("XGBoost model file 'model_xgboost_81%.json' not found. Please ensure the file is in the correct directory.")
    model = None
except Exception as e:
    st.error(f"Error loading XGBoost model: {str(e)}")
    model = None

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
    "wajah": "face",
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
    base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
except Exception as e:
    st.error(f"Error loading MobileNetV2: {str(e)}")
    base_model = None

# Function to extract features from an image
def extract_image_features(img, model):
    # Convert PIL Image to numpy array
    img = img.resize((224, 224))  # Resize to 224x224
    img_array = np.array(img)
    
    # Ensure image has 3 channels (RGB)
    if len(img_array.shape) == 2:  # Grayscale
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = img_array[:, :, :3]
    
    # Preprocess image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)
    
    # Extract features
    features = model.predict(img_array, verbose=0)
    return features.flatten()

# Image Input Section
st.header("Input Gambar")
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

# Data Input Section
st.header("Informasi Pasien")
with st.form(key="patient_form"):
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan", "Tidak Diketahui"])
    age = st.number_input("Usia", min_value=0, max_value=100, step=1)
    location = st.selectbox(
        "Lokasi Kanker Kulit",
        ["Punggung", "Ekstrimitas Bawah", "Torso", "Ekstrimitas Atas", "Perut", "wajah", "Dada", "Kaki", "Tidak Diketahui", "Leher", "Kulit Kepala", "Tangan", "Telinga", "Alat Kelamin", "Ujung Jari Kaki dan Tangan"]
    )
    submit_button = st.form_submit_button(label="Kirim")

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

    # Proceed with prediction if model and image are available
    if model is not None and base_model is not None and selected_image is not None:
        try:
            # Encode categorical variables using manual mapping
            encoded_gender = gender_mapping[gender]
            # Translate location to English and encode
            location_english = location_translation[location]
            encoded_location = location_mapping[location_english]
            
            # Extract image features
            image_features = extract_image_features(selected_image, base_model)
            
            # Combine features
            feature_names = [f"{i}" for i in range(image_features.shape[0])] + ["age", "sex", "localization"]
            combined_features = np.concatenate([image_features, [age, encoded_gender, encoded_location]])
            input_data = pd.DataFrame([combined_features], columns=feature_names)
            
            # Convert to DMatrix for XGBoost Booster
            dmatrix = xgb.DMatrix(input_data)
            
            # Make prediction
            prediction = model.predict(dmatrix)[0]
            # For multiclass, prediction is the class index
            result = class_mapping[int(prediction)]  # Map class index to class name
            st.subheader("Hasil Prediksi")
            st.write(f"Prediksi Tipe Kanker Kulit: **{result}**")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    elif model is None or base_model is None:
        st.error("Cannot make prediction due to missing model(s).")