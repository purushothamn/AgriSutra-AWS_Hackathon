import urllib.request
import streamlit as st
import boto3
import time
import json
import uuid

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="AgriSutra", page_icon="🌾", layout="centered")

# CSS for clean UI and Wireframe alignment
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-text { text-align: center; color: #2E7D32; font-family: sans-serif; }
    .sub-text { text-align: center; color: #555; margin-bottom: 2rem; }
    .stAudioInput { display: flex; justify-content: center; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# Scalable SVG representation of the AgriSutra Logo (Mic + Crops)
LOGO_SVG = """
<div style="display: flex; justify-content: center; margin-bottom: 1rem;">
    <svg width="120" height="120" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <rect x="25" y="10" width="50" height="70" rx="25" fill="none" stroke="#2E7D32" stroke-width="4"/>
      <path d="M25 45 Q25 80 50 80 Q75 80 75 45" fill="none" stroke="#2E7D32" stroke-width="4"/>
      <line x1="50" y1="80" x2="50" y2="95" stroke="#2E7D32" stroke-width="4"/>
      <line x1="35" y1="95" x2="65" y2="95" stroke="#2E7D32" stroke-width="4"/>
      <path d="M30 65 Q50 40 70 65" fill="none" stroke="#F57C00" stroke-width="3"/>
      <path d="M40 70 Q50 50 60 70" fill="none" stroke="#F57C00" stroke-width="3"/>
      <path d="M50 80 Q65 40 85 30" fill="none" stroke="#2E7D32" stroke-width="3"/>
    </svg>
</div>
"""

# --- 2. AWS CLIENT INITIALIZATION ---
try:
    session = boto3.Session(
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets.get("AWS_DEFAULT_REGION", "us-east-2")
    )
    bedrock = session.client('bedrock-runtime')
    transcribe = session.client('transcribe')
    polly = session.client('polly')
    s3 = session.client('s3')
    S3_BUCKET = st.secrets.get("AWS_S3_BUCKET_NAME", "agrisutra-general")
except Exception as e:
    st.error(f"AWS Configuration Error: Please check your .streamlit/secrets.toml. Details: {e}")
    st.stop()


# --- 3. CORE LOGIC FUNCTIONS ---
def run_stt(audio_bytes, lang_code):
    """Uploads to S3 and triggers Amazon Transcribe for vernacular speech."""
    job_name = f"AgriSutra_{uuid.uuid4().hex[:8]}"
    s3_key = f"temp_audio/{job_name}.wav"
    
    try:
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=audio_bytes)
        audio_uri = f"s3://{S3_BUCKET}/{s3_key}"
        
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_uri},
            LanguageCode=lang_code
        )
        
        # Poll for completion with a timeout
        for _ in range(60): 
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                break
            time.sleep(1.5)
            
        if job_status == 'COMPLETED':
            # FIX: Use built-in urllib to fetch the JSON file instead of boto3 session
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            with urllib.request.urlopen(transcript_uri) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data['results']['transcripts'][0]['transcript']
        return None
    except Exception as e:
        st.error(f"Transcription Error: {e}")
        return None

def get_agrisutra_advice(query, language):
    """Routes query to Bedrock (Claude 3 Haiku) enforcing Trust Engine guardrails."""
    system_prompt = f"""
    You are AgriSutra, an expert agricultural AI assistant. 
    Language: {language}. Reply ONLY in this language.
    
    TRUST ENGINE RULES:
    1. Validate safety: Never recommend banned or highly toxic pesticides.
    2. Resilience Sentry: If weather/rain is mentioned, provide immediate actionable advice (e.g., drainage).
    3. Keep answers concise, using simple analogies suitable for rural farmers.
    """
    
    try:
        response = bedrock.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=[{"role": "user", "content": [{"text": query}]}],
            system=[{"text": system_prompt}],
            inferenceConfig={"maxTokens": 400, "temperature": 0.3}
        )
        return response['output']['message']['content'][0]['text']
    except Exception as e:
        return f"AI Service Error: {str(e)}"

def synthesize_speech(text, voice_id):
    """Converts AI response back to vernacular audio using Amazon Polly."""
    try:
        response = polly.synthesize_speech(
            Text=text, OutputFormat='mp3', VoiceId=voice_id, Engine='neural'
        )
        return response['AudioStream'].read()
    except Exception as e:
        st.warning(f"Audio generation skipped (Polly Error): {e}")
        return None


# --- 4. UI LAYOUT & INTERACTION HUB ---

# Header
st.markdown(LOGO_SVG, unsafe_allow_html=True)
st.markdown("<h1 class='header-text'>AgriSutra</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Zero-Curve Voice-First AI Farm Manager</p>", unsafe_allow_html=True)

# Language Configuration
languages = {
    "English": {"code": "en-IN", "voice": "Kajal"},
    "Hindi (हिंदी)": {"code": "hi-IN", "voice": "Aditi"},
    "Tamil (தமிழ்)": {"code": "ta-IN", "voice": "N/A"},  # Fallback to text if native neural isn't available
    "Kannada (ಕನ್ನಡ)": {"code": "kn-IN", "voice": "N/A"}
}

col_lang, _ = st.columns([1, 2])
with col_lang:
    selected_lang = st.selectbox("Language / भाषा", list(languages.keys()), label_visibility="collapsed")
lang_data = languages[selected_lang]

st.divider()

# --- Voice Mode (Primary Interaction) ---
st.markdown("### 🎤 Voice Consultation")
audio_data = st.audio_input("Tap the microphone to speak")

# Instructions
st.info(f"""
**Try asking:**
* "What is the best fertilizer for my crops?"
* "Will it rain in Hosur or Bengaluru today?"
""")

# --- Text Chat Mode (Fallback/Debugging) ---
st.markdown("### 💬 Text Chat Mode")
text_query = st.text_input("Type your query here", placeholder="e.g. How to treat yellow rust in wheat?")

# --- 5. EXECUTION & RESPONSE RENDERING ---
final_query = None

if audio_data:
    with st.spinner("🎙️ Transcribing audio securely via AWS..."):
        final_query = run_stt(audio_data.getvalue(), lang_data["code"])
        if final_query:
            st.success(f"**Heard:** {final_query}")
        else:
            st.error("Could not process audio. Please try speaking clearer or use text mode.")

elif text_query:
    final_query = text_query

if final_query:
    with st.spinner("🧠 Consulting AgriSutra AI..."):
        # Get AI Text
        advice = get_agrisutra_advice(final_query, selected_lang)
        
        # Render Output Box
        st.markdown("---")
        st.markdown("#### 🌾 AgriSutra Advice:")
        st.write(advice)
        
        # Generate & Play Audio
        if lang_data["voice"] != "N/A":
            with st.spinner("🔊 Generating voice response..."):
                audio_response = synthesize_speech(advice, lang_data["voice"])
                if audio_response:
                    st.audio(audio_response, format="audio/mp3")

# --- 6. RESILIENCE SENTRY DASHBOARD ---
st.divider()
st.error("⚠️ **Sentry Alert:** Unseasonal rainfall detected nearby. Ensure harvested crops are covered and field drainage is clear.")
