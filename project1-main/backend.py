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
# USER AUTHENTICATION (SQLITE DATABASE ENGINE)
# ==========================================================
import database

def load_users():
    """Returns dictionary of users, backed by SQLite database with JSON fallback."""
    stats = database.get_database_stats()
    # Read from DB connection
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, password_hash FROM users")
    users = {}
    for row in cursor.fetchall():
        users[row["email"]] = {"password": row["password_hash"]}
        users[row["username"]] = {"password": row["password_hash"]}
    conn.close()
    return users


def save_users(users):
    """Legacy helper maintained for backward compatibility."""
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "w") as file:
                json.dump(users, file, indent=4)
        except Exception:
            pass


def hash_password(password):
    """Secure PBKDF2-HMAC-SHA256 password hashing."""
    h, _ = database.hash_password_secure(password)
    return h


def register_user(username, password, full_name="", target_role="Full Stack Developer"):
    """Registers user in SQLite database."""
    ok, _ = database.register_user_db(
        email=username,
        password=password,
        full_name=full_name,
        target_role=target_role
    )
    return ok


def login_user(username, password):
    """Authenticates user against SQLite database with rate-limiting and lockout."""
    ok, _ = database.authenticate_user_db(username, password)
    return ok


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
def generate_offline_mentor_advice(question: str, analysis_result=None):
    """
    Intelligent Career Mentor Fallback Engine.
    Provides expert career intelligence, interview roadmaps, and technical guidance
    when an external LLM API is offline or unconfigured.
    """
    q_lower = question.lower()
    matched = analysis_result.get("matched_skills", ["Python", "SQL", "Git"]) if analysis_result else ["Python", "SQL", "Git"]
    missing = analysis_result.get("missing_skills", ["Docker", "Kubernetes", "AWS"]) if analysis_result else ["Docker", "AWS", "CI/CD"]
    roles = analysis_result.get("job_roles", ["Full Stack Developer", "Backend Engineer"]) if analysis_result else ["Software Engineer"]

    if any(k in q_lower for k in ["interview", "prep", "question", "mock"]):
        return (
            "### 🎯 AI Mentor: Technical Interview Preparation Strategy\n\n"
            "Here is your personalized roadmap to ace technical interviews:\n\n"
            "1. **Core Problem Solving (Algorithms & DS):**\n"
            "   - Master Arrays, Hash Maps, Sliding Window, and Binary Trees.\n"
            "   - Practice explaining time and space complexity ($O(n)$) clearly out loud.\n\n"
            "2. **System Architecture & APIs:**\n"
            "   - Be prepared to discuss REST vs. GraphQL, database indexing, and caching strategies.\n"
            "   - Explain how you design scalable backend endpoints with proper error handling.\n\n"
            "3. **Bridging Missing Skills:**\n"
            f"   - Leverage your proven strengths in **{', '.join(matched[:3])}** while addressing **{', '.join(missing[:2])}** with a live portfolio project.\n\n"
            "💡 *Pro-Tip:* When asked about an unfamiliar tool, explain foundational principles and how quickly you master new technologies."
        )
    elif any(k in q_lower for k in ["skill", "top", "learn", "technology", "stack", "recommend"]):
        return (
            "### 💡 Career Intelligence: Recommended Tech Stack\n\n"
            f"Based on industry hiring benchmarks for **{roles[0]}**:\n\n"
            "1. **Core Language & Concurrency:** Advanced Python (FastAPI, AsyncIO, Type Hints) or Node.js / TypeScript.\n"
            "2. **Data & Persistence Layer:** PostgreSQL / SQLite with optimized schema design and ORM tools (SQLAlchemy / Prisma).\n"
            "3. **Cloud & Containerization:** Docker container packaging and CI/CD automation (GitHub Actions, AWS ECS/S3).\n"
            "4. **AI & Modern Integration:** Practical experience building RAG pipelines or integrating LLM APIs.\n\n"
            f"✅ *Your Competitive Advantage:* You already have verified competencies in **{', '.join(matched[:3])}**!"
        )
    elif any(k in q_lower for k in ["resume", "improve", "score", "ats"]):
        return (
            "### 📄 Resume Optimization Strategy\n\n"
            "1. **Quantify Your Achievements:** Use Google's XYZ formula: *'Accomplished [X] as measured by [Y] by doing [Z]'*.\n"
            f"2. **Keywords & ATS Alignment:** Integrate high-demand industry skills like **{', '.join(missing[:3])}** directly into your project bullet points.\n"
            "3. **Showcase Production Deployments:** Link live apps with demo accounts and clean GitHub repositories.\n"
            "4. **Action Verbs:** Replace passive descriptions with high-impact verbs: *Architected, Spearheaded, Optimized, Engineered*."
        )
    else:
        return (
            "### 🧠 Career Mentor Insights\n\n"
            f"Hello! As your Career Mentor, here is my tailored assessment for your **{roles[0]}** track:\n\n"
            f"- **Your Core Strengths:** Strong foundational competence in **{', '.join(matched)}**.\n"
            f"- **High-Priority Growth Target:** Focus on mastering **{', '.join(missing[:3])}** over the next 4–6 weeks.\n"
            "- **Next Actionable Step:** Build an end-to-end full-stack capstone featuring automated testing and containerized deployment.\n\n"
            "Feel free to ask me for mock interview questions, technical deep-dives, or week-by-week roadmaps!"
        )


def ai_mentor_response(question, analysis_result=None, chat_history=None):
    if chat_history is None:
        chat_history = []

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key and st is not None and hasattr(st, "secrets"):
            api_key = st.secrets.get("OPENAI_API_KEY", "")

        if not api_key or OpenAI is None:
            return generate_offline_mentor_advice(question, analysis_result)

        model_name = os.getenv("OPENAI_MODEL")
        if not model_name and st is not None and hasattr(st, "secrets"):
            model_name = st.secrets.get("OPENAI_MODEL", "gpt-4o-mini")
        if not model_name:
            model_name = "gpt-4o-mini"

        client = OpenAI(api_key=api_key)

        context = ""
        if analysis_result:
            context = f"""
Resume Skills: {analysis_result.get("resume_skills", [])}
Matched Skills: {analysis_result.get("matched_skills", [])}
Missing Skills: {analysis_result.get("missing_skills", [])}
Employability Score: {analysis_result.get("employability_score", 0)}%
Target Roles: {analysis_result.get("job_roles", [])}
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are SkillGap AI's career mentor. Give practical, structured, "
                    "supportive career advice to college students and tech professionals. "
                    "Use markdown with bullet points and bold headers."
                )
            }
        ]

        if context:
            messages.append({"role": "system", "content": f"Student Profile Context:\n{context}"})

        for msg in chat_history[-6:]:
            role = "user" if msg.get("role") == "user" else "assistant"
            messages.append({"role": role, "content": msg.get("content", msg.get("message", ""))})

        messages.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=600,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception:
        # Seamlessly fallback to the expert offline engine so the user never encounters an error
        return generate_offline_mentor_advice(question, analysis_result)
