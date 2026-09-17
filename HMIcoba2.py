import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SafeClass",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #172b4d;
}

.header {
    background: #172b4d;
    padding: 25px 30px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.header h1 {
    color: white;
    margin: 0;
}

.header p {
    color: #c8d8ed;
    margin: 5px 0 0 0;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5eaf2;
    margin-bottom: 15px;
}

.stat {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5eaf2;
    text-align: center;
}

.stat-number {
    font-size: 28px;
    font-weight: bold;
    color: #172b4d;
}

.stat-label {
    font-size: 13px;
    color: #7a879a;
}

.normal {
    background: #e8f7ef;
    padding: 10px;
    border-radius: 10px;
}

.warning {
    background: #fff4dc;
    padding: 10px;
    border-radius: 10px;
}

.danger {
    background: #ffe8e8;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# VIDEO PROCESSOR
# =========================================================

class CameraProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        # Mirror camera
        img = cv2.flip(img, 1)

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header">

<h1>🛡️ SafeClass</h1>

<p>
Smart Classroom Safety Monitoring System
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# TOP STATISTICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">01</div>
        <div class="stat-label">Camera</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">40</div>
        <div class="stat-label">Class Capacity</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">🟢</div>
        <div class="stat-label">System Status</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">0</div>
        <div class="stat-label">Active Alerts</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# =========================================================
# MAIN CONTENT
# =========================================================

left, right = st.columns([2, 1])


# =========================================================
# CAMERA
# =========================================================

with left:

    st.subheader("📷 Live Classroom Camera")

    st.caption("Camera 01 • Laptop Webcam")

    webrtc_streamer(
        key="safeclass-camera",

        video_processor_factory=CameraProcessor,

        media_stream_constraints={
            "video": True,
            "audio": False
        },

        async_processing=True
    )


# =========================================================
# MONITORING STATUS
# =========================================================

with right:

    st.subheader("📊 Monitoring Status")

    st.success("🟢 SYSTEM ACTIVE")

    st.write("**Camera**")
    st.caption("Laptop Webcam")

    st.write("**Detection Mode**")
    st.caption("Camera Preview")

    st.write("**AI Detection**")
    st.caption("Coming Soon")


    st.subheader("🚨 Alert System")

    st.info(
        "🟢 No abnormal activity detected."
    )


# =========================================================
# PEOPLE MONITORING
# =========================================================

st.divider()

st.subheader("👥 People Monitoring")

st.caption(
    "Data berikut masih berupa dummy. "
    "Nantinya akan diisi oleh AI detection."
)


col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("**PERSON ID**")

with col2:
    st.write("**ACTIVITY**")

with col3:
    st.write("**STATUS**")


# Person 1
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("👤 Person #01")

with col2:
    st.write("🪑 Sitting")

with col3:
    st.success("Normal")


# Person 2
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("👤 Person #02")

with col2:
    st.write("🚶 Walking")

with col3:
    st.success("Normal")


# Person 3
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("👤 Person #03")

with col2:
    st.write("😴 Inactive")

with col3:
    st.warning("Monitor")


# =========================================================
# AI DETECTION
# =========================================================

st.divider()

st.subheader("🧠 Planned AI Detection")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.info("""
    🧍

    **Standing**

    Normal posture
    """)


with col2:
    st.info("""
    🪑

    **Sitting**

    Normal posture
    """)


with col3:
    st.warning("""
    😴

    **Inactive**

    Monitor duration
    """)


with col4:
    st.error("""
    🚨

    **Fall / Collapse**

    Emergency alert
    """)


# =========================================================
# SYSTEM FLOW
# =========================================================

st.divider()

st.subheader("⚙️ System Flow")

st.write(
    "📷 Camera  →  "
    "👤 Person Detection  →  "
    "🦴 Pose Estimation  →  "
    "⚠️ Activity Analysis  →  "
    "🚨 Alert"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SafeClass • Biomedical Engineering Project"
)
