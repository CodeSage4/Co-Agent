from co_agent import AssistantAgent, UserProxyAgent, llm_config
from co_agent import scraper

#setting up the google gemini LLM api key
llm_config["api_key"] = "Google_API_Key"

#initializing scraper
blog_scraper = scraper.BlogScraper(name = "blog_scraper")
blog_scraper.scrape()   

# Initialize agents (assistant and user proxy)
print("Multi-Agent Chat started:")

assistant = AssistantAgent(name="assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

summary = user_proxy.initiate_postmaking_process("blog_1")
