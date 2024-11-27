# linkedin_summarizer/config.py
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

llm_config = {
    "model": "gemini-1.5-flash",
    "api_key": "AIzaSyBSSzCI4YZZSqj1EvZkBkXO-7hW-3Rioj0", #os.getenv("GOOGLE_API_KEY"),
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}
