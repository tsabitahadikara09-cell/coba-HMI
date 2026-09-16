import streamlit as st
import cv2
import numpy as np
import pydicom
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & LAYOUT
# ---------------------------------------------------------
st.set_page_config(
    page_title="MediScan AI Assist - Medical Workstation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2227; padding: 15px; border-radius: 8px; }
    .status-box { padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; }
    .status-info { background-color: #142533; color: #4dabf7; border: 1px solid #4dabf7; }
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
    """Proses Enhancement & Filtering"""
    processed = img.copy()

    # 1. CLAHE
    if clip_limit > 0:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid, tile_grid))
        processed = clahe.apply(processed)

    # 2. Filtering
    if filter_type == "Median Filter":
        k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        processed = cv2.medianBlur(processed, k)
    elif filter_type == "Gaussian Filter":
        k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        processed = cv2.GaussianBlur(processed, (k, k), 0)

    return processed

def plot_histogram(orig, proc):
    """Histogram Intensitas Piksel"""
    fig, ax = plt.subplots(figsize=(8, 2.2), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')
    
    ax.hist(orig.ravel(), bins=256, range=[0, 256], color='gray', alpha=0.5, label='Original')
    ax.hist(proc.ravel(), bins=256, range=[0, 256], color='#00d2ff', alpha=0.6, label='Enhanced')
    
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1e2227', edgecolor='none', labelcolor='white')
    ax.set_title("Distribusi Intensitas Piksel (Histogram)", color='white', fontsize=10)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 3. SIDEBAR: KONTROL INTERAKTIF
# ---------------------------------------------------------
st.sidebar.title("🩺 MediScan Workstation")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Unggah Citra Medis (PNG, JPG, DICOM)", 
    type=["png", "jpg", "jpeg", "dcm"]
)

# Pemilihan Modul Pemeriksaan (Agar teks diagnosis sesuai dengan gambar yang diunggah)
st.sidebar.markdown("### 📋 Modul Pemeriksaan Medis")
modul_pemeriksaan = st.sidebar.selectbox(
    "Jenis Citra Medis:",
    ["X-Ray Musculoskeletal (Tulang/Tangan)", "X-Ray Thorax (Dada/Paru)", "MRI / CT-Scan Otak", "USG / General Image"]
)

st.sidebar.markdown("### 🎛️ Contrast Enhancement (CLAHE)")
clip_limit = st.sidebar.slider("CLAHE Clip Limit", 0.0, 5.0, 2.0, step=0.5)
tile_grid = st.sidebar.slider("CLAHE Tile Grid Size", 2, 16, 8, step=2)

st.sidebar.markdown("### 🧹 Filtering (Noise Reduction)")
filter_type = st.sidebar.selectbox("Pilih Jenis Filter", ["None", "Median Filter", "Gaussian Filter"])
kernel_size = st.sidebar.slider("Ukuran Kernel Filter", 3, 11, 3, step=2)

st.sidebar.markdown("### 📐 Segmentasi & Mode Deteksi ROI")
mode_segmentasi = st.sidebar.selectbox(
    "Metode Penandaan Citra:",
    ["Canny Edge Detection (Deteksi Kontur Tulang/Organ)", "Thresholding ROI (Area Terang/Kepadatan Tinggi)", "Heatmap Intensity Overlay"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Mode Interaksi: **Human-in-the-Loop Assist**")

# ---------------------------------------------------------
# 4. AREA UTAMA (MAIN WORKSPACE)
# ---------------------------------------------------------
st.title("🏥 Medical Image Diagnostic Dashboard")
st.caption(f"Aplikasi Analisis Interaktif Citra Medis - **Modul: {modul_pemeriksaan}**")

if uploaded_file is not None:
    # Membaca & Memproses Gambar
    original_img = load_medical_image(uploaded_file)
    processed_img = apply_image_enhancement(original_img, clip_limit, tile_grid, filter_type, kernel_size)

    # --- TAMPILAN PERBANDINGAN HASIL FILTER ---
    st.markdown("### 🔍 Perbandingan Hasil Pengolahan Citra")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("1. Citra Asli")
        st.image(original_img, use_container_width=True, channels="GRAY", caption="Input Original")

    with col2:
        st.subheader("2. Hasil Enhancement")
        st.image(processed_img, use_container_width=True, channels="GRAY", caption=f"CLAHE={clip_limit}, Filter={filter_type}")

    with col3:
        st.subheader("3. Peta Perubahan (Diff)")
        diff_img = cv2.absdiff(original_img, processed_img)
        diff_color = cv2.applyColorMap(diff_img, cv2.COLORMAP_HOT)
        st.image(cv2.cvtColor(diff_color, cv2.COLOR_BGR2RGB), use_container_width=True, caption="Area piksel terpengaruh filter")

    # Histogram
    st.pyplot(plot_histogram(original_img, processed_img))

    st.markdown("---")

    # --- PANEL SEGMENTASI & ANALISIS SESUAI GAMBAR ---
    st.subheader("📊 Hasil Segmentasi & Feature Extraction")
    col_det1, col_det2 = st.columns([2, 1])

    # PROSES SEGMENTASI BERDASARKAN PILIHAN USER
    overlay_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)
    
    if mode_segmentasi == "Canny Edge Detection (Deteksi Kontur Tulang/Organ)":
        edges = cv2.Canny(processed_img, 50, 150)
        overlay_img[edges > 0] = [0, 255, 0] # Garis hijau untuk batas kontur
        deskripsi_seg = "Garis hijau menunjukkan batas tepi (edges) struktur anatomi / tulang."
        
    elif mode_segmentasi == "Thresholding ROI (Area Terang/Kepadatan Tinggi)":
        _, thresh = cv2.threshold(processed_img, 180, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 100:
                cv2.drawContours(overlay_img, [cnt], -1, (0, 0, 255), 2)
        deskripsi_seg = "Garis merah menandai area struktur dengan densitas/kepadatan tinggi."
        
    else: # Heatmap
        color_mask = cv2.applyColorMap(processed_img, cv2.COLORMAP_JET)
        overlay_img = cv2.addWeighted(overlay_img, 0.6, color_mask, 0.4, 0)
        deskripsi_seg = "Warna merah/kuning menunjukkan area dengan intensitas sinyal terkuat."

    with col_det1:
        st.markdown(f"**Visualisasi Segmentasi ({mode_segmentasi})**")
        st.image(cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB), caption=deskripsi_seg, use_container_width=True)

    with col_det2:
        st.markdown("**Status Analisis Sistem**")
        
        st.markdown("""
            <div class="status-box status-info">
                ℹ️ Citra Berhasil Diolah
            </div>
        """, unsafe_allow_html=True)
        
        # Informasi Dinamis Sesuai Modul
        st.markdown("**Detail Citra Teridentifikasi:**")
        st.write(f"- **Modul Aktif:** {modul_pemeriksaan}")
        st.write(f"- **Nama File:** {uploaded_file.name}")
        st.write(f"- **Resolusi Citra:** {original_img.shape[1]} x {original_img.shape[0]} px")
        st.write(f"- **Rata-rata Intensitas Piksel:** {round(np.mean(processed_img), 2)}")
        
        st.markdown("---")
        
        # Fitur HMI: Validasi Dokter
        st.markdown("**📋 Catatan & Lembar Kerja Radiolog**")
        status_medis = st.selectbox(
            "Hasil Observasi Klinis:",
            ["Struktur Anatomi Normal / Tidak Ada Kelainan", "Terdeteksi Fraktur / Dislokasi Tulang", "Terdeteksi Lesi / Kepadatan Abnormal", "Perlu Pemeriksaan Lanjutan"]
        )
        
        catatan = st.text_area("Catatan Diagnostik:", placeholder="Tuliskan catatan observasi citra di sini...")
        
        if st.button("💾 Simpan Laporan Observasi"):
            st.success(f"Laporan berhasil disimpan! Status Observasi: {status_medis}")

else:
    st.info("👈 Silakan unggah citra medis (.png, .jpg, atau .dcm) pada panel kontrol di sebelah kiri untuk memulai pemrosesan.")
    st.markdown("""
    ### Alur Kerja Interaksi Pengguna (HMI):
    1. **Upload Input:** Masukkan file citra radiologi (X-Ray Tulang / Paru / MRI / USG).
    2. **Pilih Modul & Segmentasi:** Sesuaikan jenis pemeriksaan dan mode deteksi di sidebar.
    3. **Enhancement Control:** Atur *CLAHE* & *Noise Filter* sesuai kenyamanan visual radiolog.
    4. **Clinical Decision:** Dokter/Radiolog mencatat hasil observasi klinis dan menyimpan laporan.
    """)
