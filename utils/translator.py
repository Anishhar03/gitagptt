from googletrans import Translator

translator = Translator()

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Urdu": "ur"
}

def translate_text(text, target_language):
    lang_code = language_codes.get(target_language, "en")
    result = translator.translate(text, dest=lang_code)
    return result.text
