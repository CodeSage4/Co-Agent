# linkedin_summarizer/config.py

import os

llm_config = {
    "model": "gemini-1.5-flash",
    "api_key": "AIzaSyCPjK0rn3HFAlLitrgZX4pZ-YvPud9fQCY",   #os.environ.get("GOOGLE_API_KEY"),
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}
