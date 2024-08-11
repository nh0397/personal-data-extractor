import PyPDF2

def extract_resume_data(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Return the raw text, further processing could be added
        return text
