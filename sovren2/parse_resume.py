import json

# Assuming you have the JSON response as a string (json_response) or loaded from a file
# Replace the following line with your JSON response data
json_response = '''
   (Insert your JSON response here)
'''

# Parse the JSON response
data = json.loads(json_response)

# Extract and format the resume data
name = f"Name: {data['PersonalInfo']['GivenName']} {data['PersonalInfo']['Surname']}"
phones = f"Phone: {', '.join(data['PersonalInfo']['Phones'])}"
email = f"Email: {data['PersonalInfo']['EmailAddresses'][0]}"
skills = f"Skills: {', '.join(data['Skills']['Raw'])}"

# Education
education_info = "\nEducation:"
for education in data['Education']['EducationDetails']:
    education_info += f"\n{{'Raw': '{education['Degree']['Name']['Raw']}', 'Normalized': '{education['Degree']['Name']['Normalized']}'}} from {education['SchoolName']['Raw']} ({education['LastEducationDate']['Date']})"

# Experience
experience_info = "\nExperience:"
for position in data['EmploymentHistory']['Positions']:
    employer_name = position['Employer']['Name']['Raw']
    job_title = position['JobTitle']['Raw']
    experience_info += f"\n{job_title} at {employer_name}"

# Print the formatted resume data
print(name)
print(phones)
print(email)
print(skills)
print(education_info)
print(experience_info)
