def skill_gap(resume_skills, job_skills):

    matched = list(set(resume_skills) & set(job_skills))

    missing = list(set(job_skills) - set(resume_skills))

    return matched, missing