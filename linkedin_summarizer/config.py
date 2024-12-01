# linkedin_summarizer/config.py
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

llm_config = {
    "model": "gemini-1.5-flash",
    "api_key": "AIzaSyCPjK0rn3HFAlLitrgZX4pZ-YvPud9fQCY", #os.getenv("GOOGLE_API_KEY"),
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}
