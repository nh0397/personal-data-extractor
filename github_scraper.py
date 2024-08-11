import requests
import base64
import os

def fetch_github_repositories(username):
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_ACCESS_TOKEN')}"
    }
    url = f'https://api.github.com/users/{username}/repos'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        repos = response.json()

        repo_data = []
        for repo in repos:
            readme_url = f'https://api.github.com/repos/{username}/{repo["name"]}/readme'
            readme_response = requests.get(readme_url, headers=headers)
            readme_response.raise_for_status()

            readme_content = base64.b64decode(readme_response.json()['content']).decode('utf-8')
            
            data = {
                "name": repo['name'],
                "description": repo.get('description', 'No description provided'),
                "readme": readme_content,
                "languages_url": repo['languages_url'],
                "html_url": repo['html_url'],
                "created_at": repo['created_at'],
                "updated_at": repo['updated_at']
            }
            repo_data.append(data)
        
        return repo_data

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")  # Print the complete error
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return []
