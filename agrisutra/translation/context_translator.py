"""
Context Translator Module

Translates technical agricultural terms to local languages (Hindi, Kannada, Tamil)
with visual and audio aids for better farmer comprehension.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TechnicalTerm:
    """Represents a translated technical term with multimedia aids."""
    original: str
    translation: str
    local_analogy: str
    image_url: str
    audio_url: str


@dataclass
class TranslatedResponse:
    """Response containing original text, translated text, and technical terms."""
    original_text: str
    translated_text: str
    technical_terms: List[TechnicalTerm]


class ContextTranslator:
    """
    Translates technical agricultural terms to local languages with visual and audio aids.
    
    For MVP, uses mock S3 URLs since actual assets will be created later.
    """
    
    # Translation dictionary mapping English terms to local language equivalents
    TRANSLATION_DICT = {
        "drip irrigation": {
            "hi": {
                "translation": "बूंद-बूंद सिंचाई",
                "analogy": "पानी की बूंदों से सिंचाई करने की विधि"
            },
            "kn": {
                "translation": "ಹನಿ ನೀರಾವರಿ",
                "analogy": "ನೀರಿನ ಹನಿಗಳಿಂದ ನೀರಾವರಿ ಮಾಡುವ ವಿಧಾನ"
            },
            "ta": {
                "translation": "சொட்டு நீர்ப்பாசனம்",
                "analogy": "நீர் துளிகள் மூலம் பாசனம் செய்யும் முறை"
            }
        },
        "npk fertilizer": {
            "hi": {
                "translation": "एनपीके खाद",
                "analogy": "नाइट्रोजन, फास्फोरस और पोटाशियम युक्त खाद"
            },
            "kn": {
                "translation": "ಎನ್‌ಪಿಕೆ ಗೊಬ್ಬರ",
                "analogy": "ಸಾರಜನಕ, ರಂಜಕ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಮ್ ಹೊಂದಿರುವ ಗೊಬ್ಬರ"
            },
            "ta": {
                "translation": "என்பிகே உரம்",
                "analogy": "நைட்ரஜன், பாஸ்பரஸ் மற்றும் பொட்டாசியம் கொண்ட உரம்"
            }
        },
        "pesticide": {
            "hi": {
                "translation": "कीटनाशक",
                "analogy": "कीड़ों को मारने की दवा"
            },
            "kn": {
                "translation": "ಕೀಟನಾಶಕ",
                "analogy": "ಕೀಟಗಳನ್ನು ಕೊಲ್ಲುವ ಔಷಧ"
            },
            "ta": {
                "translation": "பூச்சிக்கொல்லி",
                "analogy": "பூச்சிகளை கொல்லும் மருந்து"
            }
        },
        "sprinkler": {
            "hi": {
                "translation": "फव्वारा सिंचाई",
                "analogy": "बारिश की तरह पानी छिड़कने की मशीन"
            },
            "kn": {
                "translation": "ಚಿಮುಕಿಸುವ ಯಂತ್ರ",
                "analogy": "ಮಳೆಯಂತೆ ನೀರು ಚಿಮುಕಿಸುವ ಯಂತ್ರ"
            },
            "ta": {
                "translation": "தெளிப்பான்",
                "analogy": "மழை போல் நீர் தெளிக்கும் கருவி"
            }
        },
        "mulching": {
            "hi": {
                "translation": "मल्चिंग",
                "analogy": "मिट्टी को ढकने की विधि"
            },
            "kn": {
                "translation": "ಮಲ್ಚಿಂಗ್",
                "analogy": "ಮಣ್ಣನ್ನು ಮುಚ್ಚುವ ವಿಧಾನ"
            },
            "ta": {
                "translation": "மண் மூடுதல்",
                "analogy": "மண்ணை மூடும் முறை"
            }
        },
        "vermicompost": {
            "hi": {
                "translation": "केंचुआ खाद",
                "analogy": "केंचुओं से बनी जैविक खाद"
            },
            "kn": {
                "translation": "ಎರೆಹುಳು ಗೊಬ್ಬರ",
                "analogy": "ಎರೆಹುಳುಗಳಿಂದ ತಯಾರಿಸಿದ ಸಾವಯವ ಗೊಬ್ಬರ"
            },
            "ta": {
                "translation": "மண்புழு உரம்",
                "analogy": "மண்புழுக்களால் தயாரிக்கப்பட்ட இயற்கை உரம்"
            }
        },
        "greenhouse": {
            "hi": {
                "translation": "ग्रीनहाउस",
                "analogy": "कांच या प्लास्टिक से बना फसल उगाने का घर"
            },
            "kn": {
                "translation": "ಹಸಿರುಮನೆ",
                "analogy": "ಗಾಜು ಅಥವಾ ಪ್ಲಾಸ್ಟಿಕ್‌ನಿಂದ ಮಾಡಿದ ಬೆಳೆ ಬೆಳೆಯುವ ಮನೆ"
            },
            "ta": {
                "translation": "பசுமை இல்லம்",
                "analogy": "கண்ணாடி அல்லது பிளாஸ்டிக்கால் செய்யப்பட்ட பயிர் வளர்க்கும் வீடு"
            }
        },
        "tractor": {
            "hi": {
                "translation": "ट्रैक्टर",
                "analogy": "खेत जोतने की मशीन"
            },
            "kn": {
                "translation": "ಟ್ರಾಕ್ಟರ್",
                "analogy": "ಹೊಲ ಉಳುವ ಯಂತ್ರ"
            },
            "ta": {
                "translation": "டிராக்டர்",
                "analogy": "நிலம் உழும் இயந்திரம்"
            }
        },
        "seed drill": {
            "hi": {
                "translation": "बीज बोने की मशीन",
                "analogy": "बीज को सही दूरी पर बोने का यंत्र"
            },
            "kn": {
                "translation": "ಬೀಜ ಬಿತ್ತುವ ಯಂತ್ರ",
                "analogy": "ಬೀಜವನ್ನು ಸರಿಯಾದ ಅಂತರದಲ್ಲಿ ಬಿತ್ತುವ ಯಂತ್ರ"
            },
            "ta": {
                "translation": "விதை விதைக்கும் கருவி",
                "analogy": "விதைகளை சரியான இடைவெளியில் விதைக்கும் கருவி"
            }
        },
        "harvester": {
            "hi": {
                "translation": "कटाई मशीन",
                "analogy": "फसल काटने की मशीन"
            },
            "kn": {
                "translation": "ಕೊಯ್ಲು ಯಂತ್ರ",
                "analogy": "ಬೆಳೆ ಕೊಯ್ಯುವ ಯಂತ್ರ"
            },
            "ta": {
                "translation": "அறுவடை இயந்திரம்",
                "analogy": "பயிர் அறுவடை செய்யும் இயந்திரம்"
            }
        },
        "soil testing": {
            "hi": {
                "translation": "मिट्टी परीक्षण",
                "analogy": "मिट्टी की गुणवत्ता जांचने की प्रक्रिया"
            },
            "kn": {
                "translation": "ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ",
                "analogy": "ಮಣ್ಣಿನ ಗುಣಮಟ್ಟವನ್ನು ಪರೀಕ್ಷಿಸುವ ಪ್ರಕ್ರಿಯೆ"
            },
            "ta": {
                "translation": "மண் பரிசோதனை",
                "analogy": "மண்ணின் தரத்தை சோதிக்கும் செயல்முறை"
            }
        },
        "crop rotation": {
            "hi": {
                "translation": "फसल चक्र",
                "analogy": "अलग-अलग फसलें बारी-बारी से उगाना"
            },
            "kn": {
                "translation": "ಬೆಳೆ ಸರದಿ",
                "analogy": "ವಿವಿಧ ಬೆಳೆಗಳನ್ನು ಸರದಿಯಲ್ಲಿ ಬೆಳೆಯುವುದು"
            },
            "ta": {
                "translation": "பயிர் சுழற்சி",
                "analogy": "வெவ்வேறு பயிர்களை மாறி மாறி பயிரிடுதல்"
            }
        },
        "organic farming": {
            "hi": {
                "translation": "जैविक खेती",
                "analogy": "रासायनिक खाद के बिना खेती"
            },
            "kn": {
                "translation": "ಸಾವಯವ ಕೃಷಿ",
                "analogy": "ರಾಸಾಯನಿಕ ಗೊಬ್ಬರವಿಲ್ಲದೆ ಕೃಷಿ"
            },
            "ta": {
                "translation": "இயற்கை விவசாயம்",
                "analogy": "இரசாயன உரம் இல்லாமல் விவசாயம்"
            }
        },
        "irrigation pump": {
            "hi": {
                "translation": "सिंचाई पंप",
                "analogy": "पानी खींचने की मशीन"
            },
            "kn": {
                "translation": "ನೀರಾವರಿ ಪಂಪ್",
                "analogy": "ನೀರು ಎಳೆಯುವ ಯಂತ್ರ"
            },
            "ta": {
                "translation": "பாசன பம்ப்",
                "analogy": "நீர் இழுக்கும் இயந்திரம்"
            }
        },
        "fungicide": {
            "hi": {
                "translation": "फफूंदनाशक",
                "analogy": "फफूंद रोग को रोकने की दवा"
            },
            "kn": {
                "translation": "ಶಿಲೀಂಧ್ರನಾಶಕ",
                "analogy": "ಶಿಲೀಂಧ್ರ ರೋಗವನ್ನು ತಡೆಯುವ ಔಷಧ"
            },
            "ta": {
                "translation": "பூஞ்சைக்கொல்லி",
                "analogy": "பூஞ்சை நோயை தடுக்கும் மருந்து"
            }
        }
    }
    
    # Mock S3 bucket URL for demo purposes
    S3_BUCKET_URL = "https://agrisutra-assets.s3.ap-south-1.amazonaws.com"
    
    def __init__(self):
        """Initialize the Context Translator."""
        pass
    
    def translate_technical_terms(self, text: str, language: str) -> TranslatedResponse:
        """
        Translate technical terms in the text to the specified local language.
        
        Args:
            text: Original text containing technical terms
            language: Target language code ('hi', 'kn', 'ta')
        
        Returns:
            TranslatedResponse with original text, translated text, and technical terms
        """
        if language not in ['hi', 'kn', 'ta']:
            raise ValueError(f"Unsupported language: {language}. Must be 'hi', 'kn', or 'ta'")
        
        translated_text = text
        technical_terms = []
        
        # Search for technical terms in the text (case-insensitive)
        text_lower = text.lower()
        for term_key, translations in self.TRANSLATION_DICT.items():
            if term_key in text_lower:
                # Get translation for the specified language
                lang_data = translations.get(language, {})
                translation = lang_data.get("translation", term_key)
                analogy = lang_data.get("analogy", "")
                
                # Replace the term in the text
                # Find the original case version in the text
                start_idx = text_lower.find(term_key)
                if start_idx != -1:
                    original_term = text[start_idx:start_idx + len(term_key)]
                    translated_text = translated_text.replace(original_term, translation, 1)
                    
                    # Create TechnicalTerm object
                    tech_term = TechnicalTerm(
                        original=original_term,
                        translation=translation,
                        local_analogy=analogy,
                        image_url=self.get_term_image(term_key),
                        audio_url=self.get_term_audio(term_key, language)
                    )
                    technical_terms.append(tech_term)
        
        return TranslatedResponse(
            original_text=text,
            translated_text=translated_text,
            technical_terms=technical_terms
        )
    
    def get_term_image(self, term: str) -> str:
        """
        Get the S3 URL for the image representation of a technical term.
        
        Args:
            term: Technical term (English)
        
        Returns:
            Mock S3 URL for the term's image
        """
        # Normalize term for URL (replace spaces with underscores, lowercase)
        normalized_term = term.lower().replace(" ", "_")
        return f"{self.S3_BUCKET_URL}/translations/images/{normalized_term}.jpg"
    
    def get_term_audio(self, term: str, language: str) -> str:
        """
        Get the S3 URL for the audio pronunciation of a technical term.
        
        Args:
            term: Technical term (English)
            language: Language code ('hi', 'kn', 'ta')
        
        Returns:
            Mock S3 URL for the term's audio pronunciation
        """
        if language not in ['hi', 'kn', 'ta']:
            raise ValueError(f"Unsupported language: {language}. Must be 'hi', 'kn', or 'ta'")
        
        # Normalize term for URL (replace spaces with underscores, lowercase)
        normalized_term = term.lower().replace(" ", "_")
        return f"{self.S3_BUCKET_URL}/translations/audio/{normalized_term}_{language}.mp3"
