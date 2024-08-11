import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

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

    # Load existing JSON data from final_data.json
    profile_data = {}
    try:
        with open('final_data.json', 'r') as json_file:
            profile_data = json.load(json_file)
            if not isinstance(profile_data, dict):
                profile_data = {}
    except FileNotFoundError:
        profile_data = {}

    # Scrape data from the main profile page
    driver.get(linkedin_url)
    time.sleep(5)  # Wait for the page to load completely

    main_page_data = driver.find_element(By.TAG_NAME, 'body').text
    profile_data['Main Profile'] = main_page_data

    # Define sections to scrape
    sections = {
        "Licenses and Certifications": linkedin_url + 'details/certifications/',
        "Skills": linkedin_url + 'details/skills/',
        "Recommendations": linkedin_url + 'details/recommendations/?detailScreenTabIndex=0',
        "Honors and Awards": linkedin_url + 'details/honors/'
    }

    # Scrape each section, focusing on 'artdeco-card' class content
    for section_name, section_url in sections.items():
        driver.get(section_url)
        time.sleep(5)  # Wait for the page to load completely

        artdeco_cards = driver.find_elements(By.CLASS_NAME, 'artdeco-card')
        section_content = "\n".join([card.text.strip() for card in artdeco_cards])

        profile_data[section_name] = section_content

    # Close the browser
    driver.quit()

    # Save the updated data into final_data.json
    with open('final_data.json', 'w') as json_file:
        json.dump(profile_data, json_file, indent=4)

    return profile_data
