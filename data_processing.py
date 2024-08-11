import json

def create_final_json(user_data, github_projects, linkedin_data, resume_data):
    final_data = {
        "user": user_data,
        "github_projects": github_projects,
        "linkedin_data": linkedin_data,
        "resume": resume_data
    }
    
    # Convert the final data to JSON format
    final_json = json.dumps(final_data, indent=4)
    
    return final_json
