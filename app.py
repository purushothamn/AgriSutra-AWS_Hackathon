import streamlit as st
import boto3
import json

# --- UI Setup ---
st.set_page_config(page_title="AgriSutra MVP", page_icon="🌾")
st.title("🌾 AgriSutra: The Urban Signal")
st.caption("Team WhyKaliber | Voice-First AI Farm Manager")
st.markdown("---")

# --- AWS Setup ---
# Streamlit Cloud securely pulls your AWS keys from its own settings
try:
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=st.secrets["AWS_REGION"],
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
    )
except Exception as e:
    st.error("AWS credentials missing. Waiting for Tech Lead to configure Streamlit Secrets...")
    st.stop()

# --- Core Logic ---
def governance_layer(user_input):
    """Resilience Sentry: Blocks unsafe advice."""
    banned_keywords = ["mix", "poison", "suicide", "explosive", "unapproved", "toxic", "dangerous"]
    if any(word in user_input.lower() for word in banned_keywords):
        return False, "⚠️ [GOVERNANCE BLOCK]: Unsafe agronomy practice detected. Please consult the local Panchayat."
    return True, "Safe"

def invoke_kiro(prompt):
    """Calls Claude 3 Haiku via AWS Bedrock."""
    is_safe, warning = governance_layer(prompt)
    if not is_safe:
        return warning, True

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": "You are a vernacular voice-first AI Farm Manager for AgriSutra. Provide short, practical, safe agronomy advice.",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps(payload)
        )
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text'], False
    except Exception as e:
        return f"System Error: {str(e)}", False

# --- App Interface ---
st.info("🎙️ *Audio module in development. Using text interface for this prototype.*")

query = st.text_input("Speak to the Farm Manager (e.g., 'When should I water my crops?'):")

if st.button("Submit Query"):
    if query.strip():
        with st.spinner("Processing..."):
            answer, is_blocked = invoke_kiro(query)
            
            if is_blocked:
                st.error(answer)
                st.caption("🔒 Resilience Sentry Intercepted this request.")
            else:
                st.success("✅ Governance Passed")
                st.write(f"**AI:** {answer}")
    else:
        st.warning("Please enter a query to test.")
