"""
Groq LLM Client - Real AI Integration

This module provides integration with Groq's fast LLM API.
"""

import requests
from typing import Optional
from agrisutra.config import get_system_prompt


class GroqClient:
    """
    Groq LLM API client for real AI responses.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Groq client
        
        Args:
            api_key: Groq API key (required)
        """
        if not api_key:
            raise ValueError("Groq API key is required")
        
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama-3.3-70b-versatile"  # Production model - fast and multilingual
    
    def generate_response(
        self,
        prompt: str,
        language: str,
        system_prompt: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a response using Groq LLM API.
        
        Args:
            prompt: User prompt/query
            language: Language code (hi, kn, ta, en)
            system_prompt: Optional custom system prompt
        
        Returns:
            Generated response text or None if failed
        """
        if not prompt:
            return None
        
        # Use default system prompt if not provided
        if system_prompt is None:
            system_prompt = get_system_prompt(language)
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content']
            else:
                print(f"Groq API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return None
