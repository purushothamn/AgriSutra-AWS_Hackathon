# AgriSutra - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8502`

You should see: ✅ **Groq LLM connected! Full AI responses enabled.**

### 3. Start Asking Questions!

1. Select your language (Hindi, Kannada, Tamil, English)
2. Type any farming question
3. Get real AI-powered responses instantly!

## 📝 Example Questions

### Weather Queries
```
What is the weather in Bangalore?
Delhi में मौसम कैसा है?
```

### Finance Queries
```
What is the budget for wheat farming?
धान की खेती का बजट क्या है?
```

### General Farming
```
How to prepare soil for organic farming?
जैविक खेती के लिए मिट्टी कैसे तैयार करें?
When should I plant rice?
कीट नियंत्रण कैसे करें?
```

### 🎤 Voice Input
You can also **speak** your questions:
1. Select "Voice (Microphone)" input mode
2. Click the microphone button
3. Speak your question in any supported language
4. Get AI responses based on your speech!

## ✅ What Works

- **Real AI Responses**: Powered by Groq's Llama 3.3 70B
- **Voice Input**: Real microphone input with speech-to-text
- **Fast**: Sub-2-second response times
- **Multilingual**: Hindi, Kannada, Tamil, English
- **Smart Context**: Weather and finance data enrichment
- **Safe**: Resilience Sentry blocks harmful advice
- **Tested**: 117 unit tests, all passing

## 🎯 Features

### Specialized Agents
- **Sentry Agent**: Weather alerts and disaster warnings
- **Economist Agent**: Crop budgeting and ROI calculations

### Safety Governance
- Blocks unsafe queries (chemical mixing, harmful practices)
- Validates all responses
- Localized safety messages

### Technical Translation
- 15+ agricultural terms
- Local language analogies
- Image and audio references

## 🔧 Configuration

The Groq API key is already configured in `app.py`. For production:

1. Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

2. Add to `.gitignore`:
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

## 📊 System Architecture

```
User Query
    ↓
Safety Check (Resilience Sentry)
    ↓
Intent Classification (Router)
    ↓
Context Gathering (Agents)
    ↓
LLM Generation (Groq)
    ↓
Safety Validation
    ↓
Translation (Technical Terms)
    ↓
Response
```

## 🧪 Run Tests

```bash
# All tests
pytest tests/unit/ -v

# With coverage
pytest --cov=agrisutra --cov-report=html
```

All 117 tests pass!

## 📚 Documentation

- **Setup Guide**: GROQ_SETUP.md
- **LLM Integration**: LLM_INTEGRATION.md
- **Installation**: INSTALLATION.md
- **Features**: FEATURES.md
- **Full README**: README.md

## 🎉 You're Ready!

Your AgriSutra is fully functional with real AI responses. Just run the app and start asking farming questions in any language!

```bash
python -m streamlit run app.py
```

Happy farming! 🌾🤖
