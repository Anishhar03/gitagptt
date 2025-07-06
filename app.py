import streamlit as st
import os
import base64
from dotenv import load_dotenv
from PIL import Image
from streamlit_audio_recorder import audio_recorder

# Google Gemini
import google.generativeai as genai

# Utils
from utils.loader import load_gita_text
from utils.vector_store import create_faiss_index
from utils.voice_io import audio_to_text, text_to_speech
from utils.translator import translate_text, language_codes
from utils.gpt_prompt import build_prompt

# --- Load Environment Variables --- #
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# --- Load and Process Gita --- #
gita_text = load_gita_text("gita_book.pdf")

# --- Create Vector Index --- #
vectorstore = create_faiss_index(gita_text, GOOGLE_API_KEY)

# --- Background Image --- #
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        b64_encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(10,10,30,0.6), rgba(10,10,30,0.6)),
                              url("data:image/jpg;base64,{b64_encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("krishna_ji.jpeg")

# --- Title and Avatar --- #
col1, col2 = st.columns([1, 4])
with col1:
    st.image("krishna_avatar.jpeg", width=80)
with col2:
    st.markdown('<h1 style="margin-top: 10px;">🕉️ Gita GPT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">Divine guidance from the Bhagavad Gita 📜</p>', unsafe_allow_html=True)

# --- Language Selection --- #
language = st.selectbox("🌐 Select Language", list(language_codes.keys()))

# --- Chat History --- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Input Section --- #
st.markdown("### 🎙️ Ask Krishna")
audio_bytes = audio_recorder(text="Click to record 🎤", icon_size="2x")
user_input = ""

if audio_bytes:
    try:
        user_input = audio_to_text(audio_bytes)
        st.success(f"🗣️ You said: {user_input}")
    except:
        st.warning("Could not recognize voice. Try again.")

if not user_input:
    user_input = st.text_input("🙏 Or type your question")

# --- Gemini Model --- #
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(user_input):
    results = vectorstore.similarity_search(user_input, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    prompt = build_prompt(user_input, context)
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Submit Button --- #
if st.button("🕊️ Ask Krishna"):
    if user_input.strip():
        with st.spinner("Fetching Krishna's divine wisdom..."):
            reply = generate_response(user_input)
            translated_reply = translate_text(reply, language)

            # Add to session history
            st.session_state.chat_history.append({
                "user": user_input,
                "bot": translated_reply
            })

            # Show reply
            st.markdown("### 🧘 Krishna says:")
            st.success(translated_reply)

            # Play voice
            try:
                audio_path = text_to_speech(translated_reply, language_codes[language])
                st.audio(audio_path, format="audio/mp3")
            except:
                st.warning("Could not generate Krishna's voice.")
    else:
        st.warning("Please enter or speak a question.")

# --- Chat History --- #
if st.session_state.chat_history:
    st.markdown("### 📜 Chat History")
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Krishna:** {chat['bot']}")
        st.markdown("---")

# --- Footer --- #
st.markdown("""
    <div style='text-align:center; color:#ccc; margin-top: 40px;'>
        🌸 Made with devotion by <strong>Anish</strong> 🙏
    </div>
""", unsafe_allow_html=True)
