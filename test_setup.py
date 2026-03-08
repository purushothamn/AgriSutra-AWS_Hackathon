"""
Test AgriSutra Setup
Verify all components are working
"""

print("=" * 60)
print("🧪 Testing AgriSutra Setup")
print("=" * 60)
print()

# Test 1: Import modules
print("1️⃣ Testing imports...")
try:
    from agrisutra.orchestrator import LambdaOrchestrator
    from agrisutra.aws_speech_recognition import AWSSpeechRecognition
    from agrisutra.groq_client import GroqClient
    print("   ✅ All modules imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

print()

# Test 2: AWS Credentials
print("2️⃣ Testing AWS credentials...")
try:
    import boto3
    
    aws_access_key_id = "AKIA44QOQ7WEC6YRG3UX"
    aws_secret_access_key = "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"
    
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='ap-south-1'
    )
    
    sts = session.client('sts')
    identity = sts.get_caller_identity()
    print(f"   ✅ AWS credentials valid")
    print(f"   📋 Account: {identity['Account']}")
    print(f"   👤 User: {identity['Arn'].split('/')[-1]}")
except Exception as e:
    print(f"   ❌ AWS credentials failed: {e}")

print()

# Test 3: S3 Bucket Access
print("3️⃣ Testing S3 bucket access...")
try:
    s3 = session.client('s3')
    bucket_name = "agrisutra-general"
    
    s3.head_bucket(Bucket=bucket_name)
    print(f"   ✅ S3 bucket '{bucket_name}' accessible")
except Exception as e:
    print(f"   ❌ S3 bucket access failed: {e}")

print()

# Test 4: Transcribe Access
print("4️⃣ Testing AWS Transcribe access...")
try:
    transcribe = session.client('transcribe')
    transcribe.list_transcription_jobs(MaxResults=1)
    print(f"   ✅ AWS Transcribe accessible")
except Exception as e:
    print(f"   ❌ Transcribe access failed: {e}")

print()

# Test 5: Groq API
print("5️⃣ Testing Groq API...")
try:
    groq_api_key = "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"
    groq_client = GroqClient(api_key=groq_api_key)
    
    # Test with a simple query
    response = groq_client.generate_response("Hello", "en")
    if response:
        print(f"   ✅ Groq API working")
        print(f"   📝 Response: {response[:50]}...")
    else:
        print(f"   ⚠️  Groq API returned no response")
except Exception as e:
    print(f"   ❌ Groq API failed: {e}")

print()

# Test 6: Initialize Orchestrator
print("6️⃣ Testing Orchestrator initialization...")
try:
    orchestrator = LambdaOrchestrator(
        groq_api_key="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",
        aws_access_key_id="AKIA44QOQ7WEC6YRG3UX",
        aws_secret_access_key="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",
        aws_bucket_name="agrisutra-general"
    )
    print(f"   ✅ Orchestrator initialized successfully")
except Exception as e:
    print(f"   ❌ Orchestrator initialization failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("✅ Setup Test Complete!")
print("=" * 60)
print()
print("🚀 Ready to run: streamlit run app.py")
print()
