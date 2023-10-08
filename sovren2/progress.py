import base64
import requests
import json
import os
import datetime

# Function to generate a resume summary from the response data
def generate_resume_summary(resume_data):
    # Check if ContactInformation section exists in the response
    contact_info = resume_data.get('ContactInformation')
    if contact_info is None:
        return "Contact information not found in the resume."

    candidate_name = contact_info.get('CandidateName', {}).get('FormattedName', 'N/A')
    
    # Check if Telephones section exists in the response
    telephones = contact_info.get('Telephones', [])
    candidate_phone = ', '.join(phone['Raw'] for phone in telephones) if telephones else 'N/A'

    # Check if EmailAddresses section exists in the response
    email_addresses = contact_info.get('EmailAddresses', [])
    candidate_email = ', '.join(email_addresses) if email_addresses else 'N/A'

    # Extract skills
    skills = []
    skills_data = resume_data.get('Skills', {}).get('Raw', [])
    for skill_entry in skills_data:
        skills.append(skill_entry['Name'])

    education = resume_data.get('Education', {}).get('EducationDetails', [])
    education_info = []
    for entry in education:
        school = entry.get('SchoolName', {}).get('Raw', 'N/A')
        degree = entry.get('Degree', {}).get('Name', 'N/A')
        education_info.append(f"{degree} from {school} ({entry['LastEducationDate']['Date']})")

    experience = resume_data.get('EmploymentHistory', {}).get('Positions', [])
    experience_info = []
    for entry in experience:
        job_title = entry.get('JobTitle', {}).get('Raw', 'N/A')
        company = entry.get('Employer', {}).get('Name', {}).get('Raw', 'N/A')
        experience_info.append(f"{job_title} at {company}")

    summary = f"Name: {candidate_name}\n"
    summary += f"Phone: {candidate_phone}\n"
    summary += f"Email: {candidate_email}\n"
    summary += f"Skills: {', '.join(skills)}\n"
    summary += "Education:\n" + '\n'.join(education_info) + "\n"
    summary += "Experience:\n" + '\n'.join(experience_info) + "\n"

    return summary

# Define the file path of the resume
file_path = 'gg.docx'  # Adjust to the path of your resume file

base64str = ''

# Open the file, encode the bytes to base64, then decode that to a UTF-8 string
with open(file_path, 'rb') as f:
    base64str = base64.b64encode(f.read()).decode('UTF-8')

epochSeconds = os.path.getmtime(file_path)
lastModifiedDate = datetime.datetime.fromtimestamp(epochSeconds).strftime("%Y-%m-%d")

# Define the API endpoint URL based on your account data center
# Use https://eu-rest.resumeparsing.com/v10/parser/resume if your account is in the EU data center
# Use https://au-rest.resumeparsing.com/v10/parser/resume if your account is in the AU data center
url = "https://rest.resumeparsing.com/v10/parser/resume"

payload = {
    'DocumentAsBase64String': base64str,
    'DocumentLastModified': lastModifiedDate
    # Other options here (see https://sovren.com/technical-specs/latest/rest-api/resume-parser/api/)
}

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'sovren-accountid': "41332881",  
    'sovren-servicekey': "6I3Fp3yQF1EFqOyvjL7N6DAPrvaQ8r3wds34uKYe", 
}

# Make the request, NOTE: the payload must be serialized to a JSON string
response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    try:
        responseJson = json.loads(response.content)
        # Now, you can access the JSON data
        resumeData = responseJson.get('Value', {}).get('ResumeData', {})

        # Generate the resume summary
        summary = generate_resume_summary(resumeData)
        print(summary)

    except json.JSONDecodeError as e:
        print(f"Error parsing the response: {e}")
else:
    print(f"Error: {response.status_code}, {response.text}")
