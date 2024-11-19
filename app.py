import csv
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedin_summarizer import AssistantAgent, UserProxyAgent, llm_config, agents

# Streamlit UI setup
st.title("Co-Agent")
st.caption("Multi Agent Conversational Framework for exclusively designing 'Ready to post' and engaging LinkedIn Posts from just the Master URL of the blogs")

# Input to get the Blog ID
master_url = st.text_input("Enter Master URL of the Blog you want Co-Agent to make LinkedIn Posts of:")



# Initialize database to store scraped articles
database = {}


# Input to trigger scraping
#start_scraping = st.button("Start Scraping Google AI Blog")

if master_url:
    # Initialize the Edge driver
    driver_path = r"C:\Users\Lenovo\Downloads\edgedriver_win64\msedgedriver.exe"
    service = EdgeService(executable_path=driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up the Edge WebDriver for scraping
    driver = webdriver.Edge(service=service, options=options)

    # Open the Google AI blog page
    st.write("Scraping articles from Google AI blog...")
    driver.get("https://blog.google/technology/ai/")

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

    # Fetch article content for the first link and save to the database
    if article_info:
        st.write_stream(agents.stream_data("Scraping the blogs..."))
    
        # Initialize agents (assistant and user proxy)
        assistant = AssistantAgent(name="assistant", llm_config=llm_config)
        user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)
        
        first_article = article_info[0]
        title, link = first_article
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
        database["blog_1"] = {
            "blog_heading": title,
            "blog_content": content,
            "blog_link": link,  # Include the link
            "linkedin_summary": None
        }

        # Close the WebDriver once done
        driver.quit()

        # Streamlit Display - Show only the first article
        st.write("### First Article")
        st.write(f"**{title}**")
        st.write(f"[Read more]({link})")
        st.write(content[:500])  # Display only the first 500 characters of the article content

        # Optionally display the database
        st.write("### Database (Stored Articles)")
        st.json(database)
    else:
        st.write("No articles found.")
