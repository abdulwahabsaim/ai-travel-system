import json
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.language_data = self._load_language_data()
        self.common_phrases = self._load_common_phrases()
        
    def _load_language_data(self) -> Dict[str, Any]:
        """Load language information and codes"""
        return {
            "languages": {
                "english": {"code": "en", "name": "English", "native": "English"},
                "spanish": {"code": "es", "name": "Spanish", "native": "Español"},
                "french": {"code": "fr", "name": "French", "native": "Français"},
                "german": {"code": "de", "name": "German", "native": "Deutsch"},
                "italian": {"code": "it", "name": "Italian", "native": "Italiano"},
                "portuguese": {"code": "pt", "name": "Portuguese", "native": "Português"},
                "russian": {"code": "ru", "name": "Russian", "native": "Русский"},
                "chinese": {"code": "zh", "name": "Chinese", "native": "中文"},
                "japanese": {"code": "ja", "name": "Japanese", "native": "日本語"},
                "korean": {"code": "ko", "name": "Korean", "native": "한국어"},
                "arabic": {"code": "ar", "name": "Arabic", "native": "العربية"},
                "hindi": {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
                "thai": {"code": "th", "name": "Thai", "native": "ไทย"},
                "vietnamese": {"code": "vi", "name": "Vietnamese", "native": "Tiếng Việt"},
                "turkish": {"code": "tr", "name": "Turkish", "native": "Türkçe"}
            },
            "destinations": {
                "France": "french",
                "Spain": "spanish",
                "Italy": "italian",
                "Germany": "german",
                "Japan": "japanese",
                "China": "chinese",
                "Thailand": "thai",
                "Vietnam": "vietnamese",
                "Turkey": "turkish",
                "Russia": "russian",
                "Brazil": "portuguese",
                "Mexico": "spanish",
                "Canada": ["english", "french"],
                "Switzerland": ["german", "french", "italian"]
            }
        }
    
    def _load_common_phrases(self) -> Dict[str, Dict[str, str]]:
        """Load common travel phrases in different languages"""
        return {
            "greetings": {
                "english": "Hello",
                "spanish": "Hola",
                "french": "Bonjour",
                "german": "Hallo",
                "italian": "Ciao",
                "japanese": "こんにちは",
                "chinese": "你好",
                "korean": "안녕하세요",
                "thai": "สวัสดี",
                "vietnamese": "Xin chào"
            },
            "thank_you": {
                "english": "Thank you",
                "spanish": "Gracias",
                "french": "Merci",
                "german": "Danke",
                "italian": "Grazie",
                "japanese": "ありがとう",
                "chinese": "谢谢",
                "korean": "감사합니다",
                "thai": "ขอบคุณ",
                "vietnamese": "Cảm ơn"
            },
            "please": {
                "english": "Please",
                "spanish": "Por favor",
                "french": "S'il vous plaît",
                "german": "Bitte",
                "italian": "Per favore",
                "japanese": "お願いします",
                "chinese": "请",
                "korean": "부탁합니다",
                "thai": "กรุณา",
                "vietnamese": "Xin vui lòng"
            },
            "excuse_me": {
                "english": "Excuse me",
                "spanish": "Disculpe",
                "french": "Excusez-moi",
                "german": "Entschuldigung",
                "italian": "Scusi",
                "japanese": "すみません",
                "chinese": "对不起",
                "korean": "실례합니다",
                "thai": "ขออภัย",
                "vietnamese": "Xin lỗi"
            },
            "where_is": {
                "english": "Where is",
                "spanish": "¿Dónde está",
                "french": "Où est",
                "german": "Wo ist",
                "italian": "Dove è",
                "japanese": "どこですか",
                "chinese": "在哪里",
                "korean": "어디에 있나요",
                "thai": "อยู่ที่ไหน",
                "vietnamese": "Ở đâu"
            },
            "how_much": {
                "english": "How much",
                "spanish": "¿Cuánto cuesta",
                "french": "Combien coûte",
                "german": "Wie viel kostet",
                "italian": "Quanto costa",
                "japanese": "いくらですか",
                "chinese": "多少钱",
                "korean": "얼마인가요",
                "thai": "เท่าไหร่",
                "vietnamese": "Bao nhiêu"
            },
            "yes": {
                "english": "Yes",
                "spanish": "Sí",
                "french": "Oui",
                "german": "Ja",
                "italian": "Sì",
                "japanese": "はい",
                "chinese": "是",
                "korean": "네",
                "thai": "ใช่",
                "vietnamese": "Vâng"
            },
            "no": {
                "english": "No",
                "spanish": "No",
                "french": "Non",
                "german": "Nein",
                "italian": "No",
                "japanese": "いいえ",
                "chinese": "不",
                "korean": "아니요",
                "thai": "ไม่",
                "vietnamese": "Không"
            },
            "goodbye": {
                "english": "Goodbye",
                "spanish": "Adiós",
                "french": "Au revoir",
                "german": "Auf Wiedersehen",
                "italian": "Arrivederci",
                "japanese": "さようなら",
                "chinese": "再见",
                "korean": "안녕히 가세요",
                "thai": "ลาก่อน",
                "vietnamese": "Tạm biệt"
            },
            "help": {
                "english": "Help",
                "spanish": "Ayuda",
                "french": "Aide",
                "german": "Hilfe",
                "italian": "Aiuto",
                "japanese": "助けて",
                "chinese": "帮助",
                "korean": "도와주세요",
                "thai": "ช่วย",
                "vietnamese": "Giúp đỡ"
            }
        }
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> Dict[str, Any]:
        """Translate text to target language"""
        
        # Normalize language names
        target_lang = self._normalize_language(target_language)
        source_lang = self._normalize_language(source_language) if source_language != "auto" else "auto"
        
        # Check if language is supported
        if target_lang not in self.language_data["languages"]:
            return {
                "error": f"Unsupported target language: {target_language}",
                "supportedLanguages": list(self.language_data["languages"].keys())
            }
        
        # Simulate translation (in a real implementation, this would use a translation API)
        translated_text = self._simulate_translation(text, target_lang)
        
        # Get language information
        lang_info = self.language_data["languages"][target_lang]
        
        # Generate pronunciation guide
        pronunciation = self._generate_pronunciation_guide(translated_text, target_lang)
        
        # Get related phrases
        related_phrases = self._get_related_phrases(target_lang)
        
        return {
            "originalText": text,
            "translatedText": translated_text,
            "sourceLanguage": source_lang,
            "targetLanguage": target_lang,
            "languageInfo": lang_info,
            "pronunciation": pronunciation,
            "relatedPhrases": related_phrases,
            "confidence": 0.85  # Simulated confidence score
        }
    
    def _normalize_language(self, language: str) -> str:
        """Normalize language name to internal format"""
        language = language.lower().strip()
        
        # Map common variations
        language_mapping = {
            "en": "english",
            "eng": "english",
            "es": "spanish",
            "esp": "spanish",
            "fr": "french",
            "fra": "french",
            "de": "german",
            "ger": "german",
            "it": "italian",
            "ita": "italian",
            "pt": "portuguese",
            "por": "portuguese",
            "ru": "russian",
            "rus": "russian",
            "zh": "chinese",
            "chi": "chinese",
            "ja": "japanese",
            "jpn": "japanese",
            "ko": "korean",
            "kor": "korean",
            "ar": "arabic",
            "ara": "arabic",
            "hi": "hindi",
            "hin": "hindi",
            "th": "thai",
            "tha": "thai",
            "vi": "vietnamese",
            "vie": "vietnamese",
            "tr": "turkish",
            "tur": "turkish"
        }
        
        return language_mapping.get(language, language)
    
    def _simulate_translation(self, text: str, target_language: str) -> str:
        """Simulate translation (in real implementation, use translation API)"""
        
        # For demonstration, return common phrases if they match
        text_lower = text.lower().strip()
        
        for phrase_type, translations in self.common_phrases.items():
            if text_lower in translations.get("english", "").lower():
                return translations.get(target_language, text)
        
        # For other text, simulate translation by adding language marker
        lang_info = self.language_data["languages"][target_language]
        return f"[{lang_info['native']}] {text}"
    
    def _generate_pronunciation_guide(self, text: str, language: str) -> str:
        """Generate pronunciation guide for translated text"""
        
        pronunciation_guides = {
            "spanish": {
                "Hola": "OH-lah",
                "Gracias": "GRAH-see-ahs",
                "Por favor": "por fah-VOR"
            },
            "french": {
                "Bonjour": "bohn-ZHOOR",
                "Merci": "mehr-SEE",
                "S'il vous plaît": "seel voo PLEH"
            },
            "german": {
                "Hallo": "HAH-loh",
                "Danke": "DAHN-kuh",
                "Bitte": "BIT-tuh"
            },
            "japanese": {
                "こんにちは": "kon-nee-chee-wah",
                "ありがとう": "ah-ree-gah-toh",
                "お願いします": "oh-neh-gah-ee-shee-mahs"
            },
            "chinese": {
                "你好": "nee-hah-oh",
                "谢谢": "shieh-shieh",
                "请": "ching"
            }
        }
        
        guide = pronunciation_guides.get(language, {})
        return guide.get(text, f"Pronunciation guide not available for {text}")
    
    def _get_related_phrases(self, language: str) -> Dict[str, str]:
        """Get related useful phrases for the target language"""
        related = {}
        
        for phrase_type, translations in self.common_phrases.items():
            if language in translations:
                related[phrase_type] = translations[language]
        
        return related
    
    def get_language_for_destination(self, destination: str) -> Dict[str, Any]:
        """Get the primary language(s) for a destination"""
        
        destination_languages = self.language_data["destinations"].get(destination, "english")
        
        if isinstance(destination_languages, list):
            # Multiple languages
            languages = []
            for lang in destination_languages:
                if lang in self.language_data["languages"]:
                    languages.append(self.language_data["languages"][lang])
            
            return {
                "destination": destination,
                "languages": languages,
                "primaryLanguage": languages[0] if languages else None,
                "secondaryLanguages": languages[1:] if len(languages) > 1 else []
            }
        else:
            # Single language
            lang_info = self.language_data["languages"].get(destination_languages, None)
            
            return {
                "destination": destination,
                "languages": [lang_info] if lang_info else [],
                "primaryLanguage": lang_info,
                "secondaryLanguages": []
            }
    
    def get_essential_phrases(self, destination: str) -> Dict[str, Any]:
        """Get essential phrases for a destination"""
        
        # Get language for destination
        lang_info = self.get_language_for_destination(destination)
        primary_lang = lang_info.get("primaryLanguage", {})
        
        if not primary_lang:
            return {
                "error": f"No language information found for {destination}",
                "suggestedLanguage": "english"
            }
        
        # Get phrases in the primary language
        language_key = None
        for key, lang_data in self.language_data["languages"].items():
            if lang_data["code"] == primary_lang["code"]:
                language_key = key
                break
        
        if not language_key:
            return {
                "error": f"Language not found: {primary_lang['name']}",
                "suggestedLanguage": "english"
            }
        
        # Get essential phrases
        essential_phrases = {}
        for phrase_type, translations in self.common_phrases.items():
            if language_key in translations:
                essential_phrases[phrase_type] = {
                    "phrase": translations[language_key],
                    "pronunciation": self._generate_pronunciation_guide(translations[language_key], language_key),
                    "english": translations.get("english", "")
                }
        
        return {
            "destination": destination,
            "language": primary_lang,
            "essentialPhrases": essential_phrases,
            "totalPhrases": len(essential_phrases)
        }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of the input text"""
        
        # Simple language detection based on common words
        text_lower = text.lower()
        
        # Language detection patterns
        patterns = {
            "spanish": ["hola", "gracias", "por favor", "adiós", "sí", "no"],
            "french": ["bonjour", "merci", "oui", "non", "au revoir", "s'il vous plaît"],
            "german": ["hallo", "danke", "bitte", "ja", "nein", "auf wiedersehen"],
            "italian": ["ciao", "grazie", "per favore", "sì", "no", "arrivederci"],
            "japanese": ["こんにちは", "ありがとう", "はい", "いいえ", "さようなら"],
            "chinese": ["你好", "谢谢", "是", "不", "再见"],
            "korean": ["안녕하세요", "감사합니다", "네", "아니요", "안녕히 가세요"],
            "thai": ["สวัสดี", "ขอบคุณ", "ใช่", "ไม่", "ลาก่อน"],
            "vietnamese": ["xin chào", "cảm ơn", "vâng", "không", "tạm biệt"]
        }
        
        detected_languages = []
        for lang, words in patterns.items():
            for word in words:
                if word in text_lower:
                    detected_languages.append(lang)
                    break
        
        if detected_languages:
            primary_lang = detected_languages[0]
            lang_info = self.language_data["languages"].get(primary_lang, {})
            
            return {
                "detectedLanguage": primary_lang,
                "languageInfo": lang_info,
                "confidence": 0.8,
                "alternativeLanguages": detected_languages[1:] if len(detected_languages) > 1 else []
            }
        else:
            return {
                "detectedLanguage": "english",
                "languageInfo": self.language_data["languages"]["english"],
                "confidence": 0.6,
                "alternativeLanguages": []
            } 