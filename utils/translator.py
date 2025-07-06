from googletrans import Translator

translator = Translator()

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Sanskrit": "sa"
}

def translate_text(text, language):
    if language == "English":
        return text
    return translator.translate(text, dest=language_codes[language]).text
