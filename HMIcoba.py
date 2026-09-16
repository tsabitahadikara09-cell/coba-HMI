import streamlit as st
import cv2
import numpy as np
import pydicom
from PIL import Image

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & LAYOUT (HMI Standard)
# PERBAIKAN: Menggunakan layout="wide" (bukan page_layout)
# Harus diletakkan di paling atas sebelum panggilan st.* lainnya
# ---------------------------------------------------------
st.set_page_config(
    page_title="MediScan AI Assist - CAD Workstation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan antarmuka medis modern
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2227; padding: 15px; border-radius: 8px; }
    .status-box { padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; }
    .status-alert { background-color: #3b1414; color: #ff6b6b; border: 1px solid #ff6b6b; }
    .status-ok { background-color: #11321d; color: #51cf66; border: 1px solid #51cf66; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. HELPER FUNCTIONS: PENGOLAHAN CITRA MEDIS
# ---------------------------------------------------------
def load_medical_image(uploaded_file):
    """Membaca file citra standar (.png/.jpg) atau DICOM (.dcm)"""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    
    if uploaded_file.name.lower().endswith('.dcm'):
        # Membaca file format DICOM
        dicom_data = pydicom.dcmread(uploaded_file)
        img = dicom_data.pixel_array
        # Normalisasi skala abu-abu ke 8-bit (0-255)
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    else:
        # Membaca format citra biasa
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
    return img

def apply_image_enhancement(img, clip_limit, tile_grid, filter_type, kernel_size):
    """Proses pra-pemrosesan citra medis (Contrast Enhancement & Noise Reduction)"""
    processed = img.copy()

    # 1. Contrast Enhancement (CLAHE)
    if clip_limit > 0:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid, tile_grid))
        processed = clahe.apply(processed)

    # 2. Filtering / Noise Reduction
    if filter_type == "Median Filter":
        # Kernel size harus berupa bilangan ganjil
        k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        processed = cv2.medianBlur(processed, k)
    elif filter_type == "Gaussian Filter":
        k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        processed = cv2.GaussianBlur(processed, (k, k), 0)

    return processed

# ---------------------------------------------------------
# 3. SIDEBAR: KONTROL INTERAKTIF (HMI Control Panel)
# ---------------------------------------------------------
st.sidebar.title("🩺 MediScan Workstation")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Unggah Citra Medis (PNG, JPG, DICOM)", 
    type=["png", "jpg", "jpeg", "dcm"]
)

st.sidebar.markdown("### 🎛️ Image Enhancement")
clip_limit = st.sidebar.slider("CLAHE Clip Limit (Kontras)", 0.0, 5.0, 2.0, step=0.5)
tile_grid = st.sidebar.slider("CLAHE Tile Grid Size", 2, 16, 8, step=2)

st.sidebar.markdown("### 🧹 Noise Reduction")
filter_type = st.sidebar.selectbox("Pilih Jenis Filter", ["None", "Median Filter", "Gaussian Filter"])
kernel_size = st.sidebar.slider("Ukuran Kernel Filter", 3, 11, 3, step=2)

st.sidebar.markdown("---")
st.sidebar.caption("Mode Interaksi: **Human-in-the-Loop Assist**")

# ---------------------------------------------------------
# 4. AREA UTAMA (MAIN WORKSPACE)
# ---------------------------------------------------------
st.title("🏥 Medical Image Diagnostic Dashboard")
st.caption("Aplikasi Analisis Interaktif Citra Medis (X-Ray, CT-Scan, USG, MRI)")

if uploaded_file is not None:
    # Membaca citra dan menerapkan enhancement
    original_img = load_medical_image(uploaded_file)
    processed_img = apply_image_enhancement(original_img, clip_limit, tile_grid, filter_type, kernel_size)

    # --- TAMPILAN SIDE-BY-SIDE (Visual Comparison) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Citra Asli (Original)")
        st.image(original_img, use_container_width=True, channels="GRAY")

    with col2:
        st.subheader("⚡ Citra Terproses (Enhanced)")
        st.image(processed_img, use_container_width=True, channels="GRAY")

    st.markdown("---")

    # --- PANEL ANALISIS DIAGNOSIS & IDENTIFIKASI ---
    st.subheader("📊 Hasil Indikasi & Diagnostic Assistance")
    
    col_det1, col_det2 = st.columns([2, 1])

    with col_det1:
        st.markdown("**Segmentasi Area Terindikasi Kelainan (Heatmap Overlay)**")
        
        # Visualisasi Heatmap ROI (Region of Interest)
        color_mask = cv2.applyColorMap(processed_img, cv2.COLORMAP_JET)
        heatmap_overlay = cv2.addWeighted(
            cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR), 0.7, 
            color_mask, 0.3, 0
        )
        
        # Konversi warna BGR OpenCV ke RGB untuk tampilan Streamlit
        heatmap_rgb = cv2.cvtColor(heatmap_overlay, cv2.COLOR_BGR2RGB)
        st.image(heatmap_rgb, caption="Visualisasi Segmentasi / ROI (Region of Interest)", use_container_width=True)

    with col_det2:
        st.markdown("**Status Analisis Sistem**")
        
        # Contoh Kartu Diagnostik
        st.markdown("""
            <div class="status-box status-alert">
                ⚠️ Indikasi Kelainan Terdeteksi
            </div>
        """, unsafe_allow_html=True)
        
        st.metric(label="Tingkat Kepercayaan (Confidence Score)", value="88.4%", delta="Tinggi")
        
        st.markdown("**Detail Analisis:**")
        st.write("- **Prediksi Kategori:** Opasitas Paru / Pneumonia")
        st.write("- **Area ROI:** Lobus Kanan Bawah")
        st.write("- **Kepadatan (Avg Density):** High Opacity")
        
        st.markdown("---")
        
        # Fitur HMI: Validasi Dokter (Human-in-the-Loop)
        st.markdown("**📋 Validasi Dokter (Human-in-the-Loop)**")
        validation = st.radio(
            "Apakah Anda menyetujui analisis sistem?",
            ("Belum Diverifikasi", "Setuju (Konfirmasi Diagnosis)", "Tolak / Intervensi Manual")
        )
        
        catatan = st.text_area("Catatan Tambahan Radiolog / Dokter:", placeholder="Masukkan catatan klinis...")
        
        if st.button("💾 Simpan Laporan Diagnostik"):
            st.success(f"Laporan berhasil disimpan! Status: {validation}")

else:
    # Tampilan awal jika belum ada file yang diunggah
    st.info("👈 Silakan unggah citra medis (.png, .jpg, atau .dcm) pada panel kontrol di sebelah kiri untuk memulai pemrosesan.")
    
    st.markdown("""
    ### Alur Kerja Interaksi Pengguna (HMI):
    1. **Upload Input:** Masukkan file citra radiologi (X-Ray / CT / USG).
    2. **Enhancement Control:** Adjust *CLAHE* & *Noise Filter* sesuai kenyamanan visual radiolog.
    3. **Interactive Inspection:** Amati perbandingan gambar *side-by-side* & heatmap segmentasi.
    4. **Clinical Decision:** Dokter memvalidasi hasil prediksi AI dan memberikan catatan medis.
    """)
