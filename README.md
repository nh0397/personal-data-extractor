# Personal Data Extractor

This project is designed to automate the extraction of personal data from LinkedIn profiles, GitHub repositories, and resumes, and then generate a structured JSON file with the extracted information. 

The project uses Python, Selenium, BeautifulSoup, and various other libraries to accomplish this.

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Google Chrome Browser
- ChromeDriver (automatically managed by webdriver_manager)

## Installation


Clone the Repository

```
git clone https://github.com/yourusername/RAG-Personal-Data-Extractor.git
cd RAG-Personal-Data-Extractor
```

Install Required Python Packages

Install all the required Python packages using pip:

```
pip install -r requirements.txt
```

If you don't have a requirements.txt file, you can manually install the required packages:

```
pip install selenium beautifulsoup4 webdriver-manager python-dotenv pymupdf
```

Environment Setup

Create a .env file in the project root directory and add your credentials:

```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
GITHUB_ACCESS_TOKEN=your_github_access_token
LINKEDIN_URL=https://www.linkedin.com/in/your-profile-url/
```
- Replace your_email@example.com with your LinkedIn email.
- Replace your_password with your LinkedIn password.
- Replace your_github_access_token with your GitHub Personal Access Token.
- Replace https://www.linkedin.com/in/your-profile-url/ with your LinkedIn profile URL.

### Add Your Resume

Place your resume file named `Resume.pdf` in the `./resources/` directory of the project. This file will be used for resume parsing.


## Running the Project

Execute the main Python script to start the data extraction process:
```
python main.py
```
The script will:

- Log in to your LinkedIn account and scrape the profile data.
- Fetch all repositories from your GitHub account and extract README content.
- Parse your resume from a PDF file located in ./resources/Resume.pdf.
- Combine the extracted data into a structured JSON file and save it as final_data.json.
- Review the Output

The extracted data will be printed in the terminal and saved in a JSON file named final_data.json in the project root directory.

## Project Structure
```
├── linkedin_scraper.py         # LinkedIn scraping script
├── github_scraper.py           # GitHub scraping script
├── resume_parser.py            # Resume parsing script
├── user_input.py               # Script for handling user input
├── data_processing.py          # Script for processing and generating final JSON
├── main.py                     # Main script to run the project
├── .env                        # Environment variables file
├── README.md                   # Project documentation
├── requirements.txt            # Python package dependencies
└── resources/
    └── Resume.pdf              # Your resume file for parsing
```    
## Troubleshooting

403 Error When Fetching GitHub Data:

- Ensure your GitHub Personal Access Token has the necessary permissions to read your repositories.
- Check your API rate limits on GitHub.
- If you don't have a personal access token, go to https://github.com/settings/tokens

LinkedIn Scraping Issues:

- If Selenium is not able to log in to LinkedIn, ensure that the email and password in the .env file are correct.
- If LinkedIn profile data is not being scraped correctly, verify the profile URL and the page structure for any changes.

PDF Extraction Issues:

- Ensure that the pymupdf package is installed correctly and that your resume file is located in the ./resources/ directory.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to create a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.