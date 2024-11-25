from langchain_google_genai import ChatGoogleGenerativeAI
from .database import get_blog_data, save_summary, get_blog_heading, get_blog_url
import streamlit as st_a
import time

def stream_data(stream:str):
    for word in stream.split(" "):
        yield word + " "
        time.sleep(0.02)

class BaseAgent:
    def __init__(self, name: str, llm_config: dict):
        self.name = name
        self.llm_config = llm_config
        self.llm = self.initialise_llm()

    def initialise_llm(self):
        if "model" not in self.llm_config or "api_key" not in self.llm_config:
            raise ValueError("LLM configuration must include 'model' and 'api_key'.")
        return ChatGoogleGenerativeAI(
            model=self.llm_config["model"],
            api_key=self.llm_config["api_key"],
            temperature=self.llm_config.get("temperature", 0.7),
            max_tokens=self.llm_config.get("max_tokens", 150)
        )
    def respond(self, messages: list):
        try:
            return self.llm.invoke(messages)
        except Exception as e:
            return f"Error during LLM invocation: {e}"

class AssistantAgent(BaseAgent):
    def generate_summary(self, blog_content: str):
        st_a.write("-------------------------------------------------------------")
        st_a.write(" :violet[ASSISTANT:]")
        st_a.caption("Generating summary...")
        
        prompt = [
            ("system", "Summarize the following blog content for a LinkedIn post."),
            ("human", blog_content)
        ]
        return self.respond(prompt)

class UserProxyAgent:
    def __init__(self, name: str, assistant: AssistantAgent):
        st_a.write("-------------------------------------------------------------")
        st_a.write(" :orange[USER PROXY:]")
        st_a.write_stream(stream_data(" Assistant, Can you please Summarize the following blog content for a LinkedIn post"))
        self.name = name
        self.assistant = assistant

    def review_summary(self, summary: str):
        st_a.write("-------------------------------------------------------------")
        st_a.write(" :orange[USER PROXY:]")
        st_a.caption(" Reviewing Summary... \n")
        prompt = [
            ("system", "Review the following LinkedIn summary for factual accuracy, grammar, legal compliance, and tone. List any required corrections or return with 'no correction' if the summary is ok. "),
            ("human", summary)
        ]
        return self.assistant.respond(prompt)

    def initiate_summary_process(self, blog_id: str):
        blog_data = get_blog_data(blog_id)
        blog_heading = get_blog_heading(blog_id)
        blog_url = get_blog_url(blog_id)
        if not blog_data:
            st_a.write("-------------------------------------------------------------")
            st_a.write(" :violet[ASSISTANT:]")
            st_a.write_stream(stream_data(" :red[Blog data not found.]\n"))
            
        st_a.write(f"Blog Heading: {blog_heading}")
        st_a.write(f"Blog URL: [link](%s)" % blog_url)

        # Generate the initial summary
        summary = self.assistant.generate_summary(blog_data["blog_content"])
        if "Quota exceeded" in str(summary):
            st_a.write("LLM API quota exceeded. Please check the API provider Request Quota Limit")
            return "LLM API quota exceeded. Please check the API provider Request Quota Limit"
        summary = summary.content
        st_a.write_stream(stream_data(f":blue[Initial Summary:]  {summary}"))

        i = 0
        
        while True:
            review_feedback = self.review_summary(summary)
            review_feedback = review_feedback.content
            
            st_a.write_stream(stream_data(f" :red[Review Feedback:]  {review_feedback}"))

            if "No correction" in review_feedback:
                save_summary(blog_id, summary)
                st_a.write("-------------------------------------------------------------")
                st_a.write_stream(stream_data(" :green[Summary approved] and saved in the Database"))
                st_a.write("-------------------------------------------------------------")
                st_a.write_stream(stream_data((f":green[Final approved Summary:]  {summary}")))
                st_a.write("-------------------------------------------------------------")
                
                return summary
            
            elif i == 5:
                st_a.write("-------------------------------------------------------------")
                st_a.write_stream(stream_data(f" :red[Summary is approved] with this :red[Review Feedback:]  {review_feedback}"))
                st_a.write("-------------------------------------------------------------")
                st_a.write_stream(stream_data((f":green[Final approved Summary:] {summary}")))
                st_a.write("-------------------------------------------------------------")

            else:
                summary = self.refine_summary(summary, review_feedback)
                summary = summary.content
                st_a.write("-------------------------------------------------------------")
                st_a.write(" :violet[ASSISTANT:]")
                st_a.write_stream(stream_data(f":green[Refined Summary:]  {summary}"))
                i = i+1

    def refine_summary(self, summary: str, feedback: str):
        st_a.write("-------------------------------------------------------------")
        st_a.write(" :violet[ASSISTANT:]")
        st_a.caption("Refining summary...")
        
        prompt = [
            ("system", f"Revise the summary based on the following feedback to ensure accuracy and compliance."),
            ("human", f"Summary: {summary}\nFeedback: {feedback}")
        ]
        return self.assistant.respond(prompt)
