import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# =====================================================
# PAGE
# =====================================================

st.set_page_config(
    page_title="SafeClass",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

/* Semua tulisan */
.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stMarkdown div,
label {
    color: #172b4d !important;
}

/* Heading */
h1, h2, h3, h4 {
    color: #172b4d !important;
}

/* Header */
.safe-header {
    background: #172b4d;
    padding: 28px 32px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.safe-header h1 {
    color: white !important;
    font-size: 32px;
    margin: 0;
}

.safe-header p {
    color: #cbd8e8 !important;
    margin-top: 5px;
}

/* Card */
.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

/* Statistic */
.stat-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #172b4d !important;
}

.stat-label {
    font-size: 12px;
    color: #718096 !important;
}

/* Status */
.status-normal {
    background: #e7f7ed;
    color: #21874b !important;
    padding: 8px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 12px;
}

.status-warning {
    background: #fff4d9;
    color: #b77900 !important;
    padding: 8px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 12px;
}

.status-danger {
    background: #ffe7e7;
    color: #c53030 !important;
    padding: 8px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 12px;
}

/* Person row */
.person {
    background: #f8fafc;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
}

/* Small text */
.small {
    color: #718096 !important;
    font-size: 12px;
}

/* Alert */
.alert-safe {
    background: #e7f7ed;
    border-left: 5px solid #25a55f;
    padding: 15px;
    border-radius: 10px;
}

.alert-warning {
    background: #fff4d9;
    border-left: 5px solid #e0a000;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# CAMERA PROCESSOR
# =====================================================

class CameraProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        # mirror camera
        img = cv2.flip(img, 1)

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="safe-header">

    <h1>🛡️ SafeClass</h1>

    <p>
        Smart Classroom Safety Monitoring System
    </p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# STATISTIC
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">01</div>
        <div class="stat-label">Camera</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">40</div>
        <div class="stat-label">Class Capacity</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">🟢</div>
        <div class="stat-label">System Active</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">0</div>
        <div class="stat-label">Active Alerts</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# =====================================================
# MAIN
# =====================================================

left, right = st.columns([2, 1])


# =====================================================
# CAMERA
# =====================================================

with left:

    st.markdown("""
    <div class="card">

        <h3>📷 Live Classroom Camera</h3>

        <div class="small">
            Camera 01 • Laptop Webcam
        </div>

    </div>
    """, unsafe_allow_html=True)

    webrtc_streamer(
        key="safeclass-camera",

        video_processor_factory=CameraProcessor,

        media_stream_constraints={
            "video": True,
            "audio": False
        },

        async_processing=True
    )


# =====================================================
# MONITORING
# =====================================================

with right:

    st.markdown("""
    <div class="card">

        <h3>📊 Monitoring Status</h3>

        <div class="status-normal">
            ● SYSTEM ACTIVE
        </div>

        <br><br>

        <b>Camera</b>

        <div class="small">
            Laptop Webcam
        </div>

        <br>

        <b>Detection Mode</b>

        <div class="small">
            AI Monitoring
        </div>

        <br>

        <b>People Detected</b>

        <div style="
            font-size:28px;
            font-weight:700;
            color:#172b4d;
        ">
            3
        </div>

    </div>
    """, unsafe_allow_html=True)


    # ALERT

    st.markdown("""
    <div class="card">

        <h3>🚨 Alert System</h3>

        <div class="alert-safe">

            🟢 <b>No abnormal activity detected</b>

            <br>

            <span class="small">
                All detected persons are in normal condition.
            </span>

        </div>

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# PEOPLE MONITORING
# =====================================================

st.markdown("---")

st.markdown("""
<h2>👥 People Monitoring</h2>

<p class="small">
Real-time activity monitoring of people detected by camera.
</p>
""", unsafe_allow_html=True)


# PERSON 01
p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    st.markdown("""
    <div class="person">
        👤 <b>Person #01</b>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="person">
        🪑 Sitting
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="person">
        <span class="status-normal">NORMAL</span>
    </div>
    """, unsafe_allow_html=True)


# PERSON 02
p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    st.markdown("""
    <div class="person">
        👤 <b>Person #02</b>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="person">
        🚶 Walking
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="person">
        <span class="status-normal">NORMAL</span>
    </div>
    """, unsafe_allow_html=True)


# PERSON 03
p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    st.markdown("""
    <div class="person">
        👤 <b>Person #03</b>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="person">
        😴 Inactive
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="person">
        <span class="status-warning">MONITOR</span>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# DETECTION
# =====================================================

st.markdown("---")

st.markdown("""
<h2>🧠 Activity Detection</h2>
""", unsafe_allow_html=True)


d1, d2, d3, d4 = st.columns(4)


with d1:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:30px;">🧍</div>
        <b>Standing</b>
        <br>
        <span class="small">Normal</span>
    </div>
    """, unsafe_allow_html=True)


with d2:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:30px;">🪑</div>
        <b>Sitting</b>
        <br>
        <span class="small">Normal</span>
    </div>
    """, unsafe_allow_html=True)


with d3:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:30px;">😴</div>
        <b>Inactive</b>
        <br>
        <span class="small">Monitor duration</span>
    </div>
    """, unsafe_allow_html=True)


with d4:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:30px;">🚨</div>
        <b>Fall / Collapse</b>
        <br>
        <span class="small">Emergency alert</span>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# FLOW
# =====================================================

st.markdown("---")

st.markdown("""
<h2>⚙️ System Flow</h2>

<div class="card">

    <div style="
        text-align:center;
        font-size:16px;
        font-weight:600;
    ">

        📷 Camera
        &nbsp; → &nbsp;
        👤 Person Detection
        &nbsp; → &nbsp;
        🦴 Pose Estimation
        &nbsp; → &nbsp;
        ⚠️ Activity Analysis
        &nbsp; → &nbsp;
        🚨 Alert

    </div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "SafeClass • Biomedical Engineering Project"
)
