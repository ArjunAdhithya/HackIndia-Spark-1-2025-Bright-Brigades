from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import io
import pickle
import os

app = FastAPI()

# Load the model
MODEL_PATH = "BiLSTM_Dup1_fixed.h5"  # Ensure the correct model path
TOKENIZER_PATH = "New_tokenizer.pkl"
MAX_LENGTH = 100  # Keep the same as in training

try:
    model = load_model(MODEL_PATH, compile=False)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Load the tokenizer
try:
    with open(TOKENIZER_PATH, "rb") as f:
        tokenizer = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load tokenizer: {e}")

# Function to convert speech to text
def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()

    # Convert bytes to an audio file in memory
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    temp_audio_path = "temp_audio.wav"
    audio.export(temp_audio_path, format="wav")

    # Transcribe using SpeechRecognition
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)  # Google Speech-to-Text
        except sr.UnknownValueError:
            text = "Unable to recognize speech."
        except sr.RequestError:
            text = "Speech recognition service is unavailable."

    os.remove(temp_audio_path)  # Cleanup temp file
    return text

# Function to preprocess text for model input
def preprocess_text(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding="post")
    return padded

@app.post("/predict/")
async def predict_audio(file: UploadFile = File(...)):
    try:
        audio_data = await file.read()  # Read audio file bytes
        transcript = transcribe_audio(audio_data)
        processed_text = preprocess_text(transcript)

        prediction = model.predict(processed_text)[0][0]
        label = "Phishing" if prediction > 0.5 else "Legitimate"

        return {"transcript": transcript, "prediction": label}
    
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}"}
