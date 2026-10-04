def suggest_job_role(skills):

    roles = {
        "Machine Learning Engineer": ["python","machine learning","deep learning"],
        "Data Scientist": ["python","sql","data science"],
        "Backend Developer": ["python","flask"],
        "Software Developer": ["java","sql"],
        "Frontend Developer": ["html","css","javascript"]
    }

    for role, req in roles.items():
        if all(skill in skills for skill in req):
            return role

    return "Software Developer"