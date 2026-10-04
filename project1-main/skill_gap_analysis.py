def analyze_skill_gap(resume_skills, job_skills):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched_skills = list(resume_set.intersection(job_set))
    missing_skills = list(job_set - resume_set)

    return matched_skills, missing_skills