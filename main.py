import os
import json
import re
import time
from dotenv import load_dotenv
import google.generativeai as genai
from github_scraper import fetch_github_repositories
from linkedin_scraper import scrape_linkedin_profile
from resume_parser import extract_resume_data

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^A-Za-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\n', ' ').replace('\r', '')
        return text.strip()
    else:
        return text

def clean_data(data):
    if isinstance(data, dict):
        return {section: clean_text(content) for section, content in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    else:
        return data

def format_resume_with_gemini(resume_data):
    prompt = '''
    Given the following parsed resume data, extract and organize the information into a structured JSON format. The JSON should include the following fields:

    [Insert your resume data prompt here]

    Here is the parsed resume data:

    {resume_data}

    Return the output in the following JSON format:

    {{
      "full_name": "string",
      "email_address": "string",
      "linkedin_url": "string",
      "work_experience": [
        {{
          "company_name": "string",
          "designation": "string",
          "description": "string",
          "start_date": "string",
          "end_date": "string"
        }},
        ...
      ],
      "skills": [
        "string",
        ...
      ],
      "projects": [
        {{
          "project_name": "string",
          "description": "string"
        }},
        ...
      ],
      "certifications": [
        "string",
        ...
      ]
    }}
    '''

    formatted_prompt = prompt.format(resume_data=json.dumps(resume_data, indent=4))

    model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type": "application/json"})

    response = model.generate_content(formatted_prompt)
    formatted_resume_data = response.text

    return json.loads(formatted_resume_data)

def format_linkedin_with_gemini(linkedin_data):
    prompt = '''
    Given the following parsed LinkedIn profile data, extract and organize the information into a structured JSON format. The JSON should include the following fields:

    [Insert your LinkedIn data prompt here]

    Here is the parsed LinkedIn profile data:

    {linkedin_data}

    Return the output in the following JSON format:

    {{
      "full_name": "string",
      "headline": "string",
      "location": "string",
      "work_experience": [
        {{
          "company_name": "string",
          "designation": "string",
          "description": "string",
          "start_date": "string",
          "end_date": "string"
        }},
        ...
      ],
      "education": [
        {{
          "institution_name": "string",
          "degree": "string",
          "field_of_study": "string",
          "start_date": "string",
          "end_date": "string"
        }},
        ...
      ],
      "skills": [
        "string",
        ...
      ],
      "certifications": [
        {{
          "certification_name": "string",
          "issuing_organization": "string",
          "issue_date": "string"
        }},
        ...
      ],
      "honors_and_awards": [
        {{
          "award_name": "string",
          "issuing_organization": "string",
          "issue_date": "string"
        }},
        ...
      ]
    }}
    '''

    formatted_prompt = prompt.format(linkedin_data=json.dumps(linkedin_data, indent=4))

    model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type": "application/json"})

    response = model.generate_content(formatted_prompt)
    formatted_linkedin_data = response.text

    return json.loads(formatted_linkedin_data)

def format_github_with_gemini(github_data):
    prompt = '''
    Given the following parsed GitHub repositories data, extract and organize the information into a structured JSON format. The JSON should include the following fields:

    [Insert your GitHub data prompt here]

    Here is the parsed GitHub repositories data:

    {github_data}

    Return the output in the following JSON format:

    {{
      "repositories": [
        {{
          "name": "string",
          "description": "string",
          "languages_used": ["string", ...],
          "creation_date": "string",
          "last_updated": "string"
        }},
        ...
      ]
    }}
    '''

    formatted_prompt = prompt.format(github_data=json.dumps(github_data, indent=4))

    model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type": "application/json"})

    response = model.generate_content(formatted_prompt)
    formatted_github_data = response.text

    return json.loads(formatted_github_data)

def main():
    user_data = {
        "name": os.getenv('USER_NAME'),
        "email": os.getenv('USER_EMAIL'),
        "github_username": os.getenv('GITHUB_USERNAME'),
        "linkedin_url": os.getenv('LINKEDIN_URL')
    }

    github_projects = fetch_github_repositories(user_data['github_username'])
    linkedin_data = scrape_linkedin_profile(user_data['linkedin_url'])
    resume_data = extract_resume_data("./resources/Resume.pdf")

    time.sleep(10)  # Wait before processing with Gemini API

    formatted_resume_data = format_resume_with_gemini(resume_data)
    
    time.sleep(10)  # Wait before processing with Gemini API

    formatted_linkedin_data = format_linkedin_with_gemini(linkedin_data)

    time.sleep(10)  # Wait before processing with Gemini API

    formatted_github_data = format_github_with_gemini(github_projects)

    final_data = {
        "Name": user_data['name'],
        "email": user_data['email'],
        "linkedinURL": user_data['linkedin_url'],
        "githubURL": f"https://github.com/{user_data['github_username']}",
        "resume": formatted_resume_data,
        "github": formatted_github_data,
        "linkedin": formatted_linkedin_data
    }

    with open('final_data.json', 'w') as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    main()
