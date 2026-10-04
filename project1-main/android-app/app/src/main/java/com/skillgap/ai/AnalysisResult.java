package com.skillgap.ai;

import java.util.ArrayList;
import java.util.List;

/**
 * Data model for skill gap analysis results.
 * Shared between Analyzer, Roadmap, and Chat fragments.
 */
public class AnalysisResult {
    public List<String> resumeSkills = new ArrayList<>();
    public List<String> jdSkills = new ArrayList<>();
    public List<String> matched = new ArrayList<>();
    public List<String> missing = new ArrayList<>();
    public List<String> extra = new ArrayList<>();
    public List<String> roles = new ArrayList<>();
    public List<String> suggestedRoles = new ArrayList<>();
    public int matchScore;
    public int breadthScore;
    public int employabilityScore;

    // AI Feedback fields
    public String aiVerdict = "";
    public int atsScore;
    public List<String> strengths = new ArrayList<>();
    public List<String> improvements = new ArrayList<>();
    public List<String> atsTips = new ArrayList<>();
    public List<String> interviewTopics = new ArrayList<>();
}
