import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")


options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def linkedin_login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

   
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(LINKEDIN_EMAIL)

   
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(LINKEDIN_PASSWORD)
    password_field.send_keys(Keys.RETURN)

    time.sleep(3)  

    if "feed" in driver.current_url:
        print(" Login successful!")
    else:
        print(" Login failed!")

linkedin_login()
driver.quit()
