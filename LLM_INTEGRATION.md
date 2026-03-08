# LLM Integration Guide

## Overview

AgriSutra uses **Groq's Llama 3.3 70B** model for fast, high-quality AI responses.

## Current Setup

**Model**: `llama-3.3-70b-versatile`
**API Key**: Configured in `app.py`
**Client**: `agrisutra/groq_client.py`

## How It Works

### Request Flow
```
User Query → Safety Check → Intent Classification → Context Gathering → LLM Generation → Safety Validation → Translation → Response
```

### Context Enhancement
- Weather queries get real weather data added to prompt
- Finance queries get ROI calculations added to prompt
- General queries sent directly to LLM

## Performance
- Response time: < 2 seconds
- Multilingual support: Hindi, Kannada, Tamil, English

## Resources
- **Groq Console**: https://console.groq.com
- **Setup Guide**: See GROQ_SETUP.md

---

**Status**: ✅ Fully functional with real AI responses!
