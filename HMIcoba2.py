import streamlit as st
import cv2
import time

# =====================================================
# PAGE CONFIG
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

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: #f5f7fb;
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
    padding-top: 2rem;
    max-width: 1300px;
}

/* HEADER */
.header {
    background: #172a46;
    padding: 25px 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.title {
    font-size: 32px;
    font-weight: 700;
}

.subtitle {
    color: #b9c8dc;
    font-size: 13px;
}

/* CARDS */
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5eaf1;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
    margin-bottom: 18px;
}

.card-title {
    color: #172a46;
    font-size: 18px;
    font-weight: 700;
}

/* STATUS */
.status-online {
    background: #e7f7ed;
    color: #229653;
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.status-warning {
    background: #fff4dc;
    color: #d89000;
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.status-danger {
    background: #ffe8e8;
    color: #d93636;
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* STAT */
.stat {
    background: white;
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #e5eaf1;
}

.stat-number {
    font-size: 27px;
    font-weight: 700;
    color: #172a46;
}

.stat-label {
    font-size: 12px;
    color: #7c8798;
}

/* CAMERA */
.camera-box {
    background: #111827;
    border-radius: 18px;
    min-height: 430px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #94a3b8;
}

/* ALERT */
.alert {
    background: #fff0f0;
    border-left: 5px solid #e04444;
    padding: 15px;
    border-radius: 10px;
    color: #8c2525;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================
if "camera_on" not in st.session_state:
    st.session_state.camera_on = False


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="header">

    <div class="title">
        🛡️ SafeClass
    </div>

    <div class="subtitle">
        Smart Classroom Safety Monitoring System
    </div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# TOP STATUS
# =====================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">01</div>
        <div class="stat-label">Camera</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">--</div>
        <div class="stat-label">People Detected</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">🟢</div>
        <div class="stat-label">System Status</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">0</div>
        <div class="stat-label">Active Alerts</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# =====================================================
# MAIN LAYOUT
# =====================================================
left, right = st.columns([2.2, 1])


# =====================================================
# CAMERA
# =====================================================
with left:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            📷 Live Camera
        </div>

        <p style="color:#7c8798;font-size:12px;">
            Camera 01 • Laptop Camera
        </p>

    </div>
    """, unsafe_allow_html=True)

    camera_placeholder = st.empty()

    start_col, stop_col = st.columns(2)

    with start_col:
        if st.button(
            "▶ Start Camera",
            use_container_width=True
        ):
            st.session_state.camera_on = True

    with stop_col:
        if st.button(
            "⏹ Stop Camera",
            use_container_width=True
        ):
            st.session_state.camera_on = False


# =====================================================
# INFORMATION PANEL
# =====================================================
with right:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            📊 Monitoring Status
        </div>

        <br>

        <span class="status-online">
            ● SYSTEM ACTIVE
        </span>

        <br><br>

        <b>Camera</b>
        <br>
        <span style="color:#7c8798;">
        Laptop Webcam
        </span>

        <br><br>

        <b>Detection Mode</b>
        <br>
        <span style="color:#7c8798;">
        Basic Camera Preview
        </span>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🚨 Alert System
        </div>

        <br>

        <div style="
            background:#e8f7ee;
            padding:12px;
            border-radius:10px;
            color:#258b50;
        ">
            🟢 No abnormal activity detected
        </div>

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# CAMERA LOOP
# =====================================================
if st.session_state.camera_on:

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        st.error(
            "Kamera tidak dapat dibuka. "
            "Pastikan kamera laptop tersedia."
        )

    else:

        while st.session_state.camera_on:

            ret, frame = cap.read()

            if not ret:
                st.error("Gagal membaca kamera.")
                break

            # Mirror camera
            frame = cv2.flip(frame, 1)

            # Convert BGR → RGB
            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            camera_placeholder.image(
                frame_rgb,
                channels="RGB",
                use_container_width=True
            )

            time.sleep(0.03)

        cap.release()


# =====================================================
# DETECTION INFORMATION
# =====================================================
st.write("")

st.markdown("""
<div class="card">

    <div class="card-title">
        👥 People Monitoring
    </div>

    <br>

    <table style="width:100%;border-collapse:collapse;">

        <tr style="color:#7c8798;font-size:13px;">
            <th align="left">Person ID</th>
            <th align="left">Activity</th>
            <th align="left">Status</th>
        </tr>

        <tr>
            <td>Person #01</td>
            <td>Waiting for AI</td>
            <td>⚪ --</td>
        </tr>

        <tr>
            <td>Person #02</td>
            <td>Waiting for AI</td>
            <td>⚪ --</td>
        </tr>

        <tr>
            <td>Person #03</td>
            <td>Waiting for AI</td>
            <td>⚪ --</td>
        </tr>

    </table>

</div>
""", unsafe_allow_html=True)


# =====================================================
# SYSTEM FLOW
# =====================================================
st.markdown("""
<div class="card">

    <div class="card-title">
        ⚙️ System Flow
    </div>

    <br>

    <div style="
        text-align:center;
        font-size:16px;
        color:#172a46;
    ">

        📷 Camera
        &nbsp; →
        👤 Person Detection
        &nbsp; →
        🦴 Pose Detection
        &nbsp; →
        ⚠️ Abnormal Activity
        &nbsp; →
        🚨 Alert

    </div>

</div>
""", unsafe_allow_html=True)
