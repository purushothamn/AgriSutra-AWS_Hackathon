# Whisper Speech Recognition Setup

## Overview

AgriSutra now uses **Groq Whisper** for speech-to-text transcription. This provides:

- ✅ Fast transcription (faster than AWS Transcribe)
- ✅ High accuracy for Indian languages (Hindi, Kannada, Tamil, English)
- ✅ No AWS setup required
- ✅ Lower latency
- ✅ Cost-effective

## How It Works

1. User records audio in the Streamlit app
2. Audio bytes are sent to Groq Whisper API
3. Whisper transcribes the audio to text
4. Text is processed by the LLM pipeline

## Supported Languages

- 🇮🇳 Hindi (hi)
- 🇮🇳 Kannada (kn)
- 🇮🇳 Tamil (ta)
- 🇬🇧 English (en)

## Configuration

The Groq API key is used for both:
- LLM responses (Llama models)
- Speech recognition (Whisper)

No additional configuration needed!

## Model Used

- **Model**: `whisper-large-v3-turbo`
- **Provider**: Groq
- **Speed**: Very fast (optimized inference)
- **Accuracy**: High for Indian languages

## Code Location

- Implementation: `agrisutra/speech_recognition.py`
- Integration: `agrisutra/orchestrator.py`
- UI: `app.py`

## Benefits Over AWS Transcribe

| Feature | Groq Whisper | AWS Transcribe |
|---------|--------------|----------------|
| Speed | Very Fast | Slower (async jobs) |
| Setup | Simple | Complex (S3, IAM) |
| Cost | Lower | Higher |
| Latency | Low | Higher |
| Languages | Excellent | Good |

## Testing

To test voice input:
1. Run the app: `streamlit run app.py`
2. Select your language
3. Choose "Voice Recording" mode
4. Click the microphone and speak
5. Submit to see transcription

## API Details

- Endpoint: `https://api.groq.com/openai/v1/audio/transcriptions`
- Format: Multipart form data
- Response: Plain text transcription
- Timeout: 30 seconds
