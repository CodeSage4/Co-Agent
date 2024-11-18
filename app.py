import streamlit as st
from linkedin_summarizer import AssistantAgent, UserProxyAgent, llm_config
from time import sleep

# Initialize agents (assistant and user proxy)
assistant = AssistantAgent(name="assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

# Streamlit UI setup
st.title("Multi-Agent LinkedIn Post Generator")
st.subheader("Enter the Blog ID to generate a LinkedIn post summary")

# Input to get the Blog ID
blog_id = st.text_input("Enter Blog ID:")

# Placeholder for chat conversation and final post
chat_placeholder = st.empty()
final_post_placeholder = st.empty()

# Function to handle summary generation and agent conversation
def handle_summary_generation(blog_id):
    try:
        # Begin summary generation process
        chat_placeholder.write("**Assistant Agent**: Summarizing the blog content for a LinkedIn post...")        
        sleep(2)  # Simulate processing time
        
        # Get the blog content from the database
        blog_data = user_proxy.initiate_summary_process(blog_id)
        
        chat_placeholder.write(f"**Assistant Agent**: Here is the initial summary:\n\n{blog_data}")
        sleep(1)
        
        chat_placeholder.write("**User Proxy Agent**: Reviewing the summary for accuracy and tone...")
        sleep(2)  # Simulate review time
        
        # Simulate feedback from user proxy agent
        feedback = user_proxy.review_summary(blog_data)
        chat_placeholder.write(f"**User Proxy Agent**: Feedback received:\n\n{feedback.content}")
        
        # Check if summary is fine or needs revision
        if "No correction" in feedback.content:
            final_post_placeholder.write(f"**Final LinkedIn Post**: {blog_data}")
        else:
            chat_placeholder.write("**Assistant Agent**: Refining the summary based on feedback...")
            refined_summary = user_proxy.refine_summary(blog_data, feedback.content)
            chat_placeholder.write(f"**Assistant Agent**: Here is the refined summary:\n\n{refined_summary.content}")
            final_post_placeholder.write(f"**Final LinkedIn Post**: {refined_summary.content}")
        
    except Exception as e:
        st.error(f"Error: {e}")

# Trigger summary generation when the blog ID is entered
if blog_id:
    st.write("Processing the blog data...")
    handle_summary_generation(blog_id)
