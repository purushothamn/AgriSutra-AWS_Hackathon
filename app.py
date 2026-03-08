import streamlit as st

# 1. CRITICAL: Must be the first line.
st.set_page_config(page_title="AgriSutra AI", page_icon="🌾", layout="wide")

import tempfile
import time
import json
import uuid
import requests
import boto3
from gtts import gTTS

# Safely import the mic recorder
try:
    from streamlit_mic_recorder import mic_recorder
except ImportError:
    mic_recorder = None

# ==========================================
# ⚙️ AWS CONFIGURATION & CLIENTS
# ==========================================
def get_aws_clients():
    try:
        # Pulls securely from Streamlit Cloud Secrets
        session = boto3.Session(
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
            region_name=st.secrets.get("AWS_DEFAULT_REGION", "us-east-2")
        )
        return {
            "s3": session.client('s3'),
            "transcribe": session.client('transcribe'),
            "bedrock": session.client('bedrock-runtime')
        }
    except Exception as e:
        return None

clients = get_aws_clients()
S3_BUCKET = st.secrets.get("AWS_S3_BUCKET_NAME", "agrisutra-general")

# ==========================================
# 🧠 AWS BEDROCK (LLM) LOGIC
# ==========================================
def ask_bedrock(prompt_text):
    if not clients:
        return _mock_agronomy_response(prompt_text)
    
    try:
        # Using Claude 3 Haiku for fast, cheap, smart responses
        model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": f"You are an expert agronomist in India. Give a short, actionable answer to this farmer's query: {prompt_text}"}]
        }
        
        response = clients["bedrock"].invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps(payload)
        )
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']
    except Exception as e:
        print(f"Bedrock Error: {e}")
        return _mock_agronomy_response(prompt_text)

# ==========================================
# 🎤 AWS TRANSCRIBE & S3 LOGIC
# ==========================================
def process_audio_to_text(audio_bytes):
    if not clients:
        return "Simulated text: How should I manage my crops before the rain?"

    job_name = f"agrisutra_voice_{int(time.time())}"
    file_name = f"{job_name}.wav"
    
    try:
        # 1. Upload to S3
        clients["s3"].put_object(Bucket=S3_BUCKET, Key=file_name, Body=audio_bytes)
        s3_uri = f"s3://{S3_BUCKET}/{file_name}"
        
        # 2. Start Transcribe Job
        clients["transcribe"].start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='wav',
            LanguageCode='en-IN' # Indian English (change to hi-IN for Hindi if needed)
        )
        
        # 3. Wait for Job to Complete
        while True:
            status = clients["transcribe"].get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                break
            time.sleep(2)
            
        if job_status == 'COMPLETED':
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_response = requests.get(transcript_uri)
            transcript_json = transcript_response.json()
            return transcript_json['results']['transcripts'][0]['transcript']
        else:
            return "Audio processing failed. Please try text input."
            
    except Exception as e:
        print(f"Transcribe Error: {e}")
        return "Could not connect to AWS Transcribe. (Simulated input used)."

# ==========================================
# 🔊 VOICE OUTPUT (Google TTS Fallback)
# ==========================================
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en', tld='co.in') # Indian English accent
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")
    except Exception as e:
        st.error("Audio generation failed.")

def _mock_agronomy_response(text):
    return f"Based on your query '{text}', ensure proper soil drainage due to the upcoming rain alerts. If planning to apply urea, delay until after the showers pass to prevent nitrogen runoff and protect soil health."

# ==========================================
# 🖥️ FRONTEND UI (DASHBOARD)
# ==========================================
st.title("🌾 AgriSutra")
st.markdown("### Intelligent Agronomy & Context-Aware Assistant")
st.divider()

# --- CONTEXT NOTIFICATIONS ---
st.markdown("#### 📡 Real-Time Field Intelligence")
col1, col2, col3 = st.columns(3)
with col1:
    st.error("🌧️ **WEATHER ALERT (Hosur)**\n\n80% chance of heavy rain in 3 days. **Action:** Delay pesticide spraying & clear drainage.")
with col2:
    st.success("📰 **MARKET UPDATE**\n\nGovt announces 5% increase in Minimum Support Price (MSP) for upcoming rabi crops.")
with col3:
    st.info("🚜 **SOIL SENSOR (Mock)**\n\nMoisture: 42% (Optimal). Nitrogen levels slightly low in Sector B.")

st.divider()

# --- MAIN INTERACTION TABS ---
st.markdown("#### 🧑‍🌾 Consult AgriSutra AI")
tab1, tab2 = st.tabs(["🎤 Voice Assistant (AWS Transcribe)", "⌨️ Text Input (AWS Bedrock)"])

def handle_query(query_text):
    with st.spinner("🧠 AWS Bedrock analyzing field context..."):
        # Call the Bedrock API
        answer = ask_bedrock(query_text)
        
        st.success("Analysis Complete!")
        st.markdown(f"> **AgriSutra:** {answer}")
        
        # Play the audio response
        speak_text(answer)

with tab1:
    st.write("Tap the microphone to speak your question. Audio is routed to AWS S3 and processed by Amazon Transcribe.")
    if mic_recorder:
        audio_data = mic_recorder(start_prompt="⏺️ Start Recording", stop_prompt="⏹️ Stop Recording", key='mic')
        
        if audio_data:
            with st.spinner("🎧 Uploading to S3 & Processing via AWS Transcribe..."):
                # Convert raw bytes to text using AWS
                transcribed_text = process_audio_to_text(audio_data['bytes'])
            
            st.info(f"**Transcribed Text:** {transcribed_text}")
            handle_query(transcribed_text)
    else:
        st.warning("⚠️ `streamlit-mic-recorder` not found. Please add to requirements.txt.")

with tab2:
    user_query = st.text_input("Type your agronomy question here:")
    if st.button("Submit Text Query", type="primary"):
        if user_query:
            handle_query(user_query)
        else:
            st.error("Please enter a question.")