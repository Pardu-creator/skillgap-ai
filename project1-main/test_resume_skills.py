from resume_parser import extract_text_from_resume
from skill_extraction.skill_extractor import extract_skills

resume_path = "uploads/resumes/sample_resume.pdf"

text = extract_text_from_resume(resume_path)

skills = extract_skills(text)

print("----- RESUME SKILLS -----")
print(skills)