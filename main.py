from github_scraper import fetch_github_repositories
from linkedin_scraper import scrape_linkedin_profile
from resume_parser import extract_resume_data
from data_processing import create_final_json
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables from .env file
load_dotenv()

def clean_text(text):
    if isinstance(text, str):
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove non-alphanumeric characters (excluding spaces)
        text = re.sub(r'[^A-Za-z0-9\s]', '', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Additional cleaning (e.g., remove any specific junk patterns)
        text = text.replace('\n', ' ').replace('\r', '')
        return text.strip()
    else:
        # If the input is not a string, return it as is
        return text

def clean_data(data):
    if isinstance(data, dict):
        # Clean text for each section in a dictionary
        return {section: clean_text(content) for section, content in data.items()}
    elif isinstance(data, list):
        # Clean each item in a list
        return [clean_data(item) for item in data]
    else:
        # If data is neither a list nor a dictionary, return it as-is
        return data

def parse_and_print_json(data, indent=0):
    """
    Recursively parse and print the JSON data.
    Handles nested dictionaries and lists.
    """
    spaces = ' ' * indent
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{spaces}{key}:")
            parse_and_print_json(value, indent + 4)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            print(f"{spaces}[{index}]:")
            parse_and_print_json(item, indent + 4)
    else:
        print(f"{spaces}{data}")

def main():
    # Get user information from environment variables
    user_data = {
        "name": os.getenv('USER_NAME'),
        "email": os.getenv('USER_EMAIL'),
        "github_username": os.getenv('GITHUB_USERNAME'),
        "linkedin_url": os.getenv('LINKEDIN_URL')
    }

    # Fetch GitHub projects data
    github_projects = fetch_github_repositories(user_data['github_username'])

    # Scrape LinkedIn profile data
    linkedin_data = scrape_linkedin_profile(user_data['linkedin_url'])
    
    # Debug: Print raw LinkedIn data
    print("Raw LinkedIn data:")
    parse_and_print_json(linkedin_data)

    # Extract data from resume
    resume_data = extract_resume_data("./resources/Resume.pdf")

    # Clean the LinkedIn data and other sections if needed
    linkedin_data = clean_data(linkedin_data)
    github_projects = clean_data(github_projects)
    resume_data = clean_data(resume_data)

    # Process and create the final JSON
    final_data = create_final_json(user_data, github_projects, linkedin_data, resume_data)

    # Ensure that the final data is not accidentally converted to a string
    if isinstance(final_data, str):
        final_data = json.loads(final_data)
    
    print("Generated JSON data:")
    parse_and_print_json(final_data)

    # Save the cleaned and final JSON to a file
    with open('final_data.json', 'w') as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    main()
