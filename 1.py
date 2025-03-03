import time
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your resume PDF
RESUME_PATH = "Alcaraz Jr, Leo D. - Resume.pdf"

# LinkedIn credentials (replace with your own)
LINKEDIN_EMAIL = "your_email@example.com"
LINKEDIN_PASSWORD = "your_password"

# Keywords for job search
JOB_KEYWORDS = ["freelance", "part-time", "work from home"]

# Extract text from resume PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Parse resume text into fields (customize based on your resume structure)
def parse_resume(text):
    resume_data = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "experience": []
    }
    
    # Example parsing logic (customize for your resume)
    lines = text.split('\n')
    for line in lines:
        if "@" in line and "." in line:  # Simple email detection
            resume_data["email"] = line.strip()
        if any(char.isdigit() for char in line) and any(char.isalpha() for char in line):  # Simple phone detection
            resume_data["phone"] = line.strip()
        if "experience" in line.lower():  # Example for experience
            resume_data["experience"].append(line.strip())
    
    return resume_data

# Initialize Selenium WebDriver
def initialize_driver():
    service = Service(executable_path="path_to_chromedriver")  # Replace with your ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Log in to LinkedIn
def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    # Enter email
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(email)
    
    # Enter password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    
    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(3)

# Search for jobs
def search_jobs(driver, keywords):
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(3)
    
    # Enter search keywords
    search_box = driver.find_element(By.XPATH, "//input[contains(@aria-label, 'Search jobs')]")
    search_box.send_keys(" ".join(keywords))
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

# Apply for a job
def apply_for_job(driver, resume_data):
    # Find the first job listing
    job_listing = driver.find_element(By.XPATH, "//li[contains(@class, 'job-result-card')]")
    job_listing.click()
    time.sleep(2)
    
    # Click the "Easy Apply" button (if available)
    try:
        easy_apply_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]")
        easy_apply_button.click()
        time.sleep(2)
        
        # Fill out the application form (customize based on form fields)
        name_field = driver.find_element(By.XPATH, "//input[contains(@id, 'name')]")
        name_field.send_keys(resume_data["name"])
        
        email_field = driver.find_element(By.XPATH, "//input[contains(@id, 'email')]")
        email_field.send_keys(resume_data["email"])
        
        phone_field = driver.find_element(By.XPATH, "//input[contains(@id, 'phone')]")
        phone_field.send_keys(resume_data["phone"])
        
        # Submit the application
        submit_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Submit application')]")
        submit_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Could not apply for this job: {e}")

# Main function
def main():
    # Extract and parse resume data
    resume_text = extract_text_from_pdf(RESUME_PATH)
    resume_data = parse_resume(resume_text)
    
    # Initialize WebDriver
    driver = initialize_driver()
    
    # Log in to LinkedIn
    linkedin_login(driver, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    
    # Search for jobs
    search_jobs(driver, JOB_KEYWORDS)
    
    # Apply for the first job
    apply_for_job(driver, resume_data)
    
    # Close the browser
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()