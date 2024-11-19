import streamlit as st
from linkedin_summarizer import AssistantAgent, UserProxyAgent, llm_config, agents
import time

# Streamlit UI setup
st.title("Co-Agent")
st.caption("Multi Agent Conversational Framework for exclusively designing 'Ready to post' and engaging LinkedIn Posts from just the Master URL of the blogs")

# Input to get the Blog ID
master_url = st.text_input("Enter Master URL of the Blog you want Co-Agent to make LinkedIn Posts of:")


#trigger scraping blogs
if master_url:
    st.write_stream(agents.stream_data("Scraping the blogs..."))
    
    # Initialize agents (assistant and user proxy)
    assistant = AssistantAgent(name="assistant", llm_config=llm_config)
    user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

    summary = user_proxy.initiate_summary_process("blog_1")





