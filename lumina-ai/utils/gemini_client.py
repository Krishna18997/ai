import streamlit as st
import google.generativeai as genai

# Read API key from Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    raise Exception(
        "GOOGLE_API_KEY not found. Add it in Streamlit Secrets."
    )

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"
