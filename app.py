import streamlit as st
import boto3
import json
import io
import time

# --- AWS CONFIGURATION ---
# These are pulled from your previous setup or st.secrets
AWS_REGION = "us-east-1"
S3_BUCKET = st.secrets.get("AWS_S3_BUCKET_NAME", "agrisutra-general")

# Initialize AWS Clients
session = boto3.Session(
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=AWS_REGION
)

bedrock = session.client('bedrock-runtime')  # For AI Logic
transcribe = session.client('transcribe')    # For Voice-to-Text
polly = session.client('polly')              # For Vernacular TTS
s3 = session.client('s3')                    # For Audio Storage

# --- 1. SPEECH-TO-TEXT: AMAZON TRANSCRIBE ---
def transcribe_voice(audio_bytes, language_code):
    """Uploads to S3 and triggers Amazon Transcribe for Indian Dialects."""
    job_name = f"AgriSutra_Job_{int(time.time())}"
    s3_key = f"recordings/{job_name}.wav"
    
    # Upload to S3
    s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=audio_bytes)
    audio_uri = f"s3://{S3_BUCKET}/{s3_key}"
    
    # Start Transcription
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_uri},
        LanguageCode=language_code
    )
    
    # Simple Polling for result
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(1)
        
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        response = session.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        data = response.json()
        return data['results']['transcripts'][0]['transcript']
    return "Transcription failed."

# --- 2. AI CORE: AMAZON BEDROCK (CLAUDE 3 HAIKU) ---
def get_agrisutra_advice(query, language):
    """Uses Bedrock for intent detection and Trust Engine rules."""
    system_prompt = f"""You are AgriSutra, a pro-farmer AI. Language: {language}.
    Rules: 1. Block unsafe pesticides. 2. Provide weather-based action (Sentry logic).
    3. Use simple rural analogies."""
    
    model_id = "anthropic.claude-3-haiku-20240307-v1:0" # Fast and affordable
    
    messages = [{"role": "user", "content": [{"text": query}]}]
    
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        system=[{"text": system_prompt}],
        inferenceConfig={"maxTokens": 500, "temperature": 0.4}
    )
    return response['output']['message']['content'][0]['text']

# --- 3. TEXT-TO-SPEECH: AMAZON POLLY ---
def speak_vernacular(text, voice_id):
    """Generates lifelike speech using Amazon Polly."""
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural' # Best quality for Indian languages
    )
    return response['AudioStream'].read()

# --- STREAMLIT UI ---
st.title("🌾 AgriSutra (Full AWS)")

# Voice Mapping for Polly
languages = {
    "Hindi (हिंदी)": {"code": "hi-IN", "voice": "Aditi"},
    "Kannada (ಕನ್ನಡ)": {"code": "kn-IN", "voice": "N/A"}, # Note: Polly uses standard voices for some
    "Tamil (தமிழ்)": {"code": "ta-IN", "voice": "N/A"},
    "English": {"code": "en-IN", "voice": "Kajal"}
}

selected_lang = st.selectbox("Language / भाषा", list(languages.keys()))
lang_data = languages[selected_lang]

# Input Section
audio_input = st.audio_input("Speak to AgriSutra")

if audio_input:
    with st.spinner("🤖 Processing with AWS..."):
        # STT
        text_query = transcribe_voice(audio_input.getvalue(), lang_data["code"])
        st.write(f"**You said:** {text_query}")
        
        # Bedrock Logic
        advice = get_agrisutra_advice(text_query, selected_lang)
        st.success(f"**AgriSutra:** {advice}")
        
        # TTS
        if lang_data["voice"] != "N/A":
            audio_out = speak_vernacular(advice, lang_data["voice"])
            st.audio(audio_out, format="audio/mp3")

# Dashboard
st.divider()
st.error("🌧️ **Sentry Agent:** Rain expected in 3 hours. Drain your fields.")
