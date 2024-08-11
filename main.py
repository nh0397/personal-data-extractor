from github_scraper import fetch_github_repositories
from linkedin_scraper import scrape_linkedin_profile
from resume_parser import extract_resume_data
from user_input import prompt_user_for_info
from data_processing import create_final_json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def main():
    # Prompt user for basic information
    user_data = prompt_user_for_info()

    # Fetch GitHub projects data
    github_projects = fetch_github_repositories(user_data['github_username'])

    # Scrape LinkedIn profile data
    linkedin_data = scrape_linkedin_profile(os.getenv('LINKEDIN_URL'))

    # Extract data from resume
    resume_data = extract_resume_data("./resources/Resume.pdf")

    # Process and create the final JSON
    final_data = create_final_json(user_data, github_projects, linkedin_data, resume_data)
    print("Generated JSON data:")
    print(final_data)

    # Optionally, save the JSON to a file
    with open('final_data.json', 'w') as f:
        f.write(final_data)

if __name__ == "__main__":
    main()
