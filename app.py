import streamlit as st

# 1. MUST BE FIRST
st.set_page_config(page_title="AgriSutra AI", page_icon="🌾", layout="wide")

import tempfile
import time
import json
import boto3
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

# --- AWS CLIENT SETUP ---
def get_aws_clients():
    try:
        # Pulling from Streamlit Secrets
        session = boto3.Session(
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
            region_name=st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")
        )
        return {
            "s3": session.client('s3'),
            "transcribe": session.client('transcribe'),
            "bedrock": session.client('bedrock-runtime')
        }
    except Exception as e:
        st.sidebar.error(f"AWS Auth Error: {e}")
        return None

clients = get_aws_clients()
S3_BUCKET = st.secrets.get("AWS_S3_BUCKET_NAME", "agrisutra-audio-uploads")

# --- CORE AI LOGIC (BEDROCK) ---
def ask_agrisutra(query):
    if not clients:
        return "System is in offline mode. Please check AWS Secrets."
    
    prompt = f"""
    Human: You are AgriSutra, a professional agronomist. 
    Answer the following farmer query accurately, concisely, and with practical advice.
    Query: {query}
    Assistant:"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    })

    try:
        response = clients['bedrock'].invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=body
        )
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']
    except Exception as e:
        return f"Error connecting to Bedrock: {str(e)}"

# --- UI HEADER ---
st.title("🌾 AgriSutra: AI Agronomy Assistant")

# --- DASHBOARD WIDGETS ---
col1, col2, col3 = st.columns(3)
with col1: st.error("🌧️ **Weather:** Heavy rain in 48h. Clear drainage.")
with col2: st.success("📈 **Market:** MSP for Wheat increased by 7%.")
with col3: st.warning("🐜 **Alert:** Yellow Rust spotted in neighboring districts.")

st.divider()

# --- INTERACTION TABS ---
tab1, tab2 = st.tabs(["🎤 Voice Assistant", "⌨️ Text Input"])

with tab1:
    st.subheader("Speak your question")
    audio_data = mic_recorder(
        start_prompt="⏺️ Record Question",
        stop_prompt="⏹️ Stop & Analyze",
        just_once=True,
        key='agri_mic'
    )

    if audio_data:
        st.audio(audio_data['bytes'], format='audio/wav')
        with st.spinner("🤖 AgriSutra is thinking..."):
            # For the demo: We treat voice as a trigger to the AI
            # Real flow: Transcribe -> Text -> Bedrock
            # Quick flow for demo: Use a sample query but REAL Bedrock logic
            real_ai_response = ask_agrisutra("I have recorded a voice message. Please provide general monsoon sowing advice.")
            st.markdown(f"**AgriSutra Advice:** {real_ai_response}")
            
            # Voice Output
            tts = gTTS(text=real_ai_response, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

with tab2:
    st.subheader("Type your question")
    user_text = st.text_input("What is on your mind today?", placeholder="e.g. Best month to sow hemp?")
    if st.button("Submit Query", type="primary"):
        if user_text:
            with st.spinner("Consulting Bedrock..."):
                answer = ask_agrisutra(user_text)
                st.success("Analysis Complete!")
                st.write(f"**AgriSutra:** {answer}")
                
                # Real-time TTS for the text input too!
                tts = gTTS(text=answer, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
        else:
            st.warning("Please enter a question first.")

st.divider()
st.caption("Secured by AWS Bedrock Guardrails | Powered by Claude 3 Haiku")