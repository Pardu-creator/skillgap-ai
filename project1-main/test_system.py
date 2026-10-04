from resume_parser import extract_text_from_resume
from skill_extraction.skill_extractor import extract_skills
from skill_extraction.job_skill_extractor import extract_skills as job_extract
from skill_gap_analysis import analyze_skill_gap
from employability_score import calculate_employability_score


# Resume path
resume_path = "uploads/resumes/sample_resume.pdf"

# Extract resume text
resume_text = extract_text_from_resume(resume_path)

# Extract resume skills
resume_skills = extract_skills(resume_text)

# Job description
job_description = """
We are looking for a Python developer with knowledge of Machine Learning,
SQL, AWS, and Flask framework.
"""

# Extract job skills
job_skills = extract_skills(job_description)

# Skill gap analysis
matched, missing = analyze_skill_gap(resume_skills, job_skills)

# Employability score
score = calculate_employability_score(matched, job_skills)


print("\n----- EMPLOYABILITY ANALYSIS -----\n")

print("Resume Skills:", resume_skills)
print("Job Required Skills:", job_skills)

print("\nMatched Skills:", matched)
print("Missing Skills:", missing)

print("\nEmployability Score:", score, "%")