# linkedin_summarizer/database.py
import os
import streamlit as st_d
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# Simulated Shared Database (replace with a real database connection for production)
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
    # Initialize the Edge driver
    driver_dir = os.path.join(os.getcwd(), "edgedriver_win64")
    st_d.write(driver_dir)
    driver_path = os.path.join(driver_dir, "msedgedriver.exe")
    st_d.write(driver_path)
    service = EdgeService(executable_path=driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up the Edge WebDriver for scraping
    driver = webdriver.Edge(service=service, options=options)

    # Open the Google AI blog page
    st_d.write("Scraping articles from the blogsite...")
    driver.get(master_url)

    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract the heading (assumes h1 is used for the main title)
        heading = soup.find("h1")
        heading_text = heading.text.strip() if heading else "Heading not found"

        # Extract the content (assumes content is within <p> tags)
        paragraphs = soup.find_all("p")
        content = "\n".join(p.text.strip() for p in paragraphs) if paragraphs else "Content not found"

        # Close the driver
        driver.quit()

        # Display the scraped information
        st_d.subheader("Scraped Blog:")
        st_d.write(heading_text)
        st_d.caption(content[:1000])  # Limit the content display to the first 1000 characters

    except Exception as e:
        st_d.error(f"An error occurred: {e}")
        driver.quit()

    global database
    # Store the article in the database
    database[f"blog_1"] = {
        "blog_heading": heading_text,
        "blog_content": content,
        "blog_link": master_url,  # Include the link
        "linkedin_summary": None
    }