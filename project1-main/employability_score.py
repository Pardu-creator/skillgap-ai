def calculate_employability_score(matched, job_skills):

    if len(job_skills) == 0:
        return 0

    score = (len(matched) / len(job_skills)) * 100

    return round(score, 2)