"""
AgriSutra Streamlit UI - Main Application

This is the main Streamlit application for AgriSutra, providing a voice-first,
vernacular farm intelligence interface for rural farmers.

Validates Requirements: 2.1, 2.2, 5.5, 6.1, 6.2, 6.3, 6.6
"""

import streamlit as st
import io
import base64
from PIL import Image
from agrisutra.orchestrator import LambdaOrchestrator


# Page configuration
st.set_page_config(
    page_title="AgriSutra - Farm Intelligence",
    page_icon="�",  # Microphone icon matching your logo
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, attractive UI
st.markdown("""
<style>
    :root{
color-scheme:light;}
html,body[class*="css"]{
color-scheme :light;
background:#e3f2fd;
}
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        max-width: 900px;
        padding: 2rem 1rem;
        font-family: 'Poppins', sans-serif;
        background: #E3F2FD;
        min-height: 100vh;
    }
    
    /* Fresh background pattern */
    body {
        background: #E3F2FD; 
        background-attachment: fixed;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 50%, #81C784 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.2);
        animation: fadeInDown 0.8s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Language Selector */
    .language-section {
        background: linear-gradient(135deg, #FF7043 0%, #FF8A65 50%, #FFAB91 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(255, 112, 67, 0.2);
        animation: slideInLeft 0.8s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Input Section */
    .input-section {
        background: linear-gradient(135deg, #42A5F5 0%, #64B5F6 50%, #90CAF9 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(66, 165, 245, 0.2);
        animation: slideInRight 0.8s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .input-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Voice Recording Animation */
    .recording-pulse {
        width: 80px;
        height: 80px;
        background: #FF5722;
        border-radius: 50%;
        margin: 1rem auto;
        animation: pulse 1.5s infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 87, 34, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(255, 87, 34, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 87, 34, 0); }
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #E91E63 0%, #F06292 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4);
    }
    
    /* Response Section */
    .response-section {
        background: linear-gradient(135deg, #AB47BC 0%, #BA68C8 50%, #CE93D8 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(171, 71, 188, 0.2);
        animation: fadeInUp 0.8s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .response-text {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        color: #333;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Sidebar Styles */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #673AB7 0%, #9C27B0 100%);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #26C6DA 0%, #4DD0E1 50%, #80DEEA 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(38, 198, 218, 0.2);
        animation: bounceIn 0.8s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Technical Terms */
    .tech-term {
        background: linear-gradient(135deg, #795548 0%, #A1887F 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        color: white;
        transition: transform 0.3s ease;
    }
    
    .tech-term:hover {
        transform: scale(1.02);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #4CAF50;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: slideInLeft 0.5s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #F44336 0%, #FF7043 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: shake 0.5s ease-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Audio Player Styling */
    .stAudio {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .main-subtitle { font-size: 1rem; }
        .input-section, .response-section { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)


def get_base64_logo():
    """Convert logo to base64 for embedding in HTML"""
    try:
        with open("assets/logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def initialize_session_state():
    """Initialize session state variables"""
    if 'orchestrator' not in st.session_state:
        try:
            # ==================== CONFIGURATION ====================
            # Groq API Key for LLM
            groq_api_key = "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"
            
            # AWS Credentials for Transcribe (Speech-to-Text) - REQUIRED
            # Your AWS credentials are already configured
            aws_access_key_id = "AKIA44QOQ7WEC6YRG3UX"
            aws_secret_access_key = "fLNEUzLFU5tnnyGNS/dHB4+v51rzpT4VMAtoNLkm"
            aws_bucket_name = "agrisutra-general"  # S3 bucket name
            # ======================================================
            
            # Try to get from Streamlit secrets if available
            try:
                if hasattr(st, 'secrets'):
                    if 'GROQ_API_KEY' in st.secrets:
                        groq_api_key = st.secrets['GROQ_API_KEY']
                    if 'AWS_ACCESS_KEY_ID' in st.secrets:
                        aws_access_key_id = st.secrets['AWS_ACCESS_KEY_ID']
                    if 'AWS_SECRET_ACCESS_KEY' in st.secrets:
                        aws_secret_access_key = st.secrets['AWS_SECRET_ACCESS_KEY']
                    if 'AWS_BUCKET_NAME' in st.secrets:
                        aws_bucket_name = st.secrets['AWS_BUCKET_NAME']
            except Exception:
                pass
            
            if not groq_api_key:
                st.error("❌ Groq API key not found. Please configure it.")
                st.stop()
            
            # Initialize orchestrator with AWS Transcribe only
            st.session_state.orchestrator = LambdaOrchestrator(
                groq_api_key=groq_api_key,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_bucket_name=aws_bucket_name
            )
            
            st.success("✅ Groq LLM + AWS Transcribe connected!")
            st.info("🎤 Voice input uses AWS Transcribe for Indian languages")
            
        except Exception as e:
            st.error(f"Failed to initialize orchestrator: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()
    
    if 'data_usage' not in st.session_state:
        st.session_state.data_usage = 0
    
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []


def display_header():
    """Display application header with modern design and logo"""
    logo_base64 = get_base64_logo()
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        if logo_base64:
            # Display with actual logo
            st.markdown(f"""
            <div class="main-header">
                <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem;">
                    <img src="data:image/png;base64,{logo_base64}" 
                         style="width: 100px; height: 100px; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">
                    <div>
                        <h1 class="main-title">AgriSutra</h1>
                        <p class="main-subtitle">Voice-First Farm Intelligence for Rural India</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback to emoji if logo not found
            st.markdown("""
            <div class="main-header">
                <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
                    <div style="font-size: 4rem;">🎤</div>
                    <div>
                        <h1 class="main-title">AgriSutra</h1>
                        <p class="main-subtitle">Voice-First Farm Intelligence for Rural India</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def display_language_selector():
    """Display language selector with attractive styling"""
    st.markdown('<div class="language-section">', unsafe_allow_html=True)
    
    languages = {
        "🇮🇳 Hindi (हिंदी)": "hi",
        "🇮🇳 Kannada (ಕನ್ನಡ)": "kn", 
        "🇮🇳 Tamil (தமிழ்)": "ta",
        "🇬🇧 English": "en"
    }
    
    selected_language = st.selectbox(
        "🌍 Select Language / भाषा चुनें / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ / மொழியைத் தேர்ந்தெடுக்கவும்",
        options=list(languages.keys()),
        index=0
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return languages[selected_language]


def display_input_section(language: str):
    """
    Display input section with modern UI and animations.
    
    Args:
        language: Selected language code
    
    Returns:
        Tuple of (input_type, input_data, location, crop, area)
    """
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="input-title">💬 Ask Your Question / अपना प्रश्न पूछें</h3>', unsafe_allow_html=True)
    
    # Input mode selector with emojis
    input_mode = st.radio(
        "Choose Input Mode:",
        options=["📝 Text Input", "🎤 Voice Recording"],
        horizontal=True
    )
    
    input_type = "text"
    input_data = ""
    
    if input_mode == "📝 Text Input":
        # Text input with placeholder
        query_text = st.text_area(
            "✍️ Type your question here:",
            height=120,
            placeholder="Example: What is the weather in Bangalore? / बैंगलोर में मौसम कैसा है?",
            help="Ask about weather, crop prices, farming tips, or any agricultural query"
        )
        input_type = "text"
        input_data = query_text
        
    else:
        # Voice input with animation
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <div class="recording-pulse">🎤</div>
            <p style="color: white; font-weight: 500;">Click the microphone button below to record</p>
        </div>
        """, unsafe_allow_html=True)
        
        audio_bytes = st.audio_input("🎙️ Record your question")
        
        if audio_bytes:
            st.markdown('<div class="success-message">✅ Audio recorded successfully! Ready to process...</div>', unsafe_allow_html=True)
            input_type = "audio"
            
            # Get raw bytes from the uploaded file
            input_data = audio_bytes.getvalue()
            
            # Show audio player for playback
            st.audio(audio_bytes, format="audio/wav")
            
            # Show audio info with nice formatting
            audio_size = len(input_data)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Size", f"{audio_size:,} bytes")
            with col2:
                st.metric("💾 Size (KB)", f"{audio_size/1024:.1f} KB")
            with col3:
                duration_est = audio_size / 16000  # Rough estimate
                st.metric("⏱️ Duration", f"~{duration_est:.1f}s")
            
            if audio_size < 1024:
                st.markdown('<div class="error-message">⚠️ Audio seems very short. Please record a longer message for better results.</div>', unsafe_allow_html=True)
        else:
            st.info("🎯 No audio recorded yet. Click the microphone button above to start recording.")
            input_type = "text"
            input_data = ""
    
    # Advanced options with collapsible section
    with st.expander("⚙️ Advanced Options (Optional)", expanded=False):
        st.markdown("### 🎯 Query Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input(
                "📍 Location",
                value="bangalore",
                help="Specify location for weather queries",
                placeholder="e.g., Mumbai, Delhi, Chennai"
            )
            
            crop = st.text_input(
                "🌾 Crop Type",
                value="rice",
                help="Specify crop for finance and farming queries",
                placeholder="e.g., wheat, cotton, sugarcane"
            )
        
        with col2:
            area = st.number_input(
                "📏 Farm Area (acres)",
                min_value=0.1,
                max_value=1000.0,
                value=1.0,
                step=0.5,
                help="Farm area for financial calculations"
            )
            
            # Add query type selector
            query_type = st.selectbox(
                "🎯 Query Type",
                ["Auto-detect", "Weather", "Crop Finance", "Farming Tips", "Market Prices"],
                help="Help us understand your query better"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return input_type, input_data, location, crop, area


def display_response(response, language: str):
    """
    Display the response with modern styling and animations.
    
    Args:
        response: OrchestratorResponse object
        language: Language code
    
    Validates Requirements: 5.5
    """
    st.markdown('<div class="response-section">', unsafe_allow_html=True)
    
    if not response.success:
        st.markdown(f'<div class="error-message">❌ {response.text_response}</div>', unsafe_allow_html=True)
        if response.error_message:
            with st.expander("🔍 Error Details"):
                st.code(response.error_message)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Display success response
    st.markdown('<h3 style="color: white; text-align: center; margin-bottom: 1rem;">🎉 Response Ready!</h3>', unsafe_allow_html=True)
    
    # Display text response with nice formatting
    st.markdown(f'<div class="response-text">{response.text_response}</div>', unsafe_allow_html=True)
    
    # Display audio player if available
    if response.audio_response:
        st.markdown('<h4 style="color: white;">🔊 Listen to Response:</h4>', unsafe_allow_html=True)
        st.audio(response.audio_response, format="audio/mp3")
    
    # Display technical terms with enhanced styling
    if response.technical_terms:
        st.markdown('<h4 style="color: white; margin-top: 2rem;">📚 Technical Terms / तकनीकी शब्द</h4>', unsafe_allow_html=True)
        
        for i, term in enumerate(response.technical_terms):
            with st.expander(f"🔍 {term.original} → {term.translation}", expanded=i==0):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("### 🖼️ Visual Reference")
                    st.info(f"Image: {term.original}")
                    st.caption(f"📎 URL: {term.image_url}")
                
                with col2:
                    st.markdown("### 🌐 Translation & Context")
                    st.success(f"**{term.translation}**")
                    st.write(term.local_analogy)
                    
                    st.markdown("### 🗣️ Pronunciation Guide")
                    st.info(f"Audio: {term.translation}")
                    st.caption(f"🎵 URL: {term.audio_url}")
    
    # Display processing metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Processing Time", f"{response.processing_time_ms}ms")
    with col2:
        st.metric("🎯 Status", "Success" if response.success else "Failed")
    with col3:
        st.metric("📝 Terms Found", len(response.technical_terms))
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_data_usage():
    """
    Display data usage metrics with attractive styling.
    
    Validates Requirements: 6.6
    """
    with st.sidebar:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Data Usage Monitor</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Mock data usage for MVP
        data_usage_kb = st.session_state.data_usage / 1024
        
        # Create attractive metrics
        st.metric(
            label="💾 Data Consumed",
            value=f"{data_usage_kb:.2f} KB",
            delta=f"+{data_usage_kb*0.1:.2f} KB this session"
        )
        
        # Progress bar for data usage
        progress_percentage = min(data_usage_kb / 100, 1.0)  # Assume 100KB limit
        st.progress(progress_percentage)
        
        if progress_percentage > 0.8:
            st.warning("⚠️ High data usage!")
        elif progress_percentage > 0.5:
            st.info("📈 Moderate usage")
        else:
            st.success("✅ Low usage")
        
        # Data usage tips with emojis
        with st.expander("💡 Data Saving Tips"):
            st.markdown("""
            - 📝 Use text input when possible
            - 🖼️ Skip images if not needed  
            - 🧹 Clear cache regularly
            - 🎤 Keep voice messages short
            - 📱 Use WiFi when available
            """)


def display_query_history():
    """Display recent query history with modern styling"""
    if st.session_state.query_history:
        with st.sidebar:
            st.markdown("""
            <div class="metric-card">
                <h3>📝 Recent Queries</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for i, query in enumerate(reversed(st.session_state.query_history[-5:])):
                # Handle both text and voice queries
                if isinstance(query, str):
                    if query.startswith("[Voice]"):
                        # Voice query - show with microphone icon
                        st.markdown(f"""
                        <div class="tech-term">
                            🎤 {i+1}. {query[7:].strip()[:40]}...
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Text query - show normally
                        st.markdown(f"""
                        <div class="tech-term">
                            💬 {i+1}. {query[:40]}...
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Fallback for any other type
                    st.markdown(f"""
                    <div class="tech-term">
                        ❓ {i+1}. {str(query)[:40]}...
                    </div>
                    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display language selector
    language = display_language_selector()
    
    # Display input section
    input_type, input_data, location, crop, area = display_input_section(language)
    
    # Submit button with enhanced styling
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submit_button = st.button(
            "🚀 Submit / जमा करें / ಸಲ್ಲಿಸಿ / சமர்ப்பிக்கவும்", 
            type="primary",
            use_container_width=True
        )
    
    if submit_button:
        if not input_data:
            st.markdown('<div class="error-message">⚠️ Please enter a question first!</div>', unsafe_allow_html=True)
        else:
            # Show loading animation with spinner
            with st.spinner("🔄 Processing your query... / प्रसंस्करण हो रहा है..."):
                try:
                    # Prepare event
                    event = {
                        "input_type": input_type,
                        "input_data": input_data,
                        "language": language,
                        "location": location,
                        "crop": crop,
                        "area": area
                    }
                    
                    # Process request
                    response = st.session_state.orchestrator.handle_request(event)
                    
                    # Update data usage (mock calculation)
                    if isinstance(input_data, bytes):
                        # Voice input - input_data is already bytes
                        st.session_state.data_usage += len(input_data)
                        # Add transcribed text to history if available
                        if response.success and hasattr(response, 'text_response'):
                            st.session_state.query_history.append(f"[Voice] {response.text_response[:50]}...")
                    else:
                        # Text input - input_data is string
                        st.session_state.data_usage += len(input_data.encode('utf-8'))
                        # Add original query to history
                        st.session_state.query_history.append(input_data)
                    
                    if response.audio_response:
                        st.session_state.data_usage += len(response.audio_response)
                
                except Exception as e:
                    st.markdown(f'<div class="error-message">❌ An error occurred: {str(e)}</div>', unsafe_allow_html=True)
                    with st.expander("🔍 Error Details"):
                        import traceback
                        st.code(traceback.format_exc())
                    response = None
            
            # Display response after loading is complete
            if response:
                display_response(response, language)
    
    # Display sidebar metrics
    display_data_usage()
    display_query_history()
    
    # Footer with modern styling
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #37474F 0%, #546E7A 100%); border-radius: 15px; margin-top: 2rem;">
        <h4 style="color: white; margin: 0;">🌾 AgriSutra - Empowering Rural Farmers with AI</h4>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">AWS Hackathon MVP | Made with ❤️ for Indian Farmers</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
