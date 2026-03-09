import streamlit as st
import boto3
import time
import json
import uuid
import urllib.request

# --- 1. PAGE CONFIG & UI ASSETS ---
st.set_page_config(page_title="AgriSutra", page_icon="🌾", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-text { text-align: center; color: #2E7D32; font-family: sans-serif; }
    .sub-text { text-align: center; color: #555; margin-bottom: 2rem; }
    .agent-box { padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

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
    st.error(f"AWS Auth Error: {e}")
    st.stop()

# --- 3. ARCHITECTURE: AGENTS & GOVERNANCE ---

class TrustEngine:
    BANNED_CHEMICALS = ["monocrotophos", "endosulfan", "paraquat", "phorate"]
    @classmethod
    def validate(cls, query, advice):
        query_lower = query.lower()
        for chemical in cls.BANNED_CHEMICALS:
            if chemical in query_lower or chemical in advice.lower():
                return False, f"🚨 SAFETY BLOCK: {chemical.title()} is banned. Use Neem oil instead."
        return True, advice

class ResilienceSentry:
    @staticmethod
    def get_context(location):
        return f"WARNING: Unseasonal heavy rainfall predicted in {location} within 48 hours."

class EconomicBudgeting:
    @staticmethod
    def calculate_roi(crop, area_acres):
        prices = {"wheat": 2275, "rice": 2183, "hemp": 4500}
        yield_per_acre = {"wheat": 15, "rice": 18, "hemp": 8}
        crop_key = crop.lower()
        if crop_key in prices:
            est_revenue = prices[crop_key] * yield_per_acre[crop_key] * area_acres
            return f"💰 Economic Projection: Estimated revenue for {area_acres} acres of {crop} is ₹{est_revenue:,}."
        return ""

class AgriSutraOrchestrator:
    def __init__(self, bedrock_client):
        self.bedrock = bedrock_client
        self.model_id = "us.anthropic.claude-3-haiku-20240307-v1:0"

    def process_query(self, query, language, location="Bengaluru"):
        weather_context = ResilienceSentry.get_context(location)
        econ_context = EconomicBudgeting.calculate_roi("wheat", 2)
        system_prompt = f"You are AgriSutra, an expert Indian Agronomist. Language: {language}. Reply ONLY in this language."
        try:
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": query}]}],
                system=[{"text": system_prompt}],
                inferenceConfig={"maxTokens": 500, "temperature": 0.2}
            )
            raw_advice = response['output']['message']['content'][0]['text']
            return TrustEngine.validate(query, raw_advice)
        except Exception as e:
            return f"AI Service Error: {str(e)}", False

orchestrator = AgriSutraOrchestrator(bedrock)

# --- 4. AWS I/O FUNCTIONS ---

def run_stt(audio_bytes, lang_code):
    job_name = f"AgriSutra_{uuid.uuid4().hex[:8]}"
    s3_key = f"temp_audio/{job_name}.wav"
    try:
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=audio_bytes)
        audio_uri = f"s3://{S3_BUCKET}/{s3_key}"
        transcribe.start_transcription_job(TranscriptionJobName=job_name, Media={'MediaFileUri': audio_uri}, LanguageCode=lang_code)
        for _ in range(30):
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']: break
            time.sleep(1)
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            with urllib.request.urlopen(transcript_uri) as response:
                return json.loads(response.read().decode('utf-8'))['results']['transcripts'][0]['transcript']
    except Exception as e:
        st.error(f"STT Error: {e}")
    return None

def synthesize_speech(text, voice_id):
    """Polly integration supporting Neural engines for vernacular voices."""
    try:
        # Use 'neural' engine for high-quality Indian vernacular voices
        response = polly.synthesize_speech(
            Text=text, OutputFormat='mp3', VoiceId=voice_id, Engine='neural'
        )
        return response['AudioStream'].read()
    except:
        try:
            response = polly.synthesize_speech(
                Text=text, OutputFormat='mp3', VoiceId=voice_id, Engine='standard'
            )
            return response['AudioStream'].read()
        except:
            return None

# --- 5. UI LAYOUT ---

st.markdown(LOGO_SVG, unsafe_allow_html=True)
st.markdown("<h1 class='header-text'>AgriSutra</h1>", unsafe_allow_html=True)

# Updated: Active Voice IDs for all supported languages
languages = {
    "English": {"code": "en-IN", "voice": "Kajal"}, 
    "Hindi (हिंदी)": {"code": "hi-IN", "voice": "Aditi"},
    "Tamil (தமிழ்)": {"code": "ta-IN", "voice": "Vani"}, 
    "Kannada (ಕನ್ನಡ)": {"code": "kn-IN", "voice": "Hiujin"}
}

selected_lang = st.selectbox("Language / भाषा", list(languages.keys()))
lang_data = languages[selected_lang]

st.divider()
audio_data = st.audio_input("🎤 Voice Consultation")
text_query = st.text_input("💬 Text Chat Mode", placeholder="Type here...")

# --- 6. EXECUTION LOGIC (FIXED PRIORITY) ---
final_query = None

# 1. Handle Voice Input
if audio_data:
    with st.spinner("🎙️ Transcribing..."):
        voice_transcript = run_stt(audio_data.getvalue(), lang_data["code"])
        if voice_transcript:
            final_query = voice_transcript
            st.success(f"**Heard:** {final_query}")

# 2. Handle Text Input (PRIORITY OVERRIDE)
# This standalone 'if' ensures typed text takes precedence over old voice data
if text_query:
    final_query = text_query

# 3. Process the Result
if final_query:
    with st.spinner("🧠 Orchestrator routing..."):
        advice, is_safe = orchestrator.process_query(final_query, selected_lang)
        st.markdown("---")
        if not is_safe:
            st.error(advice)
        else:
            st.markdown("#### 🌾 AgriSutra Advice:")
            st.write(advice)
            if lang_data["voice"] != "N/A":
                with st.spinner("🔊 Generating voice..."):
                    audio_response = synthesize_speech(advice, lang_data["voice"])
                    if audio_response:
                        st.audio(audio_response, format="audio/mp3")

st.divider()
st.error("⚠️ **Sentry Alert:** Heavy rain expected in Bengaluru. Ensure field drainage is clear.")