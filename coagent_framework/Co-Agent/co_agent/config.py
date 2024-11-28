# linkedin_summarizer/config.py

llm_config = {
    "model": "gemini-1.5-flash", # replace it with your desired google model
    "api_key": "Google_API_Key", # replace it with your Google Gemini API Key 
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}

# def set_api_key(api_key:str):
#     global llm_config
