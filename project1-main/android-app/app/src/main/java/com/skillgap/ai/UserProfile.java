package com.skillgap.ai;

public class UserProfile {
    public String id;
    public String name;
    public String initials;
    public String targetRole;
    public String resumeText;
    public String jobDesc;

    public UserProfile(String id, String name, String initials, String targetRole, String resumeText, String jobDesc) {
        this.id = id;
        this.name = name;
        this.initials = initials;
        this.targetRole = targetRole;
        this.resumeText = resumeText;
        this.jobDesc = jobDesc;
    }

    public static UserProfile getDemoProfile() {
        return new UserProfile(
                "demo",
                "Demo User",
                "DU",
                "Full Stack Developer",
                SkillEngine.PRESET_FULLSTACK_RESUME,
                SkillEngine.PRESET_FULLSTACK_JD
        );
    }

    public static UserProfile getAlexProfile() {
        return new UserProfile(
                "alex",
                "Alex Rivera",
                "AR",
                "Frontend Engineer",
                SkillEngine.PRESET_FRONTEND_RESUME,
                SkillEngine.PRESET_FRONTEND_JD
        );
    }

    public static UserProfile getPriyaProfile() {
        return new UserProfile(
                "priya",
                "Priya Sharma",
                "PS",
                "Machine Learning Engineer",
                SkillEngine.PRESET_AI_RESUME,
                SkillEngine.PRESET_AI_JD
        );
    }
}
