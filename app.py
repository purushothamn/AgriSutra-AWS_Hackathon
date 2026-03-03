"""
AgriSutra Streamlit UI - Main Application

This is the main Streamlit application for AgriSutra, providing a voice-first,
vernacular farm intelligence interface for rural farmers.

Validates Requirements: 2.1, 2.2, 5.5, 6.1, 6.2, 6.3, 6.6
"""

import streamlit as st
import io
from PIL import Image
from agrisutra.orchestrator import LambdaOrchestrator


# Page configuration
st.set_page_config(
    page_title="AgriSutra - Farm Intelligence",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for low-bandwidth optimization
st.markdown("""
<style>
    .main {
        max-width: 800px;
        padding: 1rem;
    }
    .stAudio {
        max-width: 100%;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'orchestrator' not in st.session_state:
        try:
            # Groq API key (hardcoded for quick setup)
            groq_api_key = "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"
            
            # Try to get from Streamlit secrets if available
            try:
                if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                    groq_api_key = st.secrets['GROQ_API_KEY']
            except Exception:
                pass
            
            if not groq_api_key:
                st.error("❌ Groq API key not found. Please configure it.")
                st.stop()
            
            st.session_state.orchestrator = LambdaOrchestrator(groq_api_key=groq_api_key)
            st.success("✅ Groq LLM connected! Full AI responses enabled.")
            
        except Exception as e:
            st.error(f"Failed to initialize orchestrator: {str(e)}")
            st.stop()
    
    if 'data_usage' not in st.session_state:
        st.session_state.data_usage = 0
    
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []


def display_header():
    """Display application header"""
    st.title("🌾 AgriSutra")
    st.caption("Voice-First Farm Intelligence for Rural India")


def display_language_selector():
    """Display language selector"""
    languages = {
        "Hindi (हिंदी)": "hi",
        "Kannada (ಕನ್ನಡ)": "kn",
        "Tamil (தமிழ்)": "ta",
        "English": "en"
    }
    
    selected_language = st.selectbox(
        "Select Language / भाषा चुनें / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ / மொழியைத் தேர்ந்தெடுக்கவும்",
        options=list(languages.keys()),
        index=0
    )
    
    return languages[selected_language]


def display_input_section(language: str):
    """
    Display input section with voice and text options.
    
    Args:
        language: Selected language code
    
    Returns:
        Tuple of (input_type, input_data, location, crop, area)
    """
    st.subheader("Ask Your Question / अपना प्रश्न पूछें")
    
    # Input mode selector
    input_mode = st.radio(
        "Input Mode",
        options=["Text", "Voice (Microphone)"],
        horizontal=True
    )
    
    input_type = "text"
    input_data = ""
    
    if input_mode == "Text":
        # Text input
        query_text = st.text_area(
            "Type your question here:",
            height=100,
            placeholder="Example: What is the weather in Bangalore? / बैंगलोर में मौसम कैसा है?"
        )
        input_type = "text"
        input_data = query_text
    else:
        # Voice input using microphone
        st.info("🎤 Click the microphone button below to record your question")
        
        audio_bytes = st.audio_input("Record your question")
        
        if audio_bytes:
            st.success("✅ Audio recorded! Processing...")
            input_type = "audio"
            input_data = audio_bytes.getvalue()
            
            # Show audio player for playback
            st.audio(audio_bytes, format="audio/wav")
            
            # Show audio info
            audio_size = len(input_data)
            st.caption(f"Audio size: {audio_size:,} bytes ({audio_size/1024:.1f} KB)")
            
            if audio_size < 1024:
                st.warning("⚠️ Audio seems very short. Please record a longer message.")
        else:
            st.warning("No audio recorded yet. Click the microphone to start recording.")
            input_type = "text"
            input_data = ""
            input_data = ""
    
    # Additional parameters
    with st.expander("Advanced Options (Optional)"):
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input(
                "Location",
                value="bangalore",
                help="For weather queries"
            )
            
            crop = st.text_input(
                "Crop",
                value="rice",
                help="For finance queries"
            )
        
        with col2:
            area = st.number_input(
                "Farm Area (acres)",
                min_value=0.1,
                max_value=1000.0,
                value=1.0,
                step=0.5,
                help="For finance queries"
            )
    
    return input_type, input_data, location, crop, area


def display_response(response, language: str):
    """
    Display the response with text, audio, and technical terms.
    
    Args:
        response: OrchestratorResponse object
        language: Language code
    
    Validates Requirements: 5.5
    """
    if not response.success:
        st.error(response.text_response)
        if response.error_message:
            with st.expander("Error Details"):
                st.text(response.error_message)
        return
    
    # Display text response
    st.success("Response:")
    st.write(response.text_response)
    
    # Display audio player if available
    if response.audio_response:
        st.audio(response.audio_response, format="audio/mp3")
    
    # Display technical terms with images and audio
    if response.technical_terms:
        st.subheader("Technical Terms / तकनीकी शब्द")
        
        for term in response.technical_terms:
            with st.expander(f"{term.original} → {term.translation}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Display placeholder image (in production, load from S3)
                    st.caption("Image:")
                    st.text(f"[Image: {term.original}]")
                    st.caption(f"URL: {term.image_url}")
                
                with col2:
                    st.caption("Translation:")
                    st.write(f"**{term.translation}**")
                    st.write(term.local_analogy)
                    
                    st.caption("Pronunciation:")
                    st.text(f"[Audio: {term.translation}]")
                    st.caption(f"URL: {term.audio_url}")
    
    # Display processing time
    st.caption(f"Processing time: {response.processing_time_ms}ms")


def display_data_usage():
    """
    Display data usage metrics.
    
    Validates Requirements: 6.6
    """
    with st.sidebar:
        st.subheader("Data Usage")
        
        # Mock data usage for MVP
        data_usage_kb = st.session_state.data_usage / 1024
        
        st.metric(
            label="Data Consumed",
            value=f"{data_usage_kb:.2f} KB"
        )
        
        # Data usage tips
        with st.expander("Tips to Save Data"):
            st.write("""
            - Use text input instead of voice when possible
            - Avoid loading images if not needed
            - Clear cache regularly
            """)


def display_query_history():
    """Display recent query history"""
    if st.session_state.query_history:
        with st.sidebar:
            st.subheader("Recent Queries")
            
            for i, query in enumerate(reversed(st.session_state.query_history[-5:])):
                # Handle both text and voice queries
                if isinstance(query, str):
                    if query.startswith("[Voice]"):
                        # Voice query - show with microphone icon
                        st.caption(f"🎤 {i+1}. {query[7:].strip()[:45]}...")
                    else:
                        # Text query - show normally
                        st.caption(f"💬 {i+1}. {query[:45]}...")
                else:
                    # Fallback for any other type
                    st.caption(f"{i+1}. {str(query)[:45]}...")


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
    
    # Submit button
    if st.button("Submit / जमा करें / ಸಲ್ಲಿಸಿ / சமர்ப்பிக்கவும்", type="primary"):
        if not input_data:
            st.warning("Please enter a question.")
        else:
            # Show loading spinner
            with st.spinner("Processing your query... / प्रसंस्करण हो रहा है..."):
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
                    
                    # Display response
                    display_response(response, language)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    with st.expander("Error Details"):
                        import traceback
                        st.code(traceback.format_exc())
    
    # Display sidebar metrics
    display_data_usage()
    display_query_history()
    
    # Footer
    st.markdown("---")
    st.caption("AgriSutra - Empowering Rural Farmers with AI | AWS Hackathon MVP")


if __name__ == "__main__":
    main()
