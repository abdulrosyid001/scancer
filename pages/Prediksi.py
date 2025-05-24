# Perbaikan untuk bagian input gambar dalam form
with st.form(key="patient_form"):
    # ... bagian lain tetap sama ...
    
    # Bagian Input Gambar dengan error handling yang lebih baik
    st.markdown('<h3 class="centered-subheader">Input Gambar</h3>', unsafe_allow_html=True)
    
    # Informasi untuk pengguna
    st.info("""
    **Panduan Input Gambar:**
    - Untuk kamera: Pastikan browser memberikan izin akses kamera
    - Untuk upload: Gunakan gambar format JPG, JPEG, atau PNG
    - Pastikan gambar jelas dan fokus pada area kulit yang ingin diperiksa
    """)
    
    image_input_method = st.radio("Pilih Metode Input Gambar:", ["Unggah Gambar", "Ambil Foto"])

    selected_image = None
    
    if image_input_method == "Unggah Gambar":
        uploaded_file = st.file_uploader("Pilih Gambar...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                selected_image = Image.open(uploaded_file)
                st.image(selected_image, caption="Gambar yang Diunggah", use_column_width=True)
                st.success("✅ Gambar berhasil diunggah!")
            except Exception as e:
                st.error(f"Error membuka gambar: {str(e)}")
                
    else:  # Capture from Camera
        st.write("**Petunjuk Penggunaan Kamera:**")
        st.write("1. Klik tombol 'Take Photo' di bawah")
        st.write("2. Izinkan akses kamera jika diminta browser")
        st.write("3. Arahkan kamera ke area kulit yang ingin diperiksa")
        st.write("4. Klik tombol untuk mengambil foto")
        
        try:
            # Tambahkan parameter untuk debugging
            picture = st.camera_input(
                "Ambil Foto",
                help="Pastikan pencahayaan cukup dan gambar fokus pada area kulit"
            )
            
            if picture is not None:
                try:
                    selected_image = Image.open(picture)
                    st.image(selected_image, caption="Foto yang Diambil", use_column_width=True)
                    st.success("✅ Foto berhasil diambil!")
                except Exception as e:
                    st.error(f"Error memproses foto: {str(e)}")
            else:
                st.info("📷 Klik tombol 'Take Photo' untuk mengambil gambar")
                
        except Exception as e:
            st.error(f"Error mengakses kamera: {str(e)}")
            st.error("""
            **Troubleshooting Kamera:**
            - Pastikan browser memberikan izin akses kamera
            - Coba refresh halaman dan izinkan akses kamera
            - Pastikan tidak ada aplikasi lain yang menggunakan kamera
            - Coba gunakan browser Chrome atau Firefox
            - Untuk testing lokal, gunakan 'localhost' bukan IP address
            """)

    # ... sisa kode tetap sama ...

# Tambahan: Perbaikan untuk form submission handling
if submit_button:
    st.success("Data berhasil dikirim")
    st.write(f"Jenis Kelamin: {gender}")
    st.write(f"Usia: {age}")
    st.write(f"Lokasi Kanker Kulit: {location}")
    
    # Check for image input dengan pesan yang lebih jelas
    if selected_image is None:
        st.warning("⚠️ Mohon unggah gambar atau ambil foto terlebih dahulu sebelum melakukan prediksi.")
        st.info("Pastikan untuk memilih salah satu metode input gambar dan mengunggah/mengambil foto dengan benar.")
    else:
        st.success("✅ Gambar berhasil diproses, melanjutkan ke tahap prediksi...")
        
        # Proceed with prediction if all models and image are available
        if model is not None and base_model is not None and isolation_forest is not None:
            try:
                # ... kode prediksi tetap sama ...
                pass
            except Exception as e:
                st.error(f"Error dalam prediksi: {str(e)}")
                st.info("Silakan coba lagi atau hubungi administrator jika masalah berlanjut.")
        else:
            st.error("❌ Model tidak tersedia. Tidak dapat melakukan prediksi.")

# Tambahan: Debug information (opsional, untuk development)
if st.checkbox("Tampilkan Info Debug (untuk Developer)"):
    st.write("Browser User Agent:", st.runtime.get_instance().browser_info if hasattr(st.runtime.get_instance(), 'browser_info') else "N/A")
    st.write("Streamlit Version:", st.__version__)
    st.write("Models Status:")
    st.write(f"- XGBoost Model: {'✅ Loaded' if model is not None else '❌ Not Loaded'}")
    st.write(f"- MobileNetV2 Model: {'✅ Loaded' if base_model is not None else '❌ Not Loaded'}")
    st.write(f"- Isolation Forest: {'✅ Loaded' if isolation_forest is not None else '❌ Not Loaded'}")
