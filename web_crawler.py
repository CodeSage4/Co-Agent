import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver(driver_path):
    """
    Initializes the Selenium WebDriver for Edge.

    Args:
    - driver_path (str): Path to the Edge WebDriver.

    Returns:
    - webdriver instance
    """
    service = EdgeService(executable_path=driver_path)
    driver = webdriver.Edge(service=service)
    return driver

def scrape_article_links(driver, url, wait_time=10):
    """
    Scrapes article titles and links from a given webpage.

    Args:
    - driver (webdriver instance): The Selenium WebDriver instance.
    - url (str): The URL of the page to scrape.
    - wait_time (int): Time in seconds to wait for elements to load. Default is 10.

    Returns:
    - list of tuples: A list of tuples where each tuple contains (title, link).
    """
    driver.get(url)

    # Wait for the articles to load
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uni-nup__card"))
    )

    articles = driver.find_elements(By.CSS_SELECTOR, "div.uni-nup__card")

    article_info = []
    for article in articles:
        title_element = article.find_element(By.CSS_SELECTOR, "h3.uni-nup__header")
        link_element = article.find_element(By.CSS_SELECTOR, "a")

        title = title_element.text.strip()
        link = link_element.get_attribute("href").strip()

        article_info.append((title, link))

    return article_info

def fetch_article_content(driver, link, wait_time=10):
    """
    Fetches the content of an article from its URL.

    Args:
    - driver (webdriver instance): The Selenium WebDriver instance.
    - link (str): The URL of the article.
    - wait_time (int): Time in seconds to wait for the article content to load. Default is 10.

    Returns:
    - str: The content of the article.
    """
    driver.get(link)

    try:
        article_content = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.module--text.module--text__article"))
        )
        paragraphs = article_content.find_elements(By.CSS_SELECTOR, "p")
        content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
        return content
    except Exception as e:
        print(f"Could not fetch article content: {e}")
        return "Content not available"

def save_to_dict(article_info):
    """
    Saves the scraped article information (title, link, content) in the specified dictionary format.

    Args:
    - article_info (list of tuples): A list of tuples where each tuple contains (title, link, content).
    
    Returns:
    - dict: A dictionary containing all articles in the desired format.
    """
    database = {}
    for idx, (title, link, content) in enumerate(article_info, 1):
        blog_key = f"blog_{idx}"
        database[blog_key] = {
            "blog_heading": title,
            "blog_content": content,
            "linkedin_summary": None  # You can add logic for LinkedIn summary if needed.
        }
    
    return database

def main(driver_path, url):
    """
    Main function to scrape articles and save to dictionary.

    Args:
    - driver_path (str): Path to the Edge WebDriver.
    - url (str): The URL of the page to scrape.
    """
    driver = initialize_driver(driver_path)

    try:
        article_info = scrape_article_links(driver, url)

        # Fetch content for each article and store in the dictionary
        articles_with_content = []
        for title, link in article_info:
            print(f"Fetching content for: {title}")
            content = fetch_article_content(driver, link)
            articles_with_content.append((title, link, content))
            time.sleep(2)  # Optional: Wait before navigating to the next link

        # Save to dictionary
        database = save_to_dict(articles_with_content)
        print(f"Scraped {len(database)} articles.")

        # Printing the dictionary for verification
        for blog_key, data in database.items():
            print(f"Blog Key: {blog_key}")
            print(f"Blog Heading: {data['blog_heading']}")
            print(f"Blog Content: {data['blog_content']}")
            print(f"LinkedIn Summary: {data['linkedin_summary']}\n" + "-"*80 + "\n")
    
    finally:
        driver.quit()
