import streamlit as st
import sounddevice as sd
import numpy as np
import soundfile as sf
import io
import requests
import threading

# 📌 **Recording Parameters**
SAMPLERATE = 16000  # Sample rate (16kHz for speech recognition)
CHANNELS = 1  # Mono recording
DURATION = 30  # Maximum recording duration (seconds)

# Initialize session state variables
if "recording" not in st.session_state:
    st.session_state["recording"] = False
if "recorded_audio" not in st.session_state:
    st.session_state["recorded_audio"] = None
if "input_choice" not in st.session_state:
    st.session_state["input_choice"] = "Upload"

# Streamlit UI
st.title("🎤 Call Phishing Detection")
st.write("Choose your input method:")

# 📌 **Step 1: Select Input Method**
input_choice = st.radio("Select an option:", ["Upload an audio file", "Record your voice"])

st.session_state["input_choice"] = input_choice

# 📌 **Step 2: Upload an Audio File**
if input_choice == "Upload an audio file":
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if uploaded_file:
        st.audio(uploaded_file, format="audio/wav")
        if st.button("Predict Uploaded Audio"):
            files = {"file": ("uploaded_audio.wav", uploaded_file.getvalue(), "audio/wav")}
            response = requests.post("http://127.0.0.1:8000/predict/", files=files)
            result = response.json()
            st.success(f"Prediction: {result['prediction']}")
            st.write(f"Transcript: {result['transcript']}")

# 📌 **Step 3: Record Audio Using Microphone**
elif input_choice == "Record your voice":

    def record_audio():
        """Records audio and saves it to session state."""
        st.session_state["recording"] = True
        st.write("🔴 Recording... Speak now!")

        # Record audio
        audio_data = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=CHANNELS, dtype=np.int16)
        sd.wait()  # Wait until recording is finished

        # Convert to WAV format
        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, audio_data, SAMPLERATE, format="WAV")
        
        st.session_state["recorded_audio"] = wav_buffer.getvalue()
        st.session_state["recording"] = False
        st.write("✅ Recording finished.")

    # Start Recording
    if not st.session_state["recording"]:
        if st.button("🎤 Start Recording"):
            threading.Thread(target=record_audio, daemon=True).start()

    # Stop Recording Button (Not required for `sounddevice`, recording stops automatically)
    
    # Playback recorded audio (if available)
    if st.session_state["recorded_audio"]:
        st.write("🔊 Playing back recorded audio:")
        st.audio(st.session_state["recorded_audio"], format="audio/wav")

        if st.button("Predict Recorded Audio"):
            files = {"file": ("recorded_audio.wav", st.session_state["recorded_audio"], "audio/wav")}
            response = requests.post("http://127.0.0.1:8000/predict/", files=files)
            result = response.json()
            st.success(f"Prediction: {result['prediction']}")
            st.write(f"Transcript: {result['transcript']}")
