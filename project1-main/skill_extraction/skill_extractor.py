"""
Skill Extraction Engine
Extracts technical and domain skills from candidate resumes and job descriptions.
"""
import re
from backend import extract_skills, SKILLS, normalize_text

__all__ = ["extract_skills", "SKILLS", "normalize_text"]
