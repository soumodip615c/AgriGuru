import streamlit as st
import base64
import sys
import os
from pathlib import Path
from streamlit_mic_recorder import mic_recorder

# =====================================
# Project Path Setup
# =====================================
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.main import get_answer, save_history
from models.speech_to_text import transcribe_audio
from models.text_to_speech import text_to_speech
from models.disease_detector import predict_disease

# =====================================
# Page Config
# =====================================
st.set_page_config(
    page_title="AgriGuru",
    page_icon="🌾",
    layout="wide"
)

# =====================================
# Load Image
# =====================================
def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

assets_dir = project_root / "frontend" / "assets"

background_path = assets_dir / "background.jpg"
logo_path = assets_dir / "logo.png"

bg_image = get_base64(background_path)

# =====================================
# CSS
# =====================================
st.markdown(
    f"""
    <style>

    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.25);
        z-index: -1;
    }}

    .hero-card {{
        background: rgba(0,0,0,0.45);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        padding: 50px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }}

    .hero-card h1 {{
        color: white;
        font-size: 60px;
        margin-bottom: 10px;
    }}

    .hero-card h3 {{
        color: white;
        font-size: 25px;
        font-weight: 400;
    }}

    .response-box {{
        background: rgba(0,0,0,0.75);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 25px;
        margin-top: 25px;
        margin-bottom: 20px;
        color: white;
        font-size: 18px;
        line-height: 1.8;
        max-height: 500px;
        overflow-y: auto;
    }}

    .response-title {{
        font-size: 28px;
        font-weight: bold;
        color: #90EE90;
        margin-bottom: 15px;
    }}
    .disease-box {{
    background: rgba(0,0,0,0.75);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    margin-bottom: 20px;
    color: white;
}}

.disease-title {{
    font-size: 28px;
    font-weight: bold;
    color: #90EE90;
    margin-bottom: 15px;
}}

.disease-item {{
    font-size: 18px;
    line-height: 1.8;
}}

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# Session State
# =====================================
if "answer" not in st.session_state:
    st.session_state.answer = ""

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "audio_path" not in st.session_state:
    st.session_state.audio_path = ""
    
if "disease_result" not in st.session_state:
    st.session_state.disease_result = None

# =====================================
# Logo
# =====================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(str(logo_path), width=350)

# =====================================
# Hero Section
# =====================================
st.markdown(
    """
    <div class="hero-card">
        <h1>🌾 AgriGuru</h1>
        <h3>Your Smart Agricultural Assistant</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# Text Input
# =====================================
question = st.text_input(
    "Ask AgriGuru",
    placeholder="Ask about crops, soil, fertilizers, pests, irrigation...",
    label_visibility="collapsed"
)

if st.button("🚜 Get Advice", use_container_width=True):

    if question.strip():

        with st.spinner("🌱 AgriGuru is thinking..."):

            answer = get_answer(question)

            st.session_state.answer = answer
            st.session_state.transcript = ""
            st.session_state.audio_path = ""  
            save_history(question, answer)

    else:
        st.warning("Please enter a question.")

# =====================================
# Live Voice Recording
# =====================================
st.subheader("🎤 Live Voice Question")

audio = mic_recorder(
    start_prompt="🎙 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True,
    use_container_width=True
)

if audio:

    os.makedirs("input/audio", exist_ok=True)

    live_audio_path = os.path.join(
        "input",
        "audio",
        "live_recording.wav"
    )

    with open(live_audio_path, "wb") as f:
        f.write(audio["bytes"])

    with st.spinner("🎤 Transcribing..."):

        transcript = transcribe_audio(live_audio_path)
        st.session_state.transcript = transcript

    with st.spinner("🌱 Generating answer..."):

        answer = get_answer(transcript)

        st.session_state.answer = answer
        st.session_state.audio_path = ""
        

        save_history(transcript, answer)

# =====================================
# Audio Upload
# =====================================
st.subheader("📤 Upload Voice Question")

uploaded_audio = st.file_uploader(
    "Upload WAV / MP3 / M4A",
    type=["wav", "mp3", "m4a"]
)

if uploaded_audio is not None:

    if st.button("🎧 Process Uploaded Audio", use_container_width=True):

        os.makedirs("input/audio", exist_ok=True)

        audio_path = os.path.join(
            "input",
            "audio",
            uploaded_audio.name
        )

        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())

        with st.spinner("🎤 Transcribing..."):

            transcript = transcribe_audio(audio_path)
            st.session_state.transcript = transcript

        with st.spinner("🌱 Generating answer..."):

            answer = get_answer(transcript)

            st.session_state.answer = answer
            st.session_state.audio_path = ""

            save_history(transcript, answer)

# =====================================
# Transcript
# =====================================
if st.session_state.transcript:

    st.info(
        f"🎤 Transcribed Question: {st.session_state.transcript}"
    )


# =====================================
# Plant Disease Detection
# =====================================

st.subheader("🌿 Plant Disease Detection")

uploaded_image = st.file_uploader(
    "Upload Leaf Image",
    type=["jpg", "jpeg", "png"],
    key="disease_uploader"
)

if uploaded_image is not None:

    st.image(
        uploaded_image,
        caption="Uploaded Leaf Image",
        use_container_width=True
    )

    if st.button(
        "🔍 Detect Disease",
        use_container_width=True
    ):

        os.makedirs(
            "input/images",
            exist_ok=True
        )

        image_path = os.path.join(
            "input",
            "images",
            uploaded_image.name
        )

        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

        with st.spinner(
            "🌿 Detecting Disease..."
        ):

            result = predict_disease(
                image_path
            )

            st.session_state.disease_result = result
# PASTE THE RESULT BLOCK HERE 👇

if st.session_state.disease_result:

    confidence = st.session_state.disease_result["confidence"]

    if confidence >= 90:
        st.success("🟢 High Confidence")
    elif confidence >= 70:
        st.warning("🟡 Medium Confidence")
    else:
        st.error("🔴 Low Confidence")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Disease",
            st.session_state.disease_result["disease"]
        )

    with col2:
        st.metric(
            "Confidence",
            f"{confidence}%"
        )
# =====================================
# Response
# =====================================
# =====================================
# Response
# =====================================
if st.session_state.answer:

    st.markdown(
        f"""
        <div class="response-box">
            <div class="response-title">
                🌱 AgriGuru Response
            </div>
            <hr>
            {st.session_state.answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate Voice Button
    if st.button("🔊 Generate Voice"):

        with st.spinner("Generating Voice..."):

            audio_path = text_to_speech(
                st.session_state.answer
            )

            st.session_state.audio_path = audio_path

    # Audio Player
    if st.session_state.audio_path:

        st.subheader("🔊 Listen to AgriGuru")

        st.audio(
            st.session_state.audio_path,
            format="audio/mp3"
        )

    # Clear Button
    if st.button("🗑 Clear Response"):

        st.session_state.answer = ""
        st.session_state.transcript = ""
        st.session_state.audio_path = ""

        st.rerun()
# =====================================
# Sidebar History
# =====================================

st.sidebar.title("📜 Conversation History")

history_file = Path("output/history.txt")

if history_file.exists():

    with open(
        history_file,
        "r",
        encoding="utf-8"
    ) as f:

        history_text = f.read()

    st.sidebar.text_area(
        "Saved Conversations",
        value=history_text,
        height=500
    )

    if st.sidebar.button(
        "🗑 Clear History",
        use_container_width=True
    ):

        with open(
            history_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("")

        st.sidebar.success(
            "History Cleared Successfully!"
        )

        st.rerun()

else:

    st.sidebar.info(
        "No conversation history found."
    )

# =====================================
# Footer
# =====================================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        background:rgba(0,0,0,0.55);
        color:white;
        text-align:center;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
    ">
        🌾 Smart Farming • Better Yield • Better Future
    </div>
    """,
    unsafe_allow_html=True
)
