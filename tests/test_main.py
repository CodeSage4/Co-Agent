# tests/test_main.py
from linkedin_summarizer import AssistantAgent, UserProxyAgent, llm_config




#def test_summary_generation():
assistant = AssistantAgent(name="assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

summary = user_proxy.initiate_summary_process("blog_1")
#assert summary is not None
#assert "LinkedIn" in summary
