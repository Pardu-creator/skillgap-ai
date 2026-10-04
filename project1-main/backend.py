import json
import os
import hashlib
import re
from pypdf import PdfReader

try:
    import streamlit as st
    from openai import OpenAI
except Exception:
    st = None
    OpenAI = None


# ==========================================================
# FILE PATHS
# ==========================================================
USER_FILE = "users.json"


# ==========================================================
# USER AUTHENTICATION
# ==========================================================
def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return {}


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    username = username.strip().lower()
    password = password.strip()

    if username == "" or password == "":
        return False

    users = load_users()

    if username in users:
        return False

    users[username] = {
        "password": hash_password(password)
    }

    save_users(users)
    return True


def login_user(username, password):
    username = username.strip().lower()
    password = password.strip()

    if username == "" or password == "":
        return False

    users = load_users()

    if username not in users:
        return False

    return users[username]["password"] == hash_password(password)


# ==========================================================
# PDF TEXT EXTRACTION
# ==========================================================
def extract_resume_text(uploaded_file):
    text = ""

    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception:
        return ""

    return text.lower()


# ==========================================================
# SKILL DATABASE
# ==========================================================
SKILLS = [
    "python", "java", "c", "c++", "javascript", "typescript",
    "html", "css", "react", "angular", "vue", "node js",
    "express js", "bootstrap", "tailwind", "django", "flask",
    "fastapi", "streamlit",

    "sql", "mysql", "postgresql", "mongodb", "sqlite",
    "oracle", "firebase", "redis",

    "data science", "data analysis", "machine learning",
    "deep learning", "artificial intelligence", "statistics",
    "numpy", "pandas", "matplotlib", "seaborn", "scikit learn",
    "tensorflow", "keras", "pytorch", "opencv", "nlp",
    "computer vision", "power bi", "tableau", "excel",

    "aws", "azure", "google cloud", "gcp", "docker",
    "kubernetes", "jenkins", "git", "github", "gitlab",
    "linux", "ci cd",

    "data structures", "algorithms", "oops",
    "object oriented programming", "system design", "api",
    "rest api", "microservices", "software testing",
    "debugging",

    "cyber security", "network security", "ethical hacking",
    "cryptography",

    "communication", "leadership", "problem solving",
    "teamwork", "critical thinking", "time management"
]


# ==========================================================
# SKILL EXTRACTION
# ==========================================================
def normalize_text(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"[^a-zA-Z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text):
    text = normalize_text(text)
    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill.title())

    return sorted(list(set(found_skills)))


def extract_required_skills(job_description):
    jd = normalize_text(job_description)
    required_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, jd):
            required_skills.append(skill.title())

    return sorted(list(set(required_skills)))


# ==========================================================
# JOB ROLE SUGGESTION
# ==========================================================
def suggest_jobs(skills):
    skills_lower = [skill.lower() for skill in skills]

    roles = []

    if "python" in skills_lower and "sql" in skills_lower:
        roles.append("Data Analyst")

    if "python" in skills_lower and (
        "machine learning" in skills_lower or "data science" in skills_lower
    ):
        roles.append("Machine Learning Engineer")

    if (
        "deep learning" in skills_lower
        or "tensorflow" in skills_lower
        or "pytorch" in skills_lower
        or "keras" in skills_lower
    ):
        roles.append("AI Engineer")

    if (
        "html" in skills_lower
        and "css" in skills_lower
        and "javascript" in skills_lower
    ):
        roles.append("Frontend Developer")

    if (
        "flask" in skills_lower
        or "django" in skills_lower
        or "fastapi" in skills_lower
        or "node js" in skills_lower
    ):
        roles.append("Backend Developer")

    if (
        "react" in skills_lower
        or "angular" in skills_lower
        or "vue" in skills_lower
    ):
        roles.append("Web Developer")

    if (
        "aws" in skills_lower
        or "azure" in skills_lower
        or "google cloud" in skills_lower
        or "docker" in skills_lower
        or "kubernetes" in skills_lower
    ):
        roles.append("Cloud / DevOps Engineer")

    if (
        "cyber security" in skills_lower
        or "network security" in skills_lower
        or "ethical hacking" in skills_lower
    ):
        roles.append("Cyber Security Analyst")

    if (
        "power bi" in skills_lower
        or "tableau" in skills_lower
        or "excel" in skills_lower
    ):
        roles.append("Business Intelligence Analyst")

    if not roles:
        roles.append("Software Developer Trainee")

    return sorted(list(set(roles)))


# ==========================================================
# SCORE CALCULATION
# ==========================================================
def calculate_employability_score(
    resume_skills,
    required_skills,
    matched_skills,
    missing_skills
):
    if len(required_skills) == 0:
        skill_match_score = 60
    else:
        skill_match_score = int((len(matched_skills) / len(required_skills)) * 100)

    skill_strength_score = min(100, len(resume_skills) * 5)

    penalty = len(missing_skills) * 4

    final_score = int(
        (skill_match_score * 0.7)
        + (skill_strength_score * 0.3)
        - penalty
    )

    final_score = max(0, min(100, final_score))

    return final_score


# ==========================================================
# RESUME SUGGESTIONS
# ==========================================================
def generate_suggestions(resume_text, missing_skills):
    suggestions = []

    if missing_skills:
        suggestions.append(
            "Improve these missing skills: " + ", ".join(missing_skills)
        )
    else:
        suggestions.append(
            "Your resume has good skill alignment with the job description."
        )

    if "project" not in resume_text and "projects" not in resume_text:
        suggestions.append(
            "Add at least 2 to 3 strong projects related to your target job role."
        )

    if "internship" not in resume_text:
        suggestions.append(
            "Add internship, training, certification, or practical experience details."
        )

    if "github" not in resume_text:
        suggestions.append(
            "Add your GitHub profile link and project repository links."
        )

    if "linkedin" not in resume_text:
        suggestions.append(
            "Add your LinkedIn profile for better professional visibility."
        )

    if "achievement" not in resume_text and "achievements" not in resume_text:
        suggestions.append(
            "Add achievements, certifications, hackathons, workshops, or awards."
        )

    if "sql" not in resume_text:
        suggestions.append(
            "Add SQL knowledge because it is important for most data and software roles."
        )

    if "communication" not in resume_text:
        suggestions.append(
            "Mention communication, teamwork, and problem-solving skills."
        )

    return suggestions


# ==========================================================
# LEARNING ROADMAP
# ==========================================================
def generate_learning_roadmap(missing_skills):
    roadmap = []

    if not missing_skills:
        roadmap.append({
            "week": "Week 1",
            "skill": "Advanced Projects",
            "task": "Build one real-time project and upload it to GitHub."
        })

        roadmap.append({
            "week": "Week 2",
            "skill": "Interview Preparation",
            "task": "Practice aptitude, coding, resume explanation, and mock interviews."
        })

        return roadmap

    for index, skill in enumerate(missing_skills, start=1):
        roadmap.append({
            "week": f"Week {index}",
            "skill": skill,
            "task": f"Learn {skill}, practice basics, and build one mini project using {skill}."
        })

    roadmap.append({
        "week": "Final Week",
        "skill": "Resume Upgrade",
        "task": "Update resume with new skills, GitHub links, project details, and deployment links."
    })

    return roadmap


# ==========================================================
# MAIN RESUME ANALYSIS
# ==========================================================
def analyze_resume(uploaded_file, job_description):
    resume_text = extract_resume_text(uploaded_file)

    if resume_text == "":
        return {
            "error": "Unable to read resume PDF. Please upload a valid text-based PDF."
        }

    resume_skills = extract_skills(resume_text)
    required_skills = extract_required_skills(job_description)

    matched_skills = sorted(list(set(resume_skills) & set(required_skills)))
    missing_skills = sorted(list(set(required_skills) - set(resume_skills)))

    if len(required_skills) == 0:
        match_score = 60
    else:
        match_score = int((len(matched_skills) / len(required_skills)) * 100)

    employability_score = calculate_employability_score(
        resume_skills,
        required_skills,
        matched_skills,
        missing_skills
    )

    suggestions = generate_suggestions(resume_text, missing_skills)

    job_roles = suggest_jobs(resume_skills)

    roadmap = generate_learning_roadmap(missing_skills)

    return {
        "resume_text": resume_text,
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
        "employability_score": employability_score,
        "suggestions": suggestions,
        "job_roles": job_roles,
        "roadmap": roadmap
    }


# ==========================================================
# AI MENTOR USING OPENAI API
# ==========================================================
def ai_mentor_response(question, analysis_result=None, chat_history=None):
    if chat_history is None:
        chat_history = []

    if OpenAI is None or st is None:
        return "AI package is not available. Please install openai and streamlit."

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key and st is not None and hasattr(st, "secrets"):
            api_key = st.secrets.get("OPENAI_API_KEY", "")

        if not api_key:
            return (
                "OpenAI API key is missing. Please configure OPENAI_API_KEY "
                "in your environment variables or Streamlit secrets."
            )

        model_name = os.getenv("OPENAI_MODEL")
        if not model_name and st is not None and hasattr(st, "secrets"):
            model_name = st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini")
        if not model_name:
            model_name = "gpt-4.1-mini"

        client = OpenAI(api_key=api_key)

        if analysis_result:
            context = f"""
Resume Skills: {analysis_result.get("resume_skills", [])}
Required Skills: {analysis_result.get("required_skills", [])}
Matched Skills: {analysis_result.get("matched_skills", [])}
Missing Skills: {analysis_result.get("missing_skills", [])}
Match Score: {analysis_result.get("match_score", 0)}%
Employability Score: {analysis_result.get("employability_score", 0)}%
Suggested Roles: {analysis_result.get("job_roles", [])}
Suggestions: {analysis_result.get("suggestions", [])}
"""
        else:
            context = "No resume analysis available yet."

        history_text = ""

        for msg in chat_history[-8:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_text += f"{role.upper()}: {content}\n"

        prompt = f"""
You are an advanced AI career mentor inside a Skill-Gap Aware Employability Assessment Platform.

Your behavior:
- Answer like a helpful mentor.
- Use simple language for college students.
- Give practical steps.
- Suggest projects, skills, resume improvements, and interview preparation.
- If resume analysis is available, personalize the answer.
- Do not give very long answers unless asked.
- Use bullet points when useful.

Student Resume Analysis:
{context}

Previous Chat:
{history_text}

Student Question:
{question}
"""

        response = client.responses.create(
            model=model_name,
            input=prompt
        )

        return response.output_text

    except Exception as e:
        err_msg = str(e)
        # Redact any accidental key leaks or bearer tokens
        if "sk-" in err_msg or "Bearer" in err_msg or "api_key" in err_msg.lower():
            return "AI Mentor encountered an authentication error. Please verify your OpenAI API key configuration."
        return f"AI Mentor error: {err_msg}"
