import tempfile
import speech_recognition as sr
from gtts import gTTS

def audio_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        with sr.AudioFile(tmp.name) as source:
            audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    path = tempfile.mktemp(suffix=".mp3")
    tts.save(path)
    return path
