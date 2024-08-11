from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def scrape_linkedin_profile(linkedin_url):
    # Set up Selenium WebDriver options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # Initialize Chrome WebDriver using ChromeDriverManager and Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Log in to LinkedIn using credentials from .env
    driver.get('https://www.linkedin.com/login')
    driver.find_element(By.ID, 'username').send_keys(os.getenv('LINKEDIN_EMAIL'))
    driver.find_element(By.ID, 'password').send_keys(os.getenv('LINKEDIN_PASSWORD'))
    driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()

    # Wait for login to complete
    time.sleep(5)

    # Navigate to the desired LinkedIn profile
    driver.get(linkedin_url)
    time.sleep(5)  # Wait for the page to load completely

    # Extract sections using class name 'pv-profile-card'
    sections = driver.find_elements(By.CLASS_NAME, 'pv-profile-card')

    # Extract text from each section
    profile_data = {}
    for index, section in enumerate(sections):
        profile_data[f'Section_{index+1}'] = section.text.strip()

    # Close the browser
    driver.quit()

    # Print out extracted data
    for section, content in profile_data.items():
        print(f"{section}:\n{content}\n")

    return profile_data

