# 🚀 How to Run AgriSutra

## Quick Start (3 Commands)

```bash
# 1. Install dependencies (if not already done)
pip install -r requirements.txt

# 2. Run the app
python -m streamlit run app.py

# 3. Open your browser to http://localhost:8502
```

That's it! Your AgriSutra is now running with real AI responses.

## What You'll See

When the app starts, you should see:

```
✅ Groq LLM connected! Full AI responses enabled.
```

This confirms that the Groq API is working correctly.

## Using the App

### 1. Select Language
Choose from:
- Hindi (हिंदी)
- Kannada (ಕನ್ನಡ)
- Tamil (தமிழ்)
- English

### 2. Type Your Question
Examples:
- "What is the weather in Bangalore?"
- "How to prepare soil for organic farming?"
- "What is the budget for wheat farming?"
- "धान की खेती कैसे करें?"

### 3. Get AI Response
- Response appears in 1-2 seconds
- Real AI-generated advice
- Context-aware and safe

## Testing the Connection

Before running the full app, you can test the Groq connection:

```bash
python test_groq_connection.py
```

This will:
- Test English query
- Test Hindi query
- Verify API is working

Expected output:
```
🔧 Initializing Groq client...
✅ Client initialized successfully

📝 Testing English query...
✅ English response received:
   Crop rotation is a farming practice...

📝 Testing Hindi query...
✅ Hindi response received:
   फसल चक्र एक कृषि पद्धति है...

🎉 All tests passed! Groq integration is working correctly.
✅ Your AgriSutra is ready to use!
```

## Troubleshooting

### Port Already in Use

If you see "Address already in use", try a different port:

```bash
python -m streamlit run app.py --server.port 8503
```

### Import Errors

If you see import errors, reinstall dependencies:

```bash
pip install -r requirements.txt --force-reinstall
```

### API Errors

If you see "Groq API error", check:
1. Internet connection
2. API key is correct
3. Groq service is up (https://status.groq.com)

### Slow Responses

If responses are slow:
1. Check internet speed
2. Try again (first request may be slower)
3. Groq usually responds in < 2 seconds

## Running Tests

Verify everything works:

```bash
# Run all tests
pytest tests/unit/ -v

# Should see: 117 passed
```

## Stopping the App

Press `Ctrl+C` in the terminal to stop the Streamlit server.

## Next Steps

1. **Try different questions** in multiple languages
2. **Test weather queries** with different cities
3. **Test finance queries** with different crops
4. **Verify safety** by trying unsafe queries (should be blocked)

## Example Session

```bash
$ python -m streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8502
  Network URL: http://192.168.1.100:8502

✅ Groq LLM connected! Full AI responses enabled.
```

Then in the browser:
1. Select "Hindi (हिंदी)"
2. Type: "धान की खेती कैसे करें?"
3. Click "Submit / जमा करें"
4. Get real AI response in Hindi!

## Performance

- **Response Time**: 1-2 seconds
- **Languages**: 4 supported
- **Queries**: Unlimited (subject to Groq rate limits)
- **Accuracy**: High (Llama 3.3 70B model)

## Features Working

- ✅ Real AI responses (not mock)
- ✅ Multilingual support
- ✅ Weather context
- ✅ Finance context
- ✅ Safety governance
- ✅ Technical translation
- ✅ Fast responses

## Support

If you encounter issues:
1. Check GROQ_SETUP.md
2. Run test_groq_connection.py
3. Check error messages in terminal
4. Verify API key is correct

---

**Ready to go!** Just run:
```bash
python -m streamlit run app.py
```

Happy farming! 🌾🤖
