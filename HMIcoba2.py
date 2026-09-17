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
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background-color: #F5F7FB;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 1250px;
    padding-top: 25px;
}


/* ================= HEADER ================= */

.header-box {
    background: linear-gradient(
        135deg,
        #152B4D,
        #244B7A
    );

    padding: 25px 30px;

    border-radius: 20px;

    margin-bottom: 25px;

    color: white;
}

.header-title {
    font-size: 32px;
    font-weight: 700;
}

.header-subtitle {
    color: #C8D8ED;
    font-size: 13px;
}


/* ================= CARDS ================= */

.card {
    background: white;

    border-radius: 18px;

    padding: 22px;

    border: 1px solid #E5EAF2;

    box-shadow:
        0px 4px 15px rgba(30, 50, 80, 0.05);

    margin-bottom: 18px;
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #172B4D;

    margin-bottom: 5px;
}


/* ================= STAT CARD ================= */

.stat-card {
    background: white;

    border-radius: 16px;

    padding: 18px;

    border: 1px solid #E5EAF2;

    text-align: center;

    min-height: 105px;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #172B4D;
}

.stat-label {
    font-size: 12px;
    color: #7A879A;
}


/* ================= STATUS ================= */

.status-green {
    background: #E8F7EF;
    color: #238B50;

    padding: 7px 14px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 600;

    display: inline-block;
}

.status-yellow {
    background: #FFF5DE;
    color: #C98A00;

    padding: 7px 14px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 600;

    display: inline-block;
}

.status-red {
    background: #FFE9E9;
    color: #D13D3D;

    padding: 7px 14px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 600;

    display: inline-block;
}


/* ================= CAMERA ================= */

.camera-title {
    font-size: 20px;
    font-weight: 700;
    color: #172B4D;
}


/* ================= ALERT ================= */

.alert-box {
    background: #FFF0F0;

    border-left: 5px solid #E04444;

    padding: 15px;

    border-radius: 10px;

    color: #9C2929;
}


/* ================= INFO ================= */

.info-text {
    color: #7A879A;
    font-size: 13px;
}


/* ================= TABLE ================= */

.table-header {
    color: #7A879A;
    font-size: 12px;
    font-weight: 600;
}

.person-row {
    background: #FAFBFD;

    padding: 12px;

    border-radius: 10px;

    margin-top: 8px;

    color: #263B5A;

    font-size: 13px;
}


/* ================= BUTTON ================= */

.stButton > button {

    border-radius: 12px;

    height: 45px;

    font-weight: 600;

    border: none;

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
<div class="header-box">

    <div class="header-title">
        🛡️ SafeClass
    </div>

    <div class="header-subtitle">
        Smart Classroom Safety Monitoring System
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# STATISTICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("""
    <div class="stat-card">

        <div class="stat-number">
            01
        </div>

        <div class="stat-label">
            Camera Active
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="stat-card">

        <div class="stat-number">
            40
        </div>

        <div class="stat-label">
            Classroom Capacity
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="stat-card">

        <div class="stat-number">
            🟢
        </div>

        <div class="stat-label">
            System Status
        </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown("""
    <div class="stat-card">

        <div class="stat-number">
            0
        </div>

        <div class="stat-label">
            Active Alerts
        </div>

    </div>
    """, unsafe_allow_html=True)


st.write("")


# =========================================================
# MAIN AREA
# =========================================================

left, right = st.columns([2.1, 1])


# =========================================================
# CAMERA
# =========================================================

with left:

    st.markdown("""
    <div class="card">

        <div class="camera-title">
            📷 Live Classroom Camera
        </div>

        <div class="info-text">
            Camera 01 • Laptop Webcam
        </div>

        <br>

    </div>
    """, unsafe_allow_html=True)

    # Camera component
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

    st.markdown("""
    <div class="card">

        <div class="card-title">
            📊 Monitoring Status
        </div>

        <br>

        <span class="status-green">
            ● SYSTEM ACTIVE
        </span>

        <br><br>

        <b>Camera</b>

        <div class="info-text">
            Laptop Webcam
        </div>

        <br>

        <b>Detection Mode</b>

        <div class="info-text">
            Camera Preview
        </div>

        <br>

        <b>AI Detection</b>

        <div class="info-text">
            Coming Soon
        </div>

    </div>
    """, unsafe_allow_html=True)


    # Alert

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🚨 Alert System
        </div>

        <br>

        <div class="alert-box">

            🟢 No abnormal activity detected.

        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PEOPLE MONITORING
# =========================================================

st.markdown("""
<div class="card">

    <div class="card-title">
        👥 People Monitoring
    </div>

    <div class="info-text">
        Example monitoring data — AI detection will be added later.
    </div>

    <br>

</div>
""", unsafe_allow_html=True)


# Header

h1, h2, h3 = st.columns([1, 2, 1])

with h1:
    st.markdown(
        "<div class='table-header'>PERSON ID</div>",
        unsafe_allow_html=True
    )

with h2:
    st.markdown(
        "<div class='table-header'>ACTIVITY</div>",
        unsafe_allow_html=True
    )

with h3:
    st.markdown(
        "<div class='table-header'>STATUS</div>",
        unsafe_allow_html=True
    )


# Person 1

p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    st.markdown(
        "<div class='person-row'>👤 Person #01</div>",
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        "<div class='person-row'>🪑 Sitting</div>",
        unsafe_allow_html=True
    )

with p3:
    st.markdown(
        "<div class='person-row'>🟢 Normal</div>",
        unsafe_allow_html=True
    )


# Person 2

p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    st.markdown(
        "<div class='person-row'>👤 Person #02</div>",
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        "<div class='person-row'>🚶 Walking</div>",
        unsafe_allow_html=True
    )

with p3:
    st.markdown(
        "<div class='person-row'>🟢 Normal</div>",
        unsafe_allow_html=True
    )


# Person 3

p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    st.markdown(
        "<div class='person-row'>👤 Person #03</div>",
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        "<div class='person-row'>😴 Inactive</div>",
        unsafe_allow_html=True
    )

with p3:
    st.markdown(
        "<div class='person-row'>🟡 Monitor</div>",
        unsafe_allow_html=True
    )


# =========================================================
# DETECTION TYPES
# =========================================================

st.write("")

st.markdown("""
<div class="card">

    <div class="card-title">
        🧠 Planned AI Detection
    </div>

    <br>

</div>
""", unsafe_allow_html=True)


d1, d2, d3, d4 = st.columns(4)


with d1:

    st.markdown("""
    <div class="stat-card">

        🧍

        <br><br>

        <b>Standing</b>

        <br>

        <span class="info-text">
        Normal posture
        </span>

    </div>
    """, unsafe_allow_html=True)


with d2:

    st.markdown("""
    <div class="stat-card">

        🪑

        <br><br>

        <b>Sitting</b>

        <br>

        <span class="info-text">
        Normal posture
        </span>

    </div>
    """, unsafe_allow_html=True)


with d3:

    st.markdown("""
    <div class="stat-card">

        😴

        <br><br>

        <b>Inactive</b>

        <br>

        <span class="info-text">
        Monitor duration
        </span>

    </div>
    """, unsafe_allow_html=True)


with d4:

    st.markdown("""
    <div class="stat-card">

        🚨

        <br><br>

        <b>Fall / Collapse</b>

        <br>

        <span class="info-text">
        Emergency alert
        </span>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SYSTEM FLOW
# =========================================================

st.write("")

st.markdown("""
<div class="card">

    <div class="card-title">
        ⚙️ System Flow
    </div>

    <br>

    <div style="
        text-align:center;
        font-size:15px;
        color:#172B4D;
    ">

        📷 Camera
        &nbsp;&nbsp;→&nbsp;&nbsp;
        👤 Person Detection
        &nbsp;&nbsp;→&nbsp;&nbsp;
        🦴 Pose Estimation
        &nbsp;&nbsp;→&nbsp;&nbsp;
        ⚠️ Activity Analysis
        &nbsp;&nbsp;→&nbsp;&nbsp;
        🚨 Alert

    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
    text-align:center;
    color:#9AA6B6;
    font-size:11px;
    padding:20px;
">

    SafeClass • Biomedical Engineering Project

</div>
""", unsafe_allow_html=True)
