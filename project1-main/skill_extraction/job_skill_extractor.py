from skill_extraction.skill_extractor import extract_skills

job_description = """
We are looking for a Python developer with knowledge of Machine Learning,
SQL, and AWS cloud. Experience in Flask or Django is preferred.
"""

skills = extract_skills(job_description)

print("----- JOB REQUIRED SKILLS -----")
print(skills)