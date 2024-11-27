from co_agent import database

class BlogScraper:
    def __init__(self, name: str, master_url: str):
        self.name = name
        self.master_url = master_url

    def scrape(self):
        database.scrape_blog(self.master_url)