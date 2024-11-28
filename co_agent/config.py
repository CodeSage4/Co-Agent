# linkedin_summarizer/config.py
import streamlit as st_c

llm_config = {
    "model": "gemini-1.5-flash",
    "api_key": st_c.secrets["google_api_key"],
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}
