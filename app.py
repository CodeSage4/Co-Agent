import csv
import time
import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedin_summarizer import AssistantAgent, UserProxyAgent, llm_config, agents, database

# Streamlit UI setup
st.title("Co-Agent")
st.caption("Multi-Agent Conversational Framework for designing 'Ready-to-Post' LinkedIn posts from blog URLs")

# Input to get the Blog ID
master_url = st.text_input("Enter Master URL of the Blog you want Co-Agent to make LinkedIn Posts of:")

# Initialize database to store scraped articles
db = {}

if master_url:
    # Initialize the Edge driver
    driver_dir = os.path.join(os.getcwd(), "edgedriver_win64")
    #st.write(driver_dir)
    driver_path = os.path.join(driver_dir, "msedgedriver.exe")
    #st.write(driver_path)
    service = EdgeService(executable_path=driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up the Edge WebDriver for scraping
    driver = webdriver.Edge(service=service, options=options)

    # Open the Google AI blog page
    st.write("Scraping articles from the blogsite...")
    driver.get(master_url)

    # Wait for the articles to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uni-nup__card"))
    )

    # Extract article titles and links
    articles = driver.find_elements(By.CSS_SELECTOR, "div.uni-nup__card")
    article_info = []
    for article in articles:
        title_element = article.find_element(By.CSS_SELECTOR, "h3.uni-nup__header")
        link_element = article.find_element(By.CSS_SELECTOR, "a")

        title = title_element.text.strip()
        link = link_element.get_attribute("href").strip()

        article_info.append((title, link))

    # Fetch content for the first three articles and save them to the database
    st.write_stream(agents.stream_data("Scraping the blogs..."))

    
    for index, (title, link) in enumerate(article_info[:3], start=1):  # Process only the first 3 articles
        driver.get(link)

        try:
            # Wait for the article content to load
            article_content = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.module--text.module--text__article"))
            )
            paragraphs = article_content.find_elements(By.CSS_SELECTOR, "p")
            content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
        except Exception as e:
            content = "Content not available"

        # Store the article in the database
        db[f"blog_{index}"] = {
            "blog_heading": title,
            "blog_content": content,
            "blog_link": link,  # Include the link
            "linkedin_summary": None
        }

    database.import_db(db)
    # Close the WebDriver once done
    driver.quit()

    # Streamlit Display - Show the first three articles
    st.write("### First Three Articles")
    for index, article in db.items():
        st.write(f"**{article['blog_heading']}**")
        st.write(f"[Read more]({article['blog_link']})")
        st.write(article["blog_content"][:500])  # Display only the first 500 characters
        st.write("---")

   # Initialize agents (assistant and user proxy)
    st.subheader("Multi-Agent Chat started:")
    assistant = AssistantAgent(name="assistant", llm_config=llm_config)
    user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

    summary = user_proxy.initiate_summary_process("blog_1")
