import os
import time
import sys
import mysql.connector
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sqlalchemy.orm import sessionmaker
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
from model import engine, Post, Comment  # Ensure correct import path for Post and Comment models

# Load environment variables
load_dotenv()
USERNAME = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
COMPANY_PAGE_URL = "https://www.linkedin.com/company/microsoft/posts/"

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "18052310",
    "database": "linkedin_insights"
}

# Selenium WebDriver setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

def connect_to_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def login(driver):
    """Logs into LinkedIn."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD + Keys.RETURN)
    time.sleep(5)
    print("Login successful!")

def scroll_down(driver):
    """Scroll down the page to load more posts."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_posts(driver, db_conn):
    """Scrapes posts from a LinkedIn company page."""
    driver.get(COMPANY_PAGE_URL)
    time.sleep(5)
    scroll_down(driver)
    
    posts = driver.find_elements(By.CSS_SELECTOR, "div.fie-impression-container")
    page_id = COMPANY_PAGE_URL.rstrip('/').split("/")[-2]  # Extract company ID
    
    cursor = db_conn.cursor()
    
    for post in posts[:20]:
        try:
            post_content = post.find_element(By.CSS_SELECTOR, "div.chuOHdWluJcGhOyRxLDNsmlRmpDYUUfBvPovk").text.strip()
            post_url = post.find_element(By.XPATH, "ancestor::a").get_attribute("href")
        except:
            post_content = "No content"
            post_url = None
            
        post_id = hash(post_content)
        
        cursor.execute(
            "INSERT IGNORE INTO posts (id, page_id, content, post_url, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (post_id, page_id, post_content, post_url)
        )
        db_conn.commit()
        
        cursor.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
        post_db_id = cursor.fetchone()[0]
        
        scrape_comments(driver, post, post_db_id, db_conn)
    
    cursor.close()

def scrape_comments(driver, post, post_db_id, db_conn):
    """Scrapes comments for a given post."""
    try:
        post.find_element(By.XPATH, ".//button[contains(text(), 'comments')]").click()
        time.sleep(3)
        
        comment_elements = driver.find_elements(By.CSS_SELECTOR, "span.comments-comment-item__main-content")
        cursor = db_conn.cursor()
        
        for comment in comment_elements:
            comment_text = comment.text.strip()
            cursor.execute(
                "INSERT INTO comments (post_id, content, created_at) VALUES (%s, %s, NOW())",
                (post_db_id, comment_text)
            )
        
        db_conn.commit()
        cursor.close()
    except:
        pass

if __name__ == "__main__":
    db_conn = connect_to_db()
    try:
        login(driver)
        scrape_posts(driver, db_conn)
    finally:
        db_conn.close()
        driver.quit()
