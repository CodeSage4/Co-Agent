import requests
from bs4 import BeautifulSoup


database = {
    # "blog_1": {
    #     "blog_heading": "The Power of Consistency in Achieving Goals",
    #     "blog_content": "In our fast-paced world, it's easy to get distracted by new trends and immediate rewards. We often set big goals and then expect quick results. However, the key to long-term success is consistency—putting in steady, focused effort every day, no matter how small the progress seems. Consistency isn’t about being perfect. It’s about showing up, day in and day out, and doing your best. Whether you’re working on improving your fitness, advancing in your career, or learning a new skill, consistent effort compounds over time. Small, consistent steps lead to big results, but they only work if you stay committed. One of the easiest ways to develop consistency is to break your goal into manageable tasks. Instead of thinking about a huge project, focus on what you can do today. Just as a marathon runner doesn’t run 26 miles in one step, you shouldn’t expect instant results. With each step you take, you're building momentum that will carry you toward your goal. Remember, success is not about the immediate outcome, but about showing up and giving your best effort each day. In time, you’ll look back and realize that those small, consistent actions have added up to something significant.",
    #     "linkedin_summary": None
    # }
}

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

def scrape_blog(master_url:str):
    

    try:
        # Send an HTTP GET request to the blog URL
        response = requests.get(master_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the blog. Status code: {response.status_code}")


        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the heading (assumes h1 is used for the main title)
        heading = soup.find("h1")
        heading_text = heading.text.strip() if heading else "Heading not found"

        # Extract the content (assumes content is within <p> tags)
        paragraphs = soup.find_all("p")
        content = "\n".join(p.text.strip() for p in paragraphs) if paragraphs else "Content not found"

        # Display the scraped information
        print("Scraped Blog:")
        print(heading_text)
        print(content[:1000])  # Limit the content display to the first 1000 characters

    except Exception as e:
        print(f"An error occurred: {e}")

    global database
    # Store the article in the database
    database[f"blog_1"] = {
        "blog_heading": heading_text,
        "blog_content": content,
        "blog_link": master_url,  # Include the link
        "linkedin_summary": None
    }