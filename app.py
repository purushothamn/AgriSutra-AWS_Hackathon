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
    """Governance Layer: Blocks banned chemicals and enforces ethical guardrails."""
    BANNED_CHEMICALS = ["monocrotophos", "endosulfan", "paraquat", "phorate"]
    
    @classmethod
    def validate(cls, query, advice):
        query_lower = query.lower()
        for chemical in cls.BANNED_CHEMICALS:
            if chemical in query_lower or chemical in advice.lower():
                return False, f"🚨 SAFETY BLOCK: {chemical.title()} is banned/highly toxic. Please use organic alternatives like Neem oil."
        return True, advice

class ResilienceSentry:
    """Hyper-local weather monitoring and disaster preparedness."""
    @staticmethod
    def get_context(location):
        # In production, this hits a weather API. Hardcoded for MVP speed.
        return f"WARNING: Unseasonal heavy rainfall predicted in {location} within 48 hours."

class EconomicBudgeting:
    """ROI Calculator and Market Price integration."""
    @staticmethod
    def calculate_roi(crop, area_acres):
        # Simplified logic for hackathon demonstration
        prices = {"wheat": 2275, "rice": 2183, "hemp": 4500} # INR per quintal
        yield_per_acre = {"wheat": 15, "rice": 18, "hemp": 8} # quintals
        
        crop_key = crop.lower()
        if crop_key in prices:
            est_revenue = prices[crop_key] * yield_per_acre[crop_key] * area_acres
            return f"💰 Economic Projection: Estimated revenue for {area_acres} acres of {crop} is ₹{est_revenue:,} based on current MSP."
        return ""

class AgriSutraOrchestrator:
    """Routes queries and constructs the final contextual prompt for Bedrock."""
    def __init__(self, bedrock_client):
        self.bedrock = bedrock_client
        self.model_id = "us.anthropic.claude-3-haiku-20240307-v1:0" # Fixed for Ohio region

    def process_query(self, query, language, location="Bengaluru"):
        # 1. Gather Agent Contexts
        weather_context = ResilienceSentry.get_context(location)
        econ_context = EconomicBudgeting.calculate_roi("wheat", 2) # Example default injection
        
        # 2. Construct System Prompt with Context
        system_prompt = f"""
        You are AgriSutra, an expert Indian Agronomist.
        Language: {language}. Reply ONLY in this language.
        Location Context: {weather_context}
        Economic Context: {econ_context}
        
        INSTRUCTIONS:
        - Analyze the user's query.
        - If they ask about weather, incorporate the Location Context.
        - If they ask about money/yield, use the Economic Context.
        - Translate complex equipment terms into simple rural analogies (Equipment Translator requirement).
        """
        
        # 3. Call LLM
        try:
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": query}]}],
                system=[{"text": system_prompt}],
                inferenceConfig={"maxTokens": 500, "temperature": 0.2}
            )
            raw_advice = response['output']['message']['content'][0]['text']
            
            # 4. Pass through Governance Layer
            is_safe, final_advice = TrustEngine.validate(query, raw_advice)
            return final_advice, is_safe
            
        except Exception as e:
            return f"AI Service Error: {str(e)}", False

orchestrator = AgriSutraOrchestrator(bedrock)

# --- 4. AWS I/O FUNCTIONS ---

def run_stt(audio_bytes, lang_code):
    """Vernacular Voice Interface."""
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
        
        for _ in range(40): 
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                break
            time.sleep(1.5)
            
        if job_status == 'COMPLETED':
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            with urllib.request.urlopen(transcript_uri) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data['results']['transcripts'][0]['transcript']
        return None
    except Exception as e:
        st.error(f"Transcription Error: {e}")
        return None

def synthesize_speech(text, voice_id):
    """Polly integration for Vernacular output."""
    try:
        response = polly.synthesize_speech(
            Text=text, OutputFormat='mp3', VoiceId=voice_id, Engine='standard' # Fixed to standard for Ohio
        )
        return response['AudioStream'].read()
    except Exception as e:
        st.warning(f"Audio generation skipped: {e}")
        return None

# --- 5. UI LAYOUT ---

st.markdown(LOGO_SVG, unsafe_allow_html=True)
st.markdown("<h1 class='header-text'>AgriSutra</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Zero-Curve Voice-First AI Farm Manager</p>", unsafe_allow_html=True)

languages = {
    "English": {"code": "en-IN", "voice": "Raveena"}, # Raveena is standard en-IN
    "Hindi (हिंदी)": {"code": "hi-IN", "voice": "Aditi"},
    "Tamil (தமிழ்)": {"code": "ta-IN", "voice": "N/A"}, 
    "Kannada (ಕನ್ನಡ)": {"code": "kn-IN", "voice": "N/A"}
}

selected_lang = st.selectbox("Language / भाषा", list(languages.keys()))
lang_data = languages[selected_lang]

st.divider()

# Interaction Hub
st.markdown("### 🎤 Voice Consultation")
audio_data = st.audio_input("Tap the microphone to speak")

st.info("**Try asking:** 'Should I use Monocrotophos on my crops?' (Tests the Trust Engine)")

st.markdown("### 💬 Text Chat Mode")
text_query = st.text_input("Type your query here", placeholder="e.g. When is the best time to sow hemp?")

# --- 6. EXECUTION LOGIC ---
final_query = None

if audio_data:
    with st.spinner("🎙️ Transcribing audio..."):
        final_query = run_stt(audio_data.getvalue(), lang_data["code"])
        if final_query:
            st.success(f"**Heard:** {final_query}")

elif text_query:
    final_query = text_query

if final_query:
    with st.spinner("🧠 Orchestrator routing query..."):
        # Process through Orchestrator (includes Sentry, Budgeting, Trust Engine)
        advice, is_safe = orchestrator.process_query(final_query, selected_lang)
        
        st.markdown("---")
        if not is_safe:
            st.error(advice)
        else:
            st.markdown("#### 🌾 AgriSutra Advice:")
            st.write(advice)
            
            # Generate Audio if safe
            if lang_data["voice"] != "N/A":
                with st.spinner("🔊 Generating voice..."):
                    audio_response = synthesize_speech(advice, lang_data["voice"])
                    if audio_response:
                        st.audio(audio_response, format="audio/mp3")

# Sentry Dashboard Widget
st.divider()
st.error("⚠️ **Sentry Alert:** Heavy rain expected in Bengaluru. Ensure field drainage is clear.")
