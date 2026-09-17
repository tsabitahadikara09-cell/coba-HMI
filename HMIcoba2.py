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

.stApp {
    background-color: #F5F7FB;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

/* Header */
.header-box {
    background-color: #172B4D;
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.header-title {
    color: white;
    font-size: 34px;
    font-weight: 700;
}

.header-subtitle {
    color: #C8D8ED;
    font-size: 14px;
    margin-top: 5px;
}

/* Card */
.card-box {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    margin-bottom: 15px;
}

/* Stat */
.stat-box {
    background-color: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    text-align: center;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #172B4D;
}

.stat-label {
    font-size: 12px;
    color: #718096;
}

/* Person */
.person-box {
    background-color: #F8FAFC;
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CAMERA PROCESSOR
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

st.markdown(
    '<div class="header-box">'
    '<div class="header-title">🛡️ SafeClass</div>'
    '<div class="header-subtitle">'
    'Smart Classroom Safety Monitoring System'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# STATISTICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        '<div class="stat-box">'
        '<div class="stat-number">01</div>'
        '<div class="stat-label">Camera</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="stat-box">'
        '<div class="stat-number">40</div>'
        '<div class="stat-label">Class Capacity</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="stat-box">'
        '<div class="stat-number">🟢</div>'
        '<div class="stat-label">System Active</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        '<div class="stat-box">'
        '<div class="stat-number">0</div>'
        '<div class="stat-label">Active Alerts</div>'
        '</div>',
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# MAIN CAMERA + STATUS
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
    st.caption("AI Activity Monitoring")

    st.write("**People Detected**")

    st.metric(
        label="Current",
        value="3"
    )

    st.divider()

    st.subheader("🚨 Alert System")

    st.success(
        "🟢 No abnormal activity detected."
    )


# =========================================================
# PEOPLE MONITORING
# =========================================================

st.divider()

st.subheader("👥 People Monitoring")

st.caption(
    "Monitoring aktivitas setiap orang yang terdeteksi kamera."
)


# Header tabel

c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.caption("PERSON ID")

with c2:
    st.caption("ACTIVITY")

with c3:
    st.caption("STATUS")


# =========================================================
# PERSON 1
# =========================================================

c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.write("👤 Person #01")

with c2:
    st.write("🪑 Sitting")

with c3:
    st.success("NORMAL")


# =========================================================
# PERSON 2
# =========================================================

c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.write("👤 Person #02")

with c2:
    st.write("🚶 Walking")

with c3:
    st.success("NORMAL")


# =========================================================
# PERSON 3
# =========================================================

c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.write("👤 Person #03")

with c2:
    st.write("😴 Inactive")

with c3:
    st.warning("MONITOR")


# =========================================================
# ACTIVITY DETECTION
# =========================================================

st.divider()

st.subheader("🧠 Activity Detection")

d1, d2, d3, d4 = st.columns(4)

with d1:
    st.info(
        "🧍\n\n"
        "**Standing**\n\n"
        "Normal posture"
    )

with d2:
    st.info(
        "🪑\n\n"
        "**Sitting**\n\n"
        "Normal posture"
    )

with d3:
    st.warning(
        "😴\n\n"
        "**Inactive**\n\n"
        "Monitor duration"
    )

with d4:
    st.error(
        "🚨\n\n"
        "**Fall / Collapse**\n\n"
        "Emergency alert"
    )


# =========================================================
# SYSTEM FLOW
# =========================================================

st.divider()

st.subheader("⚙️ System Flow")

flow = st.columns(5)

with flow[0]:
    st.info("📷\n\n**Camera**")

with flow[1]:
    st.info("👤\n\n**Person Detection**")

with flow[2]:
    st.info("🦴\n\n**Pose Estimation**")

with flow[3]:
    st.warning("⚠️\n\n**Activity Analysis**")

with flow[4]:
    st.error("🚨\n\n**Alert**")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SafeClass • Biomedical Engineering Project"
)
