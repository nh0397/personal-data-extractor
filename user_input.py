def prompt_user_for_info():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    github_username = input("Enter your GitHub username: ")
    linkedin_url = input("Enter your LinkedIn profile URL: ")
    
    return {
        "name": name,
        "email": email,
        "github_username": github_username,
        "linkedin_url": linkedin_url
    }
