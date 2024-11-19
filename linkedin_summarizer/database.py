# linkedin_summarizer/database.py

# Simulated Shared Database (replace with a real database connection for production)
database = {}

def get_blog_data(blog_id: str):
    """Retrieve the blog data for a given blog ID."""
    return database.get(blog_id)

def save_blog_data(blog_id: str, heading: str, content: str, summary: str = None):
    """Save new blog data into the database."""
    database[blog_id] = {
        "blog_heading": heading,
        "blog_content": content,
        "linkedin_summary": summary
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
