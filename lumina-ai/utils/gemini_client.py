import streamlit as st
import google.generativeai as genai

# Get API key from Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    raise Exception(
        "GOOGLE_API_KEY not found. Add it in Streamlit Secrets."
    )

# Configure Gemini
genai.configure(api_key=API_KEY)

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")


def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "No response generated."

    except Exception as e:
        return f"Gemini Error: {str(e)}"
