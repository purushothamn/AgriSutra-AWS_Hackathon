# AgriSutra: Voice-First Farm Intelligence System

AgriSutra is a vernacular, voice-first farm intelligence system designed for rural farmers in India. This MVP enables farmers to interact with AI-powered agricultural guidance in their native languages (Hindi, Kannada, Tamil, English) through an easy-to-use interface.

## Features

- **Real AI Responses**: Powered by Groq's Llama 3.3 70B LLM
- **Voice Input**: Real microphone input with Groq Whisper speech-to-text
- **Multilingual Support**: Hindi, Kannada, Tamil, and English
- **Specialized Agents**: 
  - Sentry Agent for weather alerts and disaster management
  - Economist Agent for crop budgeting and ROI calculations
- **Safety Governance**: Resilience Sentry validates queries and responses to prevent harmful advice
- **Technical Term Translation**: Context Translator provides local language translations with visual and audio aids
- **Fast & Reliable**: Sub-2-second response times with Groq

## Architecture

The system consists of six core components:
1. **Voice Pipeline**: Real speech-to-text using Groq Whisper
2. **Multi-Agent Router**: Intent classification and routing
3. **Specialized Agents**: Sentry (weather) and Economist (finance)
4. **Resilience Sentry**: Safety governance layer
5. **Context Translator**: Technical term translation
6. **Groq LLM Client**: Real AI-powered responses

## Prerequisites

- Python 3.8 or higher
- Internet connection
- Groq API key (already configured!)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agrisutra-farm-intelligence
```

### 2. Set Up Virtual Environment

**On Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

**Manual Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your default browser at `http://localhost:8502`

You should see: ✅ **Groq LLM connected! Full AI responses enabled.**

### 4. Start Using AgriSutra!

1. Select your language (Hindi, Kannada, Tamil, English)
2. Type any farming question
3. Get real AI-powered responses instantly!

**Example questions:**
- "What is the weather in Bangalore?"
- "How to prepare soil for organic farming?"
- "What is the budget for wheat farming?"
- "When should I plant rice?"

## Project Structure

```
agrisutra-farm-intelligence/
├── agrisutra/
│   ├── __init__.py
│   ├── config.py              # Configuration and AWS settings
│   ├── voice_pipeline/        # AWS Transcribe and Polly integration
│   ├── agents/                # Sentry and Economist agents
│   ├── safety/                # Resilience Sentry (safety governance)
│   ├── translation/           # Context Translator
│   ├── voice_pipeline/        # Voice processing (mock for MVP)
│   ├── groq_client.py         # Groq LLM integration
│   ├── orchestrator.py        # Main request coordinator
│   └── config.py              # System configuration
├── tests/
│   ├── unit/                  # Unit tests (95 tests, all passing)
│   ├── properties/            # Property-based tests
│   └── integration/           # Integration tests
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── setup.sh                   # Linux/Mac setup script
├── setup.bat                  # Windows setup script
├── GROQ_SETUP.md             # Groq API setup guide
└── README.md                 # This file
```

## Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/ -v

# Run with coverage
pytest --cov=agrisutra --cov-report=html
```

All 95 unit tests pass successfully!

## Configuration

All configuration is managed in `agrisutra/config.py`. Key settings include:

- **LLM Model**: Groq Llama 3.3 70B (production model)
- **Response Length**: Max 800 tokens for detailed responses
- **Supported Languages**: Hindi (hi), Kannada (kn), Tamil (ta), English (en)
- **Performance**: Sub-2-second response times

## Usage

1. **Select Language**: Choose Hindi, Kannada, Tamil, or English
2. **Input Query**: Type your farming question
3. **Receive Response**: Get real AI-powered advice in your language
   - Audio playback
   - Visual aids for technical terms

### Example Queries

**Weather (Hindi)**: "आज का मौसम कैसा है?" (What's the weather today?)

**Finance (Kannada)**: "ಗೋಧಿ ಬೆಳೆಯ ROI ಎಷ್ಟು?" (What's the ROI for wheat crop?)

**General (Tamil)**: "நெல் பயிருக்கு எப்போது நீர் பாய்ச்ச வேண்டும்?" (When should I water rice crop?)

## Safety Features

The Resilience Sentry blocks queries and responses containing:
- Chemical mixing instructions
- Unsafe agricultural practices
- Harmful advice

Blocked queries receive a localized safety message in the user's language.

## Development

### Adding New Features

1. Create feature branch
2. Implement changes in appropriate module
3. Add unit tests and property tests
4. Update documentation
5. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions and classes
- Keep functions focused and concise

## Troubleshooting

### AWS Credentials Error
- Verify `.env` file has correct credentials
- Check AWS IAM permissions for Bedrock, Transcribe, Polly
- Ensure AWS region is correct

### Audio Input Not Working
- Check browser permissions for microphone access
- Verify audio format is WAV, 16kHz sample rate
- Fall back to text input if audio fails

### Slow Response Times
- Check network connectivity
- Verify AWS service availability
- Enable caching for frequently accessed data

## License

This project is developed for the AWS Hackathon. See LICENSE file for details.

## Team

Team WhyKaliber - Building voice-first AI solutions for rural India

## Acknowledgments

- AWS for Bedrock, Transcribe, and Polly services
- Streamlit for the UI framework
- Hypothesis for property-based testing
