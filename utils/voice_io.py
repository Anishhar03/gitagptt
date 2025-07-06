from gtts import gTTS
import tempfile
import os

def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_path.name)
    return temp_path.name
