# linkedin_summarizer/database.py

# Simulated Shared Database (replace with a real database connection for production)
database = {
    # "blog_1": {
    #     "blog_heading": "The Power of Consistency in Achieving Goals",
    #     "blog_content": "In our fast-paced world, it's easy to get distracted by new trends and immediate rewards. We often set big goals and then expect quick results. However, the key to long-term success is consistency—putting in steady, focused effort every day, no matter how small the progress seems. Consistency isn’t about being perfect. It’s about showing up, day in and day out, and doing your best. Whether you’re working on improving your fitness, advancing in your career, or learning a new skill, consistent effort compounds over time. Small, consistent steps lead to big results, but they only work if you stay committed. One of the easiest ways to develop consistency is to break your goal into manageable tasks. Instead of thinking about a huge project, focus on what you can do today. Just as a marathon runner doesn’t run 26 miles in one step, you shouldn’t expect instant results. With each step you take, you're building momentum that will carry you toward your goal. Remember, success is not about the immediate outcome, but about showing up and giving your best effort each day. In time, you’ll look back and realize that those small, consistent actions have added up to something significant.",
    #     "linkedin_summary": None
    # }
}

def import_db(db: dict):
    global database
    database = db


def get_blog_data(blog_id: str):
    """Retrieve the blog data for a given blog ID."""
    return database.get(blog_id)

def save_blog_data(blog_id: str, heading: str, content: str, summary: str = None):
    """Save new blog data into the database."""
    database[blog_id] = {
        "blog_heading": heading,
        "blog_content": content,
        "linkedin_summary": summary, 
    }
    return True

def save_summary(blog_id: str, summary: str):
    """Save the LinkedIn summary for a specific blog."""
    if blog_id in database:
        database[blog_id]["linkedin_summary"] = summary
        return True
    return False

def get_blog_heading(blog_id):
    """Get the heading of the blog."""
    blog_data = get_blog_data(blog_id)
    return blog_data.get("blog_heading") if blog_data else None

def get_blog_url(blog_id):
    """Get the URL of the blog."""
    blog_data = get_blog_data(blog_id)
    return f"https://co-agent.streamlit.app/{blog_id}" if blog_data else None
