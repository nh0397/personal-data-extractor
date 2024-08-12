import os
import json
import time
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import google.generativeai as genai
from github_scraper import fetch_github_repositories
from linkedin_scraper import scrape_linkedin_profile
from resume_parser import extract_resume_data

# Load environment variables
load_dotenv()

# Set up Gemini API key
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')

class GoogleEmbeddings:
    def __init__(self, model_name: str = "models/embedding-001") -> None:
        self.model_name = model_name

    def generate_embeddings(self, inp: str) -> np.ndarray:
        if not GEMINI_API_KEY:
            print("Please set correct Google API key")
            return []

        genai.configure(api_key=GEMINI_API_KEY)
        result = genai.embed_content(model=self.model_name,
                                content=inp,
                                task_type="retrieval_document",)

        try:
            embds = np.array(result.get("embedding", []))
        except:
            print("Embeddings not found")
            return []

        return list(list(embds.reshape(1, -1))[0])

def format_resume_with_gemini(resume_data):
    prompt = '''
    Given the following parsed resume data, extract and organize the information into a structured JSON format. The JSON should include the following fields:
    1. "full_name": The full name of the candidate.
    2. "email_address": The candidate's email address.
    3. "linkedin_url": The URL of the candidate's LinkedIn profile.
    4. "work_experience": A list of dictionaries.
    5. "skills": An array of skills listed in the resume.
    6. "projects": A list of dictionaries.
    7. "certifications": An array of certifications listed in the resume.

    Ensure that all extracted information is accurately formatted.

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
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(formatted_prompt)
    formatted_resume_data = json.loads(response.text)

    return formatted_resume_data

def format_linkedin_with_gemini(linkedin_data):
    prompt = '''
    Given the following parsed LinkedIn profile data, extract and organize the information into a structured JSON format. The JSON should include the following fields:
    1. "full_name": The full name of the profile owner.
    2. "headline": The headline or current designation.
    3. "location": The current location of the profile owner.
    4. "work_experience": A list of dictionaries.
    5. "education": A list of dictionaries.
    6. "skills": An array of skills listed in the LinkedIn profile.
    7. "certifications": A list of certifications.
    8. "honors_and_awards": A list of honors and awards.

    Ensure that all extracted information is accurately formatted.

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
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(formatted_prompt)
    formatted_linkedin_data = json.loads(response.text)

    return formatted_linkedin_data

def format_github_with_gemini(github_data):
    prompt = '''
    Given the following parsed GitHub repositories data, extract and organize the information into a structured JSON format. The JSON should include the following fields:
    1. "repositories": A list of repositories, each containing:
       - "name": The name of the repository.
       - "description": The description of the repository.
       - "languages_used": An array of languages used in the repository.
       - "creation_date": The date the repository was created.
       - "last_updated": The date the repository was last updated.

    Ensure that all extracted information is accurately formatted.

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
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(formatted_prompt)
    formatted_github_data = json.loads(response.text)

    return formatted_github_data

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

    # Initialize the GoogleEmbeddings class
    google_embeddings = GoogleEmbeddings()

    # Create embeddings for each section and store them in separate collections
    basic_details = {
        "Name": final_data["Name"],
        "email": final_data["email"],
        "linkedinURL": final_data["linkedinURL"],
        "githubURL": final_data["githubURL"]
    }
    basic_details_embeddings = google_embeddings.generate_embeddings(json.dumps(basic_details))

    resume_embeddings = google_embeddings.generate_embeddings(json.dumps(final_data["resume"]))
    linkedin_embeddings = google_embeddings.generate_embeddings(json.dumps(final_data["linkedin"]))
    github_embeddings = google_embeddings.generate_embeddings(json.dumps(final_data["github"]))

    # Connect to MongoDB
    from urllib.parse import quote_plus
    user_name = quote_plus("jaylodha97")
    password = quote_plus("Jaylodha@123")
    MONGO_URI=f"mongodb+srv://{user_name}:{password}@cluster0.5hufumz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    client = MongoClient(MONGO_URI)
    print(client)
    db = client[os.getenv('MONGO_DB_NAME')][os.getenv('MONGO_CL_NAME')]
    print(type(db))

    # Store embeddings in their respective collections
    # db['basic_details'].insert_one({"key": "basic_details", "embedding": basic_details_embeddings})
    # db['resume'].insert_one({"key": "resume", "embedding": resume_embeddings})
    # db['linkedin'].insert_one({"key": "linkedin", "embedding": linkedin_embeddings})
    # db['github'].insert_one({"key": "github", "embedding": github_embeddings})
    collection_data= [{
        "resume_data": json.dumps(final_data["resume"]),
        "embeddings": resume_embeddings
    },
    {
        "github_data": json.dumps(final_data["github"]),
        "embeddings": github_embeddings
    },
    {
        "linkedin_data": json.dumps(final_data["linkedin"]),
        "embeddings": linkedin_embeddings
    }]

    db.insert_many(collection_data)

    # Save the final data to final_data.json
    with open('final_data.json', 'w') as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    main()
