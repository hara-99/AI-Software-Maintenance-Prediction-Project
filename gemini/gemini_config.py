import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

MODEL_NAME = "gemini-3.5-flash"

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to .env locally or Streamlit Cloud Secrets."
    )

from google import genai

client = genai.Client(api_key=API_KEY)