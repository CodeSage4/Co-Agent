# linkedin_summarizer/config.py
from dotenv import load_dotenv, find_dotenv
import os
import streamlit as st_c
load_dotenv(find_dotenv())

llm_config = {
    "model": "gemini-1.5-flash",
    "api_key": st_c.secrets["google_api_key"]
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}
