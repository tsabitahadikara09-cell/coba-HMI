import streamlit as st
import random
import time

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Hand Hero",
    page_icon="🖐️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: #f4f7fc;
}

/* Hide Streamlit default */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Header */
.hero {
    background: linear-gradient(135deg, #0d1b35, #173865);
    padding: 25px 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 3px;
}

.hero-subtitle {
    color: #bcd7ff;
    font-size: 14px;
}

/* Cards */
.card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 4px 15px rgba(20,40,80,0.07);
    border: 1px solid #e8edf5;
    margin-bottom: 18px;
}

.card-title {
    color: #13294b;
    font-size: 18px;
    font-weight: 700;
}

.big-number {
    color: #172f57;
    font-size: 32px;
    font-weight: 700;
}

.small-text {
    color: #77839a;
    font-size: 12px;
}

/* Stat cards */
.stat {
    background: white;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    border: 1px solid #e7edf5;
}

.stat-icon {
    font-size: 28px;
}

.stat-value {
    font-size: 23px;
    font-weight: 700;
    color: #17345e;
}

.stat-label {
    color: #7b879b;
    font-size: 12px;
}

/* Game card */
.game-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    border: 1px solid #e4eaf3;
    height: 100%;
}

.game-icon {
    font-size: 45px;
}

.game-title {
    font-size: 18px;
    font-weight: 700;
    color: #17345e;
}

.game-description {
    color: #718096;
    font-size: 13px;
}

/* Game screen */
.game-screen {
    background: linear-gradient(180deg, #cceeff, #edf8ff);
    border-radius: 25px;
    padding: 40px;
    text-align: center;
    min-height: 420px;
    border: 1px solid #d9eaf5;
}

.apple {
    font-size: 100px;
    margin: 35px 0;
}

.hand {
    font-size: 80px;
}

/* Progress */
.progress-bg {
    background: #e8edf5;
    border-radius: 20px;
    height: 13px;
    overflow: hidden;
}

.progress-fill {
    background: linear-gradient(90deg, #3588f5, #65b8ff);
    height: 100%;
    border-radius: 20px;
}

/* Badge */
.badge {
    display: inline-block;
    background: #e8f7ee;
    color: #2e9d5b;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* Navigation */
.nav-title {
    font-size: 25px;
    font-weight: 700;
    color: #152d50;
    margin-bottom: 5px;
}

.nav-subtitle {
    color: #7a879b;
    font-size: 13px;
    margin-bottom: 20px;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: none;
    background: #3988f5;
    color: white;
    font-weight: 600;
    height: 45px;
}

.stButton > button:hover {
    background: #2674dc;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1b35;
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "score" not in st.session_state:
    st.session_state.score = 120

if "repetitions" not in st.session_state:
    st.session_state.repetitions = 12

if "rom" not in st.session_state:
    st.session_state.rom = 75

if "accuracy" not in st.session_state:
    st.session_state.accuracy = 88


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("""
    <h2>🖐️ Hand Hero</h2>
    <p style="color:#aebbd0;">Rehabilitation Game</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠  Home", use_container_width=True):
        st.session_state.page = "Home"

    if st.button("🎮  Training", use_container_width=True):
        st.session_state.page = "Training"

    if st.button("📊  Progress", use_container_width=True):
        st.session_state.page = "Progress"

    if st.button("⚙️  Settings", use_container_width=True):
        st.session_state.page = "Settings"

    st.markdown("---")

    st.markdown("""
    <small>
    Hardware Status<br>
    🟢 ESP32 Connected<br>
    🟢 Flex Sensor Ready
    </small>
    """, unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">🖐️ Hand Hero</div>
    <div class="hero-subtitle">
        Rehabilitation Game for a Stronger Tomorrow
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HOME
# =========================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="nav-title">Hello, Sarah! 👋</div>
    <div class="nav-subtitle">
        Keep going, you're doing great!
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1])

    with col1:

        st.markdown("""
        <div class="card">
            <div class="card-title">Today's Progress</div>
            <br>
            <div style="font-size:45px;font-weight:700;color:#3988f5;">
                80%
            </div>
            <div class="small-text">
                12 / 15 Exercises Completed
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶ Start Training", use_container_width=True):
            st.session_state.page = "Training"
            st.rerun()

    with col2:

        st.markdown("""
        <div class="card">
            <div class="card-title">Training Goal</div>
            <br>
            <span class="badge">Active</span>
            <br><br>
            <b>Improve Finger Mobility</b>
            <p class="small-text">
                Complete 15 repetitions per session.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Quick Stats")

    c1, c2, c3, c4 = st.columns(4)

    stats = [
        ("🖐️", "75°", "ROM"),
        ("🔄", "12", "Repetitions"),
        ("🎯", "88%", "Accuracy"),
        ("⏱️", "15:32", "Training Time")
    ]

    for col, stat in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="stat">
                <div class="stat-icon">{stat[0]}</div>
                <div class="stat-value">{stat[1]}</div>
                <div class="stat-label">{stat[2]}</div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# TRAINING
# =========================================================
elif st.session_state.page == "Training":

    st.markdown("""
    <div class="nav-title">Choose Your Training 🎮</div>
    <div class="nav-subtitle">
        Select a game and start your rehabilitation.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    games = [
        ("🍎", "Grab the Apple", "Bend your fingers to grab the apple.", "Level 1 • Easy"),
        ("⭐", "Catch the Star", "Move your hand left and right.", "Level 2 • Medium"),
        ("🎈", "Squeeze the Balloon", "Bend your fingers gradually.", "Level 3 • Hard")
    ]

    for col, game in zip([c1, c2, c3], games):

        with col:

            st.markdown(f"""
            <div class="game-card">
                <div class="game-icon">{game[0]}</div>
                <br>
                <div class="game-title">{game[1]}</div>
                <p class="game-description">
                    {game[2]}
                </p>
                <span class="badge">{game[3]}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"Play {game[1]}",
                key=game[1],
                use_container_width=True
            ):
                st.session_state.page = "Game"
                st.rerun()


# =========================================================
# GAME
# =========================================================
elif st.session_state.page == "Game":

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown("""
        <div class="game-screen">

            <div style="
                display:flex;
                justify-content:space-between;
                font-weight:700;
                color:#17345e;
            ">
                <span>⭐ SCORE : 120</span>
                <span>⏸</span>
            </div>

            <div class="apple">🍎</div>

            <div class="hand">🖐️</div>

            <h3>Grab the Apple!</h3>

            <p>
                Bend your fingers to grab the apple.
            </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">
            <div class="card-title">Live Sensor Data</div>
            <br>
        """, unsafe_allow_html=True)

        finger_bend = random.randint(65, 80)
        finger_angle = random.randint(60, 75)

        st.metric("Finger Bend", f"{finger_bend}%")
        st.progress(finger_bend / 100)

        st.metric("Finger Angle", f"{finger_angle}°")

        st.markdown("""
        <hr>
        <span class="badge">🟢 Good Movement</span>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Finish Training", use_container_width=True):
            st.session_state.page = "Result"
            st.rerun()


# =========================================================
# RESULT
# =========================================================
elif st.session_state.page == "Result":

    st.markdown("""
    <div style="
        text-align:center;
        background:white;
        border-radius:25px;
        padding:40px;
    ">

        <div style="font-size:70px;">🏆</div>

        <h1 style="color:#17345e;">
            Training Complete!
        </h1>

        <p style="color:#77839a;">
            Great job! Keep up the progress.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    results = [
        ("⭐", "850", "Score"),
        ("🔄", "20", "Repetitions"),
        ("🖐️", "75°", "ROM"),
        ("🎯", "88%", "Accuracy")
    ]

    for col, result in zip([c1, c2, c3, c4], results):

        with col:

            st.markdown(f"""
            <div class="stat">
                <div class="stat-icon">{result[0]}</div>
                <div class="stat-value">{result[1]}</div>
                <div class="stat-label">{result[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="card">
        <div class="card-title">
            Movement Progress
        </div>
        <br>

        <div class="progress-bg">
            <div class="progress-fill" style="width:88%;"></div>
        </div>

        <br>

        <span class="badge">
            88% Accuracy
        </span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("📊 View Progress", use_container_width=True):
            st.session_state.page = "Progress"
            st.rerun()

    with c2:
        if st.button("🎮 Train Again", use_container_width=True):
            st.session_state.page = "Training"
            st.rerun()


# =========================================================
# PROGRESS
# =========================================================
elif st.session_state.page == "Progress":

    st.markdown("""
    <div class="nav-title">Your Progress 📊</div>
    <div class="nav-subtitle">
        Track your rehabilitation journey.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Average ROM", "75°", "+8°")

    with c2:
        st.metric("Average Accuracy", "88%", "+5%")

    with c3:
        st.metric("Total Repetitions", "126", "+24")

    st.write("")

    st.markdown("""
    <div class="card">
        <div class="card-title">
            📈 ROM Progress
        </div>
        <br>
    </div>
    """, unsafe_allow_html=True)

    # Simple chart using Streamlit
    chart_data = {
        "Mon": 48,
        "Tue": 55,
        "Wed": 60,
        "Thu": 64,
        "Fri": 68,
        "Sat": 72,
        "Sun": 75
    }

    st.line_chart(chart_data)

    st.markdown("""
    <div class="card">
        <div class="card-title">
            Recent Sessions
        </div>
        <br>

        🟢 <b>Grab the Apple</b>
        <br>
        <small>20 reps • Accuracy 88%</small>

        <hr>

        ⭐ <b>Catch the Star</b>
        <br>
        <small>15 reps • Accuracy 82%</small>

        <hr>

        🎈 <b>Squeeze the Balloon</b>
        <br>
        <small>12 reps • Accuracy 79%</small>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SETTINGS
# =========================================================
elif st.session_state.page == "Settings":

    st.markdown("""
    <div class="nav-title">Settings ⚙️</div>
    <div class="nav-subtitle">
        Customize your rehabilitation training.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">🎯 Training Target</div>
        <br>
    </div>
    """, unsafe_allow_html=True)

    repetitions = st.slider(
        "Target Repetitions",
        min_value=5,
        max_value=50,
        value=20
    )

    rom_target = st.slider(
        "Target ROM",
        min_value=30,
        max_value=120,
        value=75
    )

    st.success(
        f"Target set to {repetitions} repetitions and {rom_target}° ROM."
    )

    st.markdown("""
    <div class="card">
        <div class="card-title">🔌 Hardware</div>
        <br>
        🟢 ESP32 — Connected
        <br><br>
        🟢 Flex Sensor — Ready
        <br><br>
        ⚪ MPU6050 — Optional
    </div>
    """, unsafe_allow_html=True)
