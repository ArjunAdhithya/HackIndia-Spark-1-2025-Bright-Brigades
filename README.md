Scam Call Phishing Detection


Project Overview


Scam calls are a growing cybersecurity threat, and existing caller identification solutions like Truecaller often fail to detect sophisticated phishing attempts. This project aims to build an AI-powered scam call detection system that analyzes call audio and transcripts to determine whether a call is fraudulent.


Features


Audio Input: Users can upload or record calls in real time.
Speech-to-Text Conversion: Converts audio to text using an ASR (Automatic Speech Recognition) model.
Speaker Diarization: Separates different speakers to isolate the scammer’s speech.
Phishing Detection Model: Uses an XGBoost machine learning model to classify calls as "Phishing Scam" or "Legitimate."
Real-Time Classification: Provides instant results for call legitimacy.
API & Web Integration: Offers an API and web interface for seamless interaction.
Enterprise & Adaptive Security Features: Continuously improves with new scam patterns and supports enterprise integration.


Project Workflow


Audio Input: User uploads or records a call.
Speech-to-Text: The system converts the audio into text.
Speaker Diarization: Identifies and isolates scammer voices.
Text Analysis: The transcript is analyzed using the trained XGBoost model.
Classification: The call is classified as "Phishing Scam" or "Legitimate."
Result Display: The result is presented via a web interface or API.


Technologies Used


Machine Learning: XGBoost, Random Forest (for initial models)
Deep Learning: ASR models for speech-to-text conversion
Web Development: Flask/FastAPI for backend, React.js for frontend
Cloud Deployment: AWS/GCP for hosting the application
Data Processing: NLTK, Scikit-learn, Pandas


Project Structure


├── dataset/                  # Phishing and legitimate call transcripts
├── models/                   # Trained ML/DL models
├── backend/                  # Flask/FastAPI backend
├── frontend/                 # React.js frontend
├── api/                      # API development
├── scripts/                  # Data preprocessing and training scripts
└── README.md                 # Project documentation



Installation & Setup


Prerequisites


Python 3.8+
Virtual environment (optional but recommended)
Node.js (for frontend development)


Backend Setup


cd backend
pip install -r requirements.txt
python app.py



Frontend Setup


cd frontend
npm install
npm start



API Usage (Example Request)


POST /predict
Content-Type: application/json
{
    "audio_file": "call_audio.wav"
}



Future Enhancements


Real-time Call Analysis: Implement live call monitoring.
Advanced NLP Models: Use transformers for better text classification.
Multi-Language Support: Expand recognition beyond English.
Integration with Telecom Providers: Enhance real-world usability.


License


This project is open-source and available under the MIT License.


Team: Bright Brigades


Abjith
Arjun
Asif
Gowsilan


Feel free to contribute and enhance this project.
