"""
Test script to verify orchestrator initialization
"""

from agrisutra.orchestrator import LambdaOrchestrator

try:
    # Test with API key
    groq_api_key = "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"
    orchestrator = LambdaOrchestrator(groq_api_key=groq_api_key)
    print("✅ SUCCESS: Orchestrator initialized correctly with Groq API key!")
    print(f"✅ LLM Client: {type(orchestrator.llm_client).__name__}")
    print(f"✅ Speech Recognition: {type(orchestrator.speech_recognition).__name__}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
