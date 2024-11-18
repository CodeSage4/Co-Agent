from langchain_google_genai import ChatGoogleGenerativeAI
from .database import get_blog_data, save_summary

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
        print("-------------------------------------------------------------")
        print("ASSISTANT: \n Generating Summary... \n")
        prompt = [
            ("system", "Summarize the following blog content for a LinkedIn post."),
            ("human", blog_content)
        ]
        return self.respond(prompt)

class UserProxyAgent:
    def __init__(self, name: str, assistant: AssistantAgent):
        print("-------------------------------------------------------------")
        print("USER PROXY: \n Assistant Can you please Summarize the following blog content for a LinkedIn post")
        self.name = name
        self.assistant = assistant

    def review_summary(self, summary: str):
        print("-------------------------------------------------------------")
        print("USER PROXY: \n Reviewing Summary... \n")
        prompt = [
            ("system", "Review the following LinkedIn summary for factual accuracy, grammar, legal compliance, and tone. List any required corrections or return with 'no correction' if the summary is ok. "),
            ("human", summary)
        ]
        return self.assistant.respond(prompt)

    def initiate_summary_process(self, blog_id: str):
        blog_data = get_blog_data(blog_id)
        if not blog_data:
            return "------------------------------------------------------------- \nASSISTANT: \n Blog data not found."
        print("Blog_heading \n Blog_link")

        # Generate the initial summary
        summary = self.assistant.generate_summary(blog_data["blog_content"])
        summary = summary.content
        print(f"Initial Summary:\n{summary}")

        i = 0
        
        while i < 5:
            review_feedback = self.review_summary(summary)
            review_feedback = review_feedback.content
            print(f"Review Feedback:\n {review_feedback}")

            if "No correction" in review_feedback:
                save_summary(blog_id, summary)
                print("-------------------------------------------------------------")
                print("Summary approved and saved in the Database.")
                print("-------------------------------------------------------------")
                print(f"Final approved Summary:\n {summary}")
                return summary
            else:
                summary = self.refine_summary(summary, review_feedback)
                print(f"Refined Summary: {summary}")
                i = i+1

    def refine_summary(self, summary: str, feedback: str):
        print("-------------------------------------------------------------")
        print("ASSISTANT: \n Refining summary... \n")
        prompt = [
            ("system", f"Revise the summary based on the following feedback to ensure accuracy and compliance."),
            ("human", f"Summary: {summary}\nFeedback: {feedback}")
        ]
        return self.assistant.respond(prompt)
