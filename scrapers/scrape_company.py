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
from model import engine, Page  


load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")



options = Options()
options.add_argument("--headless") 
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
  

def scrape_company_details(company_url):
    """Scrapes company details from a LinkedIn company page."""
    driver.get(company_url)
    time.sleep(5)

    try:
        name = driver.find_element(By.CSS_SELECTOR, "h1").text
    except:
        name = None

    try:
        description = driver.find_element(By.XPATH, '//section/p').text  
    except:
        description = None


    try:
        website = driver.find_element(By.CSS_SELECTOR, "section dl dd:nth-child(2)").text
    except:
        website = None



    try:
       industry = driver.find_element(By.XPATH, "//div[contains(@class, 'org-top-card-summary-info-list__info-item')]").text
    except:
        industry = None

    import re

    try:
        followers_text = driver.find_element(By.CSS_SELECTOR, "section dl dd:nth-child(9)").text
        followers = int(re.sub(r"[^\d]", "", followers_text))  
    except:
        followers = None



    try:
        headcount = driver.find_element(By.XPATH, "//section/dl/dd[4]").text
    except:
        headcount = None

    try:
        specialties = driver.find_element(By.CSS_SELECTOR, "section > dl > dd:nth-child(13)").text

    except:
        specialties = None

    try:
        profile_picture_element = driver.find_element(By.CSS_SELECTOR, ".org-top-card-primary-content__logo")
        profile_picture = profile_picture_element.get_attribute("src") 
    except:
        profile_picture = None




    
    Session = sessionmaker(bind=engine)
    session = Session()

    company = Page(
        linkedin_id=company_url.rstrip('/').split("/")[-2], 
        name=name,
        url=company_url,
        description=description,
        website=website,
        industry=industry,
        followers=followers,
        headcount=headcount,
        specialties=specialties,
        profile_picture=profile_picture,
    )

    session.add(company)
    session.commit()
    session.close()

    print(" Company details saved to database.")

if __name__ == "__main__":
    linkedin_login()
    company_url = "https://www.linkedin.com/company/microsoft/about/"  
    scrape_company_details(company_url)
    driver.quit()

