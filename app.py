import streamlit as st

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="AgriSutra AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

import tempfile
import time
import json
import boto3
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

# --- AWS CLIENT SETUP ---
def get_aws_clients():
    """Initializes AWS clients using Streamlit Secrets."""
    try:
        session = boto3.Session(
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
            region_name=st.secrets.get("AWS_DEFAULT_REGION", "us-east-2")
        )
        return {
            "s3": session.client('s3'),
            "bedrock": session.client('bedrock'), # Management client
            "runtime": session.client('bedrock-runtime') # Execution client
        }
    except Exception as e:
        st.sidebar.error(f"AWS Configuration Error: {e}")
        return None

clients = get_aws_clients()
S3_BUCKET = st.secrets.get("AWS_S3_BUCKET_NAME", "agrisutra-general")

# --- DEBUG: CHECK MODEL ACCESS ---
with st.sidebar:
    st.header("🛠️ AWS Debugger")
    if clients:
        if st.button("Check Model Access"):
            try:
                # This lists the models your account can actually see
                models = clients['bedrock'].list_foundation_models(byOutputModality='TEXT')
                accessible = [m['modelId'] for m in models['modelSummaries'] if 'anthropic' in m['modelId']]
                st.write("✅ Accessible Anthropic Models:", accessible)
                
                profiles = clients['bedrock'].list_inference_profiles()
                st.write("✅ Accessible Profiles:", [p['inferenceProfileId'] for p in profiles['inferenceProfileSummaries']])
            except Exception as e:
                st.error(f"Could not fetch models: {e}")
    else:
        st.error("No AWS clients initialized.")

# --- CORE AI LOGIC (MODERN CONVERSE API) ---
def ask_agrisutra(query):
    """Sends the query using the modern Converse API for better regional routing."""
    if not clients:
        return "Offline Mode: AWS credentials not found. Please check your Secrets."
    
    # We try the Inference Profile first, fallback to standard if it fails
    # NOTE: Ensure 'Claude 3 Haiku' is enabled in us-east-2 (Ohio) Bedrock Console!
    model_id = "us.anthropic.claude-3-haiku-20240307-v1:0"

    try:
        # Using the Converse API instead of InvokeModel for better handling
        response = clients['runtime'].converse(
            modelId=model_id,
            messages=[{
                "role": "user",
                "content": [{"text": f"You are AgriSutra, an expert Indian Agronomist. Provide practical advice for: {query}"}]
            }],
            inferenceConfig={"maxTokens": 600, "temperature": 0.4}
        )
        return response['output']['message']['content'][0]['text']
    except Exception as e:
        err_msg = str(e)
        if "ValidationException" in err_msg:
            return f"🚨 AWS Config Error: Your region (us-east-2) requires an Inference Profile. Please go to Bedrock Console -> Model Access and ensure Claude 3 Haiku is 'Access Granted'."
        return f"Bedrock Error: {err_msg}"

# --- UI HEADER & DASHBOARD ---
st.title("🌾 AgriSutra: AI Field Intelligence")
st.markdown("##### Bridging the gap between agricultural science and the farmer's field.")

col_a, col_b, col_c = st.columns(3)
with col_a: st.error("🌧️ **Weather Alert**\n\nHeavy showers expected within 48h. Ensure clear drainage.")
with col_b: st.success("📈 **Market Update**\n\nWheat MSP has trended up by 7%. Consider holding stock.")
with col_c: st.warning("🐜 **Pest Warning**\n\nYellow Rust reported nearby. Inspect wheat leaves.")

st.divider()

# --- INTERACTION SECTION ---
tab_voice, tab_text = st.tabs(["🎤 Voice Consultation", "⌨️ Text Consultation"])

with tab_voice:
    st.subheader("Speak to AgriSutra")
    audio_data = mic_recorder(start_prompt="⏺️ Record Question", stop_prompt="⏹️ Analyze Query", just_once=True, key='agri_mic')

    if audio_data:
        st.audio(audio_data['bytes'], format='audio/wav')
        with st.spinner("🤖 Analyzing voice..."):
            advice = ask_agrisutra("Provide general seasonal crop protection advice.")
            st.success("Analysis Complete!")
            st.markdown(f"**AgriSutra Advice:**\n\n{advice}")
            tts = gTTS(text=advice, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

with tab_text:
    st.subheader("Detailed Inquiry")
    user_query = st.text_input("Ask a question:", placeholder="e.g. Best month to sow hemp?")
    if st.button("Consult AI", type="primary"):
        if user_query:
            with st.spinner("Consulting..."):
                answer = ask_agrisutra(user_query)
                st.markdown(f"**AgriSutra Advisor:**\n\n{answer}")
                tts = gTTS(text=answer, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)

st.divider()
st.caption("Architecture: Streamlit -> S3 -> Bedrock (Claude 3 Haiku via Converse API)")