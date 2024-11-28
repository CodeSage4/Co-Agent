# Co-Agent: Multi-Agent Conversational Framework  

[![PyPI version](https://badge.fury.io/py/coagent-framework.svg)](https://pypi.org/project/coagent-framework/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  

Co-Agent is a sophisticated **Multi-Agent Conversational Framework** designed to automate the creation of **LinkedIn-ready posts** from blog content. Leveraging advanced AI technologies such as **Google Gemini** for natural language processing and **multi-agent systems** for task delegation, Co-Agent ensures an engaging, professional, and shareable output tailored for social media.  

---

## 🌟 Key Features  

- **Intelligent Blog Scraping**  
   Extracts meaningful content from blogs using a customizable scraper.  

- **AI-Driven Summarization**  
   Summarizes blogs into concise LinkedIn posts, maintaining professional tone and format.  

- **Multi-Agent Collaboration**  
   Deploys a dynamic agent-based system for iterative content refinement, ensuring quality and coherence.  

- **Cross-Platform Support**  
   Features both a **Streamlit-based UI** and **console-based interface** for accessibility and user convenience.  

- **Plug-and-Play Architecture**  
   Easily integrates with pre-trained LLMs like Google Gemini or other APIs for future scalability.  

- **Preformatted Outputs**  
   Produces LinkedIn-ready summaries complete with hashtags, headlines, and call-to-action links.  

---

## 🚀 Quick Start  

### Installation  

Install Co-Agent from PyPI using the following command:  

```bash
pip install coagent-framework
```  


### Usage  

#### Console Workflow  

Here’s a step-by-step example for using Co-Agent via the console:  

```python
from co_agent import AssistantAgent, UserProxyAgent, llm_config
from co_agent import scraper

# Setting up the Google Gemini LLM API key
llm_config["api_key"] = "Your_Google_API_Key"

# Initializing the scraper
blog_scraper = scraper.BlogScraper(name="blog_scraper")
blog_scraper.scrape()   

# Initialize agents (Assistant and User Proxy)
print("Multi-Agent Chat started:")

assistant = AssistantAgent(name="assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(name="user_proxy", assistant=assistant)

# Process blog content for LinkedIn
summary = user_proxy.initiate_postmaking_process("blog_1")
```  

#### Streamlit UI  
To use Co-Agent with an interactive interface, visit the Streamlit app here:
👉 https://co-agent.streamlit.app/

Simply enter the blog URL in the provided field, and the app will guide you through the process of generating a LinkedIn-ready post.

---

## 🛠️ How It Works  

### Core Components  

1. **Scraper Module**  
   The scraper fetches content from a user-provided blog URL, stripping unnecessary formatting while retaining essential information.  

2. **Multi-Agent System**  
   - **AssistantAgent:** Responsible for generating initial summaries from blog content.  
   - **UserProxyAgent:** Reviews and refines the summary based on user feedback and iterative collaboration.  

3. **LLM Integration**  
   Google Gemini, or a similar LLM, is used for understanding context, generating concise summaries, and formatting content.  

4. **Database Storage**  
   Approved summaries are stored in a database for later retrieval, ensuring content reusability.  

5. **Formatter**  
   Formats the final summary into a LinkedIn-ready post, including a headline, body, hashtags, and call-to-action links.  

---

## 📂 Directory Structure  

The following is the structure of the project:  

```
coagent_framework/co_agent/
├── agents.py          # Multi-agent system implementation
├── scraper.py         # Blog scraping functionality
├── database.py        # Database utilities
├── config.py          # Configuration settings
app.py                 # main file
pyproject.toml         # Poetry configuration for dependencies
README.md              # Project documentation
```  

---

## 📊 Example Output  

### Input  

Blog URL: [Viola-Jones Algorithm Blog](https://medium.com/@pvt.dhruvkumar/viola-jones-algorithm-a-miracle-5e10085aba50)  

### Output  

**Headline:**  
Viola-Jones Object Detection: A Revolutionary Leap in Computer Vision  

**Body:**  
Remember the early 2000s when real-time object detection felt like science fiction? That all changed thanks to the groundbreaking work of Viola and Jones! Their 2001 algorithm, a marvel of machine learning, used a boosted cascade of simple features (Haar-like features and AdaBoost) to achieve incredibly efficient object detection. This clever approach prioritized relevant features and quickly discarded irrelevant ones, making real-time face detection a reality – a true game-changer!

This algorithm's impact is still felt today. Easily accessible via OpenCV, it continues to serve as a foundational element in many computer vision applications. Want to delve deeper into the magic behind this revolutionary technique? 

---

## 🧑‍💻 Contributing  

We welcome contributions to Co-Agent! If you would like to contribute:  

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/YourFeature`).  
3. Commit your changes (`git commit -m 'Add YourFeature'`).  
4. Push the branch (`git push origin feature/YourFeature`).  
5. Open a Pull Request.  

For major changes, please open an issue first to discuss your ideas.  

---

## ⚖️ License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  

---
