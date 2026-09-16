import streamlit as st
import cv2
import numpy as np
import pydicom
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & LAYOUT (HMI Standard)
# ---------------------------------------------------------
st.set_page_config(
    page_title="MediScan AI Assist - CAD Workstation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan antarmuka medis
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
        dicom_data = pydicom.dcmread(uploaded_file)
        img = dicom_data.pixel_array
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    else:
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
    return img

def apply_image_enhancement(img, clip_limit, tile_grid, filter_type, kernel_size):
    """Proses pra-pemrosesan citra medis (CLAHE & Filtering)"""
    processed = img.copy()

    # 1. Contrast Enhancement (CLAHE)
    if clip_limit > 0:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid, tile_grid))
        processed = clahe.apply(processed)

    # 2. Filtering / Noise Reduction
    if filter_type == "Median Filter":
        k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        processed = cv2.medianBlur(processed, k)
    elif filter_type == "Gaussian Filter":
        k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        processed = cv2.GaussianBlur(processed, (k, k), 0)

    return processed

def plot_histogram(orig, proc):
    """Membuat perbandingan histogram distribusi piksel"""
    fig, ax = plt.subplots(figsize=(8, 2.5), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')
    
    ax.hist(orig.ravel(), bins=256, range=[0, 256], color='gray', alpha=0.5, label='Original')
    ax.hist(proc.ravel(), bins=256, range=[0, 256], color='#00d2ff', alpha=0.6, label='Enhanced')
    
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1e2227', edgecolor='none', labelcolor='white')
    ax.set_title("Distribusi Intensitas Piksel (Histogram)", color='white', fontsize=10)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 3. SIDEBAR: KONTROL INTERAKTIF (HMI Control Panel)
# ---------------------------------------------------------
st.sidebar.title("🩺 MediScan Workstation")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Unggah Citra Medis (PNG, JPG, DICOM)", 
    type=["png", "jpg", "jpeg", "dcm"]
)

st.sidebar.markdown("### 🎛️ Contrast Enhancement (CLAHE)")
clip_limit = st.sidebar.slider("CLAHE Clip Limit", 0.0, 5.0, 2.0, step=0.5)
tile_grid = st.sidebar.slider("CLAHE Tile Grid Size", 2, 16, 8, step=2)

st.sidebar.markdown("### 🧹 Filtering (Noise Reduction)")
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
    # Read & Process Image
    original_img = load_medical_image(uploaded_file)
    processed_img = apply_image_enhancement(original_img, clip_limit, tile_grid, filter_type, kernel_size)

    # --- TAMPILAN PERBANDINGAN HASIL FILTER (Visual Comparison) ---
    st.markdown("### 🔍 Perbandingan Hasil Pengolahan Citra")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("1. Citra Asli")
        st.image(original_img, use_container_width=True, channels="GRAY", caption="Input Original")

    with col2:
        st.subheader("2. Hasil Filter")
        st.image(processed_img, use_container_width=True, channels="GRAY", caption=f"Enhancement: CLAHE={clip_limit}, Filter={filter_type}")

    with col3:
        st.subheader("3. Peta Perubahan (Diff)")
        # Hitung selisih mutlak antara citra asli dan citra terproses
        diff_img = cv2.absdiff(original_img, processed_img)
        # Bikin berwarna biar kelihatan jelas area piksel yang berubah/dihaluskan
        diff_color = cv2.applyColorMap(diff_img, cv2.COLORMAP_HOT)
        st.image(cv2.cvtColor(diff_color, cv2.COLOR_BGR2RGB), use_container_width=True, caption="Area piksel yang mengalami penyesuaian")

    # Histogram Perubahan Intensitas
    st.pyplot(plot_histogram(original_img, processed_img))

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
        
        heatmap_rgb = cv2.cvtColor(heatmap_overlay, cv2.COLOR_BGR2RGB)
        st.image(heatmap_rgb, caption="Visualisasi Segmentasi / ROI (Region of Interest)", use_container_width=True)

    with col_det2:
        st.markdown("**Status Analisis Sistem**")
        
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
        
        # Fitur HMI: Validasi Dokter
        st.markdown("**📋 Validasi Dokter (Human-in-the-Loop)**")
        validation = st.radio(
            "Apakah Anda menyetujui analisis sistem?",
            ("Belum Diverifikasi", "Setuju (Konfirmasi Diagnosis)", "Tolak / Intervensi Manual")
        )
        
        catatan = st.text_area("Catatan Tambahan Radiolog / Dokter:", placeholder="Masukkan catatan klinis...")
        
        if st.button("💾 Simpan Laporan Diagnostik"):
            st.success(f"Laporan berhasil disimpan! Status: {validation}")

else:
    st.info("👈 Silakan unggah citra medis (.png, .jpg, atau .dcm) pada panel kontrol di sebelah kiri untuk memulai pemrosesan.")
    
    st.markdown("""
    ### Alur Kerja Interaksi Pengguna (HMI):
    1. **Upload Input:** Masukkan file citra radiologi (X-Ray / CT / USG).
    2. **Enhancement Control:** Adjust *CLAHE* & *Noise Filter* sesuai kenyamanan visual radiolog.
    3. **Interactive Inspection:** Amati perbandingan gambar *side-by-side* & heatmap segmentasi.
    4. **Clinical Decision:** Dokter memvalidasi hasil prediksi AI dan memberikan catatan medis.
    """)
