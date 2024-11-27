import streamlit as st
from co_agent import AssistantAgent, UserProxyAgent, llm_config
from co_agent import scraper

# Streamlit UI setup
st.title("Co-Agent")
st.caption("Multi-Agent Conversational Framework for designing 'Ready-to-Post' LinkedIn posts from blog URLs")

# Input to get the Blog ID
master_url = st.text_input("Enter Master URL of the Blog you want Co-Agent to make LinkedIn Posts of:")

if master_url:
    blog_scraper = scraper.BlogScraper(name = "blog_scraper", master_url=master_url)
    blog_scraper.scrape()   

   # Initialize agents (assistant and user proxy)
    st.subheader("Multi-Agent Chat started:")

    assistant = AssistantAgent(name="assistant", llm_config=llm_config)
    user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

    summary = user_proxy.initiate_postmaking_process("blog_1")
