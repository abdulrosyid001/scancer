import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.ensemble import IsolationForest
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load models
model = xgb.Booster()
model.load_model("model_xgboost_81.json")

isolation_forest = joblib.load("model_isolation_forest.pkl")
base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224, 224, 3))

# Helper functions
def extract_image_features(img, model):
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

def detect_anomalies(isolation_forest, data):
    predictions = isolation_forest.predict(data)
    anomalies = predictions == -1
    scores = isolation_forest.score_samples(data)
    return scores, anomalies

# Mappings
gender_mapping = {"Perempuan": 0, "Laki-laki": 1, "Tidak Diketahui": 2}
location_translation = {
    "Punggung": "back", "Ekstrimitas Bawah": "lower extremity", "Torso": "trunk",
    "Ekstrimitas Atas": "upper extremity", "Perut": "abdomen", "Wajah": "face",
    "Dada": "chest", "Kaki": "foot", "Tidak Diketahui": "unknown", "Leher": "neck",
    "Kulit Kepala": "scalp", "Tangan": "hand", "Telinga": "ear", "Alat Kelamin": "genital",
    "Ujung Jari Kaki dan Tangan": "acral"
}
location_mapping = {
    "abdomen": 0, "acral": 1, "back": 2, "chest": 3, "ear": 4, "face": 5,
    "foot": 6, "genital": 7, "hand": 8, "lower extremity": 9, "neck": 10,
    "scalp": 11, "trunk": 12, "unknown": 13, "upper extremity": 14
}
class_mapping = {0: "akiec", 1: "bcc", 2: "bkl", 3: "df", 4: "mel", 5: "nv", 6: "vasc"}
full_name_mapping = {
    "akiec": "Keratosis Aktinik", "bcc": "Karsinoma Sel Basal", "bkl": "Lesi Keratosis Jinak",
    "df": "Dermatofibroma", "mel": "Melanoma", "nv": "Nevi Melanositik", "vasc": "Lesi Vaskular"
}
advice_mapping = {
    "mel": "*Saran:* Melanoma bersifat agresif. Segera konsultasikan ke dokter.",
    "nv": "*Saran:* Lesi jinak, namun perlu dipantau.",
    "akiec": "*Saran:* Dapat menjadi ganas jika tidak ditangani.",
    "bcc": "*Saran:* Tidak menyebar tapi bisa merusak jaringan lokal.",
    "bkl": "*Saran:* Umumnya jinak, tetap perlu evaluasi dokter.",
    "df": "*Saran:* Umumnya jinak, periksa jika berubah.",
    "vasc": "*Saran:* Lesi jinak. Bisa diatasi dengan prosedur ringan."
}

# --- UI ---
st.title("Aplikasi Deteksi Kanker Kulit")

with st.form(key="patient_form"):
    st.subheader("Informasi Pasien")
    gender = st.selectbox("Jenis Kelamin", list(gender_mapping.keys()))
    age = st.number_input("Usia", 0, 100, 25)
    location = st.selectbox("Lokasi Kanker Kulit", list(location_translation.keys()))

    st.subheader("Input Gambar")
    image_input_method = st.radio("Pilih Metode Input", ["Unggah Gambar", "Ambil Foto"])
    
    selected_image = None
    if image_input_method == "Unggah Gambar":
        uploaded_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            selected_image = Image.open(uploaded_file)
            st.image(selected_image, caption="Gambar Terpilih", use_column_width=True)
    else:
        activate_camera = st.checkbox("Aktifkan Kamera")
        if activate_camera:
            camera_file = st.camera_input("Ambil Foto")
            if camera_file:
                selected_image = Image.open(camera_file)
                st.image(selected_image, caption="Foto Kamera", use_column_width=True)

    submitted = st.form_submit_button("Kirim")

# --- Prediction ---
if submitted:
    if selected_image is None:
        st.warning("Silakan unggah atau ambil gambar terlebih dahulu.")
    else:
        try:
            encoded_gender = gender_mapping[gender]
            loc_en = location_translation[location]
            encoded_location = location_mapping[loc_en]
            image_features = extract_image_features(selected_image, base_model)
            combined = np.concatenate([image_features, [age, encoded_gender, encoded_location]])
            df_input = pd.DataFrame([combined], columns=[str(i) for i in range(len(combined))])
            
            # Anomaly detection
            scores, is_anomaly = detect_anomalies(isolation_forest, df_input)
            if is_anomaly[0]:
                st.error("Gambar terdeteksi sebagai tidak valid atau tidak sesuai.")
            else:
                dmatrix = xgb.DMatrix(df_input)
                prediction = model.predict(dmatrix)[0]
                result_code = class_mapping[int(prediction)]
                st.subheader("Hasil Prediksi")
                st.write(f"Jenis Kanker Kulit: **{full_name_mapping[result_code]}**")
                st.markdown(advice_mapping[result_code])
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")
