# Voice Input Guide - Groq Whisper

## Quick Start

1. **Run the app**:
   ```bash
   streamlit run app.py
   ```

2. **Select your language** from the dropdown

3. **Choose "🎤 Voice Recording"** mode

4. **Click the microphone button** and speak your question

5. **Click Submit** - Whisper will transcribe instantly!

## Supported Languages

| Language | Code | Example Question |
|----------|------|------------------|
| Hindi | hi | "बैंगलोर में मौसम कैसा है?" |
| Kannada | kn | "ಬೆಂಗಳೂರಿನಲ್ಲಿ ಹವಾಮಾನ ಹೇಗಿದೆ?" |
| Tamil | ta | "பெங்களூரில் வானிலை எப்படி இருக்கிறது?" |
| English | en | "What is the weather in Bangalore?" |

## Tips for Best Results

✅ **Speak clearly** - Enunciate your words
✅ **Reduce background noise** - Find a quiet place
✅ **Keep it short** - 5-15 seconds is ideal
✅ **Select correct language** - Helps Whisper understand better
✅ **Use natural speech** - No need to speak slowly

## What You Can Ask

### Weather Queries
- "What's the weather today?"
- "Will it rain tomorrow?"
- "Temperature in my area?"

### Crop Finance
- "How much does rice farming cost?"
- "What's the ROI for wheat?"
- "Profit from sugarcane?"

### Farming Tips
- "When to plant tomatoes?"
- "Best fertilizer for cotton?"
- "How to prevent pests?"

## How It Works

```
Your Voice → Microphone → Audio Bytes → Groq Whisper → Text → LLM → Response
```

1. **Record**: Browser captures your voice
2. **Upload**: Audio sent to Groq Whisper API
3. **Transcribe**: Whisper converts speech to text (< 1 second)
4. **Process**: LLM generates response
5. **Respond**: Text and audio response returned

## Troubleshooting

### No audio recorded
- Check browser microphone permissions
- Try clicking the microphone button again
- Ensure your microphone is working

### Transcription failed
- Check internet connection
- Verify Groq API key is valid
- Try recording again with clearer audio

### Wrong language detected
- Select the correct language before recording
- Speak more clearly
- Try text input as fallback

## Technical Specs

- **Model**: whisper-large-v3-turbo
- **Speed**: < 1 second for typical queries
- **Accuracy**: 95%+ for clear audio
- **Max duration**: 30 seconds recommended
- **Formats**: WAV, MP3, M4A, FLAC, OGG

## Privacy & Security

- Audio is sent to Groq's secure API
- No audio is stored permanently
- Transcription happens in real-time
- Data is encrypted in transit

## Comparison: Text vs Voice

| Feature | Text Input | Voice Input |
|---------|-----------|-------------|
| Speed | Fast | Very Fast |
| Accuracy | 100% | 95%+ |
| Convenience | Typing required | Hands-free |
| Best for | Complex queries | Quick questions |
| Accessibility | Requires literacy | No literacy needed |

## Example Session

1. Open app → Select "Hindi"
2. Click "Voice Recording"
3. Speak: "बैंगलोर में मौसम कैसा है?"
4. Click Submit
5. See transcription: "बैंगलोर में मौसम कैसा है?"
6. Get response with weather info
7. Listen to audio response

## Advanced Features

### Language Auto-Detection
Whisper can detect language automatically, but selecting it manually improves accuracy.

### Multi-Language Support
You can speak in one language and get responses in another by changing the language selector.

### Noise Handling
Whisper is trained to handle background noise, but clearer audio = better results.

## Need Help?

- Check `WHISPER_SETUP.md` for technical details
- Run `python test_whisper.py` to test setup
- See `README.md` for general setup instructions
