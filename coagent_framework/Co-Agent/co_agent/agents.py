from langchain_google_genai import ChatGoogleGenerativeAI
from .database import get_blog_data, save_summary, get_blog_heading, get_blog_url

class BaseAgent:
    def __init__(self, name: str, llm_config: dict):
        self.name = name
        self.llm_config = llm_config
        self.llm = self.initialise_llm()
        
        # Console UI setup
        print("----------------------------------------------------------------------")
        print("Co-Agent")
        print("Multi-Agent Conversational Framework for designing 'Ready-to-Post' LinkedIn posts from blog URLs")
        print("----------------------------------------------------------------------")

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
        print("-------------------------------------------------------------")
        print("ASSISTANT: ")
        print("Generating summary...")
        
        prompt = [
            ("system", "Summarize the following blog content for a LinkedIn post."),
            ("human", blog_content)
        ]
        return self.respond(prompt)

class UserProxyAgent:
    def __init__(self, name: str, assistant: AssistantAgent):
        print("-------------------------------------------------------------")
        print("USER PROXY: ")
        print(" Assistant, Can you please Summarize the following blog content for a LinkedIn post")
        self.name = name
        self.assistant = assistant

    def review_summary(self, summary: str):
        print("-------------------------------------------------------------")
        print("USER PROXY:")
        print(" Reviewing Summary... \n")
        prompt = [
            ("system", "Review the following LinkedIn summary for factual accuracy, grammar, legal compliance, and tone. List any required corrections or return with 'no correction' if the summary is ok. "),
            ("human", summary)
        ]
        return self.assistant.respond(prompt)

    def initiate_postmaking_process(self, blog_id: str):
        blog_data = get_blog_data(blog_id)
        blog_heading = get_blog_heading(blog_id)
        blog_url = get_blog_url(blog_id)
        formatter = Formatter(self.assistant)

        if not blog_data:
            print("-------------------------------------------------------------")
            print("ASSISTANT:")
            print("Blog data not found.")
            
        print(f"Blog Heading: {blog_heading}")
        print(f"Blog URL {blog_url}")

        # Generate the initial summary
        summary = self.assistant.generate_summary(blog_data["blog_content"])
        print(summary)
        if "Quota exceeded" in str(summary):
            print("LLM API quota exceeded. Please check the API provider Request Quota Limit")
            return "LLM API quota exceeded. Please check the API provider Request Quota Limit"
        summary = summary.content
        print(f"Initial Summary:  {summary}")

        i = 0
        
        while True:
            review_feedback = self.review_summary(summary)
            review_feedback = review_feedback.content
            
            print(f"Review Feedback:  {review_feedback}")

            if "No correction" in review_feedback:
                save_summary(blog_id, summary)
                print("-------------------------------------------------------------")
                print("Summary approved and saved in the Database")
                print("-------------------------------------------------------------")
                print(f"Final approved Summary:  {summary}")
                print("-------------------------------------------------------------")
                
                # Format the summary for LinkedIn using LLM
                linkedin_post = formatter.format_for_linkedin(summary, blog_heading, blog_url)
                return linkedin_post
            
            elif i == 5:
                print("-------------------------------------------------------------")
                print(f"Summary is approved with this Review Feedback: {review_feedback}")
                print("-------------------------------------------------------------")
                print(f"Final approved Summary:  {summary}")
                print("-------------------------------------------------------------")

                # Format the approved summary for LinkedIn using LLM
                linkedin_post = formatter.format_for_linkedin(summary, blog_heading, blog_url)
                return linkedin_post

            else:
                summary = self.refine_summary(summary, review_feedback)
                summary = summary.content
                print("-------------------------------------------------------------")
                print("ASSISTANT: ")
                print(f"Refined Summary: {summary}")
                i = i+1

    def refine_summary(self, summary: str, feedback: str):
        print("-------------------------------------------------------------")
        print("ASSISTANT:")
        print("Refining summary...")
        
        prompt = [
            ("system", f"Revise the summary based on the following feedback to ensure accuracy and compliance."),
            ("human", f"Summary: {summary}\nFeedback: {feedback}")
        ]
        return self.assistant.respond(prompt)

class Formatter(BaseAgent):
    def __init__(self, assistant: AssistantAgent):
        self.assistant = assistant  # Use the AssistantAgent to interact with the LLM
        
    def format_for_linkedin(self, summary: str, blog_heading: str, blog_url: str):
        """
        Formats the summary into a LinkedIn-ready post using the LLM.
        """
        print("FORMATTER:")
        print("Formatting summary for LinkedIn post using LLM...")
        
        # Create the prompt
        prompt = [
            ("system", "Format the following text into a professional, engaging LinkedIn post. Include relevant hashtags."),
            ("human", f"Blog Heading: {blog_heading}\nSummary: {summary}\nBlog URL: {blog_url}")
        ]

        # Get the response from the LLM
        try:
            response = self.assistant.respond(prompt)
            linkedin_post = response.content  # Extract the content of the response
        except Exception as e:
            linkedin_post = f"Error during LinkedIn post formatting: {e}"

        print("-------------------------------------------------------------")
        print("Formatted LinkedIn Post:")
        print(linkedin_post)
        return linkedin_post
