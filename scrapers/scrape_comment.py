import os
import time
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
from model import engine, Comment  # Ensure correct import path

# Load environment variables
load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")


# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def linkedin_login():
    """Logs into LinkedIn using provided credentials."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(LINKEDIN_EMAIL)
    password_input.send_keys(LINKEDIN_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)
    print(" Login successful!")

def scrape_company_details(company_url):
    """Scrapes company details from a LinkedIn company page."""
    driver.get(company_url)
    time.sleep(5)

    try:
        content = driver.find_element(By.CSS_SELECTOR, "div.update-components-text div.update-components-update-v2__commentary").text
    except:
        content = "No content"

    try:
       post_id = driver.find_element(By.CSS_SELECTOR, "a.feed-shared-control-menu__content.artdeco-dropdown__content.artdeco-dropdown--is-dropdown-element.artdeco-dropdown__content--has-arrow.artdeco-dropdown__content--arrow-right.artdeco-dropdown__content--justification-right.artdeco-dropdown__content--placement-bottom.ember-view").get_attribute("href")
    except:
        post_id = "No post url"

    try:
       user_name = driver.find_element(By.CSS_SELECTOR, "a.feed-shared-control-menu__content.artdeco-dropdown__content.artdeco-dropdown--is-dropdown-element.artdeco-dropdown__content--has-arrow.artdeco-dropdown__content--arrow-right.artdeco-dropdown__content--justification-right.artdeco-dropdown__content--placement-bottom.ember-view").get_attribute("href")
    except:
        user_name = "No user name"



    try:
       created_at = driver.find_element(By.CSS_SELECTOR, "div > div > div.fie-impression-container > div.relative > div.GtjXTXpBiVBMuxFJjGInqHGgpmYsIlTXFNPc.display-flex.align-items-flex-start.update-components-actor--with-control-menu > div > div > span").text
    except:
        created_at = None

    


    # Store in database
    Session = sessionmaker(bind=engine)
    session = Session()

    company = Post(
        page_id=company_url.rstrip('/').split("/")[-2], 
        content=content,
        user_name=user_name,
        created_at=created_at,
        post_id=post_id,
        
    )

    session.add(company)
    session.commit()
    session.close()

    print(" Company details saved to database.")

if __name__ == "__main__":
    linkedin_login()
    company_url = "https://www.linkedin.com/company/microsoft/posts/"  # Change as needed
    scrape_company_details(company_url)
    driver.quit()

