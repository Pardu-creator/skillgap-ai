package com.skillgap.ai;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

/**
 * Client-side skill extraction engine ported from the web app's JavaScript.
 * Contains skill taxonomy, role blueprints, learning resources, and analysis logic.
 */
public class SkillEngine {

    // ─── Skill Taxonomy ───────────────────────────────────────
    public static final String[] SKILL_DATABASE = {
        "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "HTML", "CSS",
        "React", "Next.js", "Angular", "Vue", "Node.js", "Express.js", "Bootstrap",
        "Tailwind CSS", "Django", "Flask", "FastAPI", "Streamlit",
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "Firebase", "Redis",
        "Data Science", "Data Analysis", "Machine Learning", "Deep Learning",
        "Artificial Intelligence", "Statistics", "NumPy", "Pandas", "Matplotlib",
        "Seaborn", "Scikit-Learn", "TensorFlow", "Keras", "PyTorch", "OpenCV", "NLP",
        "Computer Vision", "LLMs", "LangChain", "Prompt Engineering", "Power BI", "Tableau", "Excel",
        "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins",
        "Git", "GitHub", "GitLab", "Linux", "CI/CD", "Terraform", "Serverless",
        "Data Structures", "Algorithms", "OOP", "System Design", "REST API",
        "GraphQL", "Microservices", "Unit Testing", "Debugging", "Appium", "Selenium",
        "Cyber Security", "Network Security", "Ethical Hacking", "Cryptography", "OAuth",
        "Communication", "Leadership", "Problem Solving", "Teamwork", "Critical Thinking", "Agile",
        "Spring Boot", "Rust", "Go", "Swift", "Kotlin", "R", "MATLAB", "Scala",
        "Apache Spark", "Hadoop", "Kafka", "RabbitMQ", "Nginx", "Figma", "Jira",
        "Scrum", "DevOps", "Blockchain", "Web3", "Solidity", "React Native", "Flutter"
    };

    // ─── Role Blueprints ──────────────────────────────────────
    public static final Map<String, String[]> ROLE_BLUEPRINTS = new HashMap<>();
    static {
        ROLE_BLUEPRINTS.put("Full Stack Developer", new String[]{"JavaScript", "TypeScript", "React", "Node.js", "SQL", "MongoDB", "REST API", "Git", "HTML", "CSS", "Docker"});
        ROLE_BLUEPRINTS.put("Frontend Engineer", new String[]{"JavaScript", "TypeScript", "React", "Next.js", "HTML", "CSS", "Tailwind CSS", "Git", "REST API", "Unit Testing"});
        ROLE_BLUEPRINTS.put("Backend Engineer", new String[]{"Python", "Java", "Node.js", "FastAPI", "SQL", "PostgreSQL", "Redis", "Docker", "REST API", "System Design"});
        ROLE_BLUEPRINTS.put("Machine Learning Engineer", new String[]{"Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NumPy", "Pandas", "Scikit-Learn", "SQL", "Docker"});
        ROLE_BLUEPRINTS.put("Data Scientist / Analyst", new String[]{"Python", "SQL", "Data Analysis", "Statistics", "Pandas", "NumPy", "Power BI", "Tableau", "Excel", "Machine Learning"});
        ROLE_BLUEPRINTS.put("Cloud & DevOps Engineer", new String[]{"AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Terraform", "Git", "Azure", "Serverless", "Jenkins"});
        ROLE_BLUEPRINTS.put("Cyber Security Analyst", new String[]{"Cyber Security", "Network Security", "Ethical Hacking", "Linux", "Cryptography", "Python", "OAuth"});
        ROLE_BLUEPRINTS.put("Mobile App Developer", new String[]{"React Native", "Flutter", "Kotlin", "Swift", "Firebase", "REST API", "Git", "JavaScript"});
        ROLE_BLUEPRINTS.put("AI/LLM Engineer", new String[]{"Python", "LLMs", "LangChain", "Prompt Engineering", "NLP", "Deep Learning", "FastAPI", "Docker", "Git"});
    }

    // ─── Learning Resources ──────────────────────────────────
    public static final Map<String, String> LEARNING_COURSES = new HashMap<>();
    static {
        LEARNING_COURSES.put("Python", "Python for Everybody (Coursera) & Python Crash Course");
        LEARNING_COURSES.put("JavaScript", "The Complete JavaScript Course (Udemy / MDN Web Docs)");
        LEARNING_COURSES.put("TypeScript", "TypeScript Handbook & Total TypeScript");
        LEARNING_COURSES.put("React", "Full Modern React 19 Tutorial & Epic React");
        LEARNING_COURSES.put("Node.js", "Node.js Developer Course & Official Node Docs");
        LEARNING_COURSES.put("SQL", "SQL for Data Science (Coursera) & LeetCode Database 50");
        LEARNING_COURSES.put("Docker", "Docker Mastery on Udemy & Docker Getting Started Guide");
        LEARNING_COURSES.put("Kubernetes", "Kubernetes for Developers & CKAD Bootcamp");
        LEARNING_COURSES.put("AWS", "AWS Certified Solutions Architect Associate (Stephane Maarek)");
        LEARNING_COURSES.put("Machine Learning", "Machine Learning Specialization by Andrew Ng (Coursera)");
        LEARNING_COURSES.put("Deep Learning", "Deep Learning Specialization by deeplearning.ai");
        LEARNING_COURSES.put("FastAPI", "FastAPI Full Course & Official Test-Driven FastAPI Guide");
        LEARNING_COURSES.put("Git", "Pro Git Book & GitHub Skills Lab");
        LEARNING_COURSES.put("System Design", "Grokking System Design & System Design Primer on GitHub");
        LEARNING_COURSES.put("LLMs", "LangChain + Hugging Face NLP Course");
        LEARNING_COURSES.put("Next.js", "Next.js Official Learn Course & Vercel Docs");
    }

    // ─── Preset Profiles ─────────────────────────────────────
    public static final String PRESET_FRONTEND_RESUME = "ALEX RIVERA\nFrontend Developer\nEmail: alex@example.com | Portfolio: alexrivera.dev\n\nSKILLS:\nJavaScript, TypeScript, React, HTML5, CSS3, Tailwind CSS, Git, GitHub, REST APIs, Redux, Responsive Web Design\n\nEXPERIENCE:\nFrontend Developer at TechNova (2023 - Present)\n- Built responsive single-page web applications using React and TypeScript.\n- Integrated RESTful APIs and optimized web performance achieving 95+ Lighthouse scores.\n- Collaborated with UX designers and backend engineers in an Agile sprint environment.\n\nPROJECTS:\n- E-Commerce Web Platform: React, Redux Toolkit, Tailwind CSS\n- Analytics Dashboard: Chart.js, TypeScript, REST API\n\nEDUCATION:\nB.Tech in Computer Science - 8.5 CGPA";
    public static final String PRESET_FRONTEND_JD = "Looking for a Senior Frontend Engineer proficient in JavaScript, TypeScript, React, Next.js, HTML, CSS, Tailwind CSS, GraphQL, Unit Testing, and Git. Experience with Web Performance, Microservices, and CI/CD pipelines is a plus.";

    public static final String PRESET_AI_RESUME = "PRIYA SHARMA\nAI & Data Science Specialist\n\nSKILLS:\nPython, Machine Learning, Deep Learning, TensorFlow, PyTorch, Pandas, NumPy, Scikit-Learn, SQL, Data Analysis, Matplotlib, Git\n\nEXPERIENCE:\nData Scientist Intern at Apex AI (2024)\n- Developed deep learning models for classification with 94% accuracy.\n- Extracted and cleaned tabular datasets using Pandas and SQL queries.\n- Fine-tuned transformer models for sentiment analysis.\n\nPROJECTS:\n- Sentiment Analyzer: Built NLP pipeline with 91% accuracy using BERT\n- Image Classifier: CNN model with TensorFlow, deployed on Flask\n\nEDUCATION:\nM.Tech in AI & ML - 9.1 CGPA";
    public static final String PRESET_AI_JD = "We are hiring a Machine Learning Engineer with strong experience in Python, PyTorch, TensorFlow, LLMs, NLP, LangChain, Docker, AWS, FastAPI, and SQL. You will build and deploy production ML microservices.";

    public static final String PRESET_FULLSTACK_RESUME = "JORDAN LEE\nSoftware Engineer\n\nSKILLS:\nPython, Django, JavaScript, React, Node.js, Express.js, PostgreSQL, MongoDB, Docker, Git, REST API, Linux\n\nEXPERIENCE:\nFull Stack Engineer at CloudCraft (2022 - Present)\n- Developed full stack web applications with React and Node.js/PostgreSQL.\n- Designed REST APIs and deployed containerized services using Docker and Git.\n- Mentored 3 junior developers and led code review sessions.\n\nPROJECTS:\n- Task Management SaaS: React, Node.js, MongoDB, JWT Auth\n- Real-time Chat App: Socket.io, Express, Redis\n\nEDUCATION:\nB.Sc. Computer Science - 3.8 GPA";
    public static final String PRESET_FULLSTACK_JD = "Seeking a Full Stack Developer experienced in TypeScript, React, Next.js, Node.js, Express.js, PostgreSQL, Redis, Docker, Kubernetes, AWS, and System Design.";

    // ─── Analysis Methods ─────────────────────────────────────

    public static String normalize(String text) {
        return text.toLowerCase()
                .replaceAll("[-_]", " ")
                .replaceAll("[^a-z0-9+#. ]", " ")
                .replaceAll("\\s+", " ")
                .trim();
    }

    public static List<String> extractSkills(String text) {
        String norm = normalize(text);
        Set<String> found = new LinkedHashSet<>();
        for (String skill : SKILL_DATABASE) {
            String skillNorm = normalize(skill);
            String regex = "\\b" + Pattern.quote(skillNorm) + "\\b";
            if (Pattern.compile(regex, Pattern.CASE_INSENSITIVE).matcher(norm).find()) {
                found.add(skill);
            }
        }
        List<String> result = new ArrayList<>(found);
        Collections.sort(result);
        return result;
    }

    public static List<String> suggestRoles(List<String> skills) {
        List<String> sLower = new ArrayList<>();
        for (String s : skills) sLower.add(s.toLowerCase());

        List<Map.Entry<String, Integer>> suggestions = new ArrayList<>();
        for (Map.Entry<String, String[]> entry : ROLE_BLUEPRINTS.entrySet()) {
            int hits = 0;
            for (String req : entry.getValue()) {
                if (sLower.contains(req.toLowerCase())) hits++;
            }
            if (hits >= 2) {
                Map<String, Integer> map = new HashMap<>();
                map.put(entry.getKey(), hits);
                suggestions.add(map.entrySet().iterator().next());
            }
        }

        suggestions.sort((a, b) -> b.getValue() - a.getValue());

        List<String> result = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : suggestions) {
            result.add(entry.getKey());
        }

        if (result.isEmpty()) {
            result.add("Software Developer Trainee");
            result.add("Junior Web Developer");
        }
        return result;
    }

    public static AnalysisResult analyze(String resumeText, String jdText) {
        List<String> resumeSkills = extractSkills(resumeText);

        List<String> requiredSkills;
        if (jdText != null && !jdText.trim().isEmpty()) {
            requiredSkills = extractSkills(jdText);
        } else {
            requiredSkills = new ArrayList<>();
        }

        if (requiredSkills.isEmpty()) {
            requiredSkills = Arrays.asList("JavaScript", "TypeScript", "React", "Node.js", "SQL", "Git", "REST API", "Docker");
        }

        List<String> matched = new ArrayList<>();
        List<String> missing = new ArrayList<>();
        List<String> extra = new ArrayList<>();

        for (String s : requiredSkills) {
            boolean found = false;
            for (String rs : resumeSkills) {
                if (rs.equalsIgnoreCase(s)) { found = true; break; }
            }
            if (found) matched.add(s);
            else missing.add(s);
        }

        for (String s : resumeSkills) {
            boolean found = false;
            for (String rs : requiredSkills) {
                if (rs.equalsIgnoreCase(s)) { found = true; break; }
            }
            if (!found) extra.add(s);
        }

        int matchScore = requiredSkills.size() > 0 ? Math.round((float) matched.size() / requiredSkills.size() * 100) : 0;
        int skillWeight = Math.min(resumeSkills.size() * 5, 40);
        int matchWeight = Math.round(matchScore * 0.45f);
        int bonusWeight = matched.size() >= 4 ? 15 : (matched.size() * 3);
        int employabilityScore = Math.min(skillWeight + matchWeight + bonusWeight, 100);

        List<String> roles = suggestRoles(resumeSkills);

        AnalysisResult result = new AnalysisResult();
        result.resumeSkills = resumeSkills;
        result.jdSkills = requiredSkills;
        result.matched = matched;
        result.missing = missing;
        result.extra = extra;
        result.matchScore = matchScore;
        result.employabilityScore = employabilityScore;
        result.roles = roles;
        return result;
    }

    public static String getResource(String skill) {
        String resource = LEARNING_COURSES.get(skill);
        return resource != null ? resource : "Search for top-rated courses on Coursera/Udemy";
    }
}
