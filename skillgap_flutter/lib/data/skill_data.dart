// SkillGap AI — static data layer.
// Ported from the original web app's app.js skill taxonomy, role blueprints,
// learning courses and sample candidate presets.

const List<String> kSkillDatabase = [
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
  "Scrum", "DevOps", "Blockchain", "Web3", "Solidity", "React Native", "Flutter",
];

/// Required skills per career role.
const Map<String, List<String>> kRoleBlueprints = {
  "Full Stack Developer": [
    "JavaScript", "TypeScript", "React", "Node.js", "SQL", "MongoDB",
    "REST API", "Git", "HTML", "CSS", "Docker",
  ],
  "Frontend Engineer": [
    "JavaScript", "TypeScript", "React", "Next.js", "HTML", "CSS",
    "Tailwind CSS", "Git", "REST API", "Unit Testing",
  ],
  "Backend Engineer": [
    "Python", "Java", "Node.js", "FastAPI", "SQL", "PostgreSQL",
    "Redis", "Docker", "REST API", "System Design",
  ],
  "Machine Learning Engineer": [
    "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "NumPy", "Pandas", "Scikit-Learn", "SQL", "Docker",
  ],
  "Data Scientist / Analyst": [
    "Python", "SQL", "Data Analysis", "Statistics", "Pandas", "NumPy",
    "Power BI", "Tableau", "Excel", "Machine Learning",
  ],
  "Cloud & DevOps Engineer": [
    "AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Terraform",
    "Git", "Azure", "Serverless", "Jenkins",
  ],
  "Cyber Security Analyst": [
    "Cyber Security", "Network Security", "Ethical Hacking", "Linux",
    "Cryptography", "Python", "OAuth",
  ],
  "Mobile App Developer": [
    "React Native", "Flutter", "Kotlin", "Swift", "Firebase",
    "REST API", "Git", "JavaScript",
  ],
  "AI/LLM Engineer": [
    "Python", "LLMs", "LangChain", "Prompt Engineering", "NLP",
    "Deep Learning", "FastAPI", "Docker", "Git",
  ],
};

/// Estimated compensation per role (USD, market intelligence snapshot).
const Map<String, String> kRoleSalaries = {
  "Full Stack Developer": "\$95k - \$140k",
  "Frontend Engineer": "\$90k - \$135k",
  "Backend Engineer": "\$100k - \$150k",
  "Machine Learning Engineer": "\$120k - \$175k",
  "Data Scientist / Analyst": "\$95k - \$145k",
  "Cloud & DevOps Engineer": "\$110k - \$160k",
  "Cyber Security Analyst": "\$90k - \$140k",
  "Mobile App Developer": "\$85k - \$130k",
  "AI/LLM Engineer": "\$130k - \$190k",
};

/// Recommended learning resources per skill.
const Map<String, String> kLearningCourses = {
  "Python": "Python for Everybody (Coursera) & Python Crash Course",
  "JavaScript": "The Complete JavaScript Course (Udemy / MDN Web Docs)",
  "TypeScript": "TypeScript Handbook & Total TypeScript",
  "React": "Full Modern React Tutorial & Epic React",
  "Node.js": "Node.js Developer Course & Official Node Docs",
  "SQL": "SQL for Data Science (Coursera) & LeetCode Database 50",
  "Docker": "Docker Mastery on Udemy & Docker Getting Started Guide",
  "Kubernetes": "Kubernetes for Developers & CKAD Bootcamp",
  "AWS": "AWS Certified Solutions Architect Associate (Stephane Maarek)",
  "Machine Learning": "Machine Learning Specialization by Andrew Ng (Coursera)",
  "Deep Learning": "Deep Learning Specialization by deeplearning.ai",
  "FastAPI": "FastAPI Full Course & Official Test-Driven FastAPI Guide",
  "Git": "Pro Git Book & GitHub Skills Lab",
  "System Design": "Grokking System Design & System Design Primer on GitHub",
  "LLMs": "LangChain + Hugging Face NLP Course",
  "Next.js": "Next.js Official Learn Course & Vercel Docs",
};

/// Fallback required skills when no job description is provided.
const List<String> kDefaultRequiredSkills = [
  "JavaScript", "TypeScript", "React", "Node.js", "SQL", "Git", "REST API", "Docker",
];

/// Job description templates shown in the Analyzer template dropdown.
const Map<String, String> kRoleTemplates = {
  "fullstack": "Seeking a Full Stack Engineer experienced in JavaScript, TypeScript, React, Node.js, SQL, MongoDB, REST API, Docker, and Git.",
  "frontend": "Looking for a Frontend Engineer proficient in JavaScript, TypeScript, React, Next.js, HTML, CSS, Tailwind CSS, REST API, and Unit Testing.",
  "backend": "Hiring a Backend Engineer with strong experience in Python, FastAPI, PostgreSQL, Docker, Redis, REST API, and System Design.",
  "ml": "We are hiring a Machine Learning Engineer with strong experience in Python, PyTorch, TensorFlow, LLMs, NLP, LangChain, Docker, AWS, FastAPI, and SQL.",
  "devops": "Seeking a DevOps & Cloud Engineer skilled in AWS, Kubernetes, Docker, CI/CD, Terraform, Linux, Jenkins, and Git.",
};

const List<String> kTargetRoles = [
  "Full Stack Developer",
  "Frontend Engineer",
  "Backend Engineer",
  "Machine Learning Engineer",
  "Data Scientist / Analyst",
  "Cloud & DevOps Engineer",
  "Cyber Security Analyst",
  "Mobile App Developer",
  "AI/LLM Engineer",
];

const List<String> kExperienceLevels = [
  "Undergraduate / Fresher",
  "Junior (1 - 2 Years)",
  "Mid-Level (3 - 5 Years)",
  "Senior (5+ Years)",
];

/// Sample candidate presets (resume text + matching job description).
class SamplePreset {
  final String key;
  final String label;
  final String resume;
  final String jd;
  const SamplePreset(this.key, this.label, this.resume, this.jd);
}

const List<SamplePreset> kSamplePresets = [
  SamplePreset(
    "frontend",
    "Frontend Dev",
    "ALEX RIVERA\nFrontend Developer\nEmail: alex@example.com | Portfolio: alexrivera.dev\n\nSKILLS:\nJavaScript, TypeScript, React, HTML5, CSS3, Tailwind CSS, Git, GitHub, REST APIs, Redux, Responsive Web Design\n\nEXPERIENCE:\nFrontend Developer at TechNova (2023 - Present)\n- Built responsive single-page web applications using React and TypeScript.\n- Integrated RESTful APIs and optimized web performance achieving 95+ Lighthouse scores.\n- Collaborated with UX designers and backend engineers in an Agile sprint environment.\n\nPROJECTS:\n- E-Commerce Web Platform: React, Redux Toolkit, Tailwind CSS\n- Analytics Dashboard: Chart.js, TypeScript, REST API\n\nEDUCATION:\nB.Tech in Computer Science - 8.5 CGPA",
    "Looking for a Senior Frontend Engineer proficient in JavaScript, TypeScript, React, Next.js, HTML, CSS, Tailwind CSS, GraphQL, Unit Testing, and Git. Experience with Web Performance, Microservices, and CI/CD pipelines is a plus.",
  ),
  SamplePreset(
    "ai",
    "AI & ML Engineer",
    "PRIYA SHARMA\nAI & Data Science Specialist\n\nSKILLS:\nPython, Machine Learning, Deep Learning, TensorFlow, PyTorch, Pandas, NumPy, Scikit-Learn, SQL, Data Analysis, Matplotlib, Git\n\nEXPERIENCE:\nData Scientist Intern at Apex AI (2024)\n- Developed deep learning models for classification with 94% accuracy.\n- Extracted and cleaned tabular datasets using Pandas and SQL queries.\n- Fine-tuned transformer models for sentiment analysis.\n\nPROJECTS:\n- Sentiment Analyzer: Built NLP pipeline with 91% accuracy using BERT\n- Image Classifier: CNN model with TensorFlow, deployed on Flask\n\nEDUCATION:\nM.Tech in AI & ML - 9.1 CGPA",
    "We are hiring a Machine Learning Engineer with strong experience in Python, PyTorch, TensorFlow, LLMs, NLP, LangChain, Docker, AWS, FastAPI, and SQL. You will build and deploy production ML microservices.",
  ),
  SamplePreset(
    "fullstack",
    "Full Stack Dev",
    "JORDAN LEE\nSoftware Engineer\n\nSKILLS:\nPython, Django, JavaScript, React, Node.js, Express.js, PostgreSQL, MongoDB, Docker, Git, REST API, Linux\n\nEXPERIENCE:\nFull Stack Engineer at CloudCraft (2022 - Present)\n- Developed full stack web applications with React and Node.js/PostgreSQL.\n- Designed REST APIs and deployed containerized services using Docker and Git.\n- Mentored 3 junior developers and led code review sessions.\n\nPROJECTS:\n- Task Management SaaS: React, Node.js, MongoDB, JWT Auth\n- Real-time Chat App: Socket.io, Express, Redis\n\nEDUCATION:\nB.Sc. Computer Science - 3.8 GPA",
    "Seeking a Full Stack Developer experienced in TypeScript, React, Next.js, Node.js, Express.js, PostgreSQL, Redis, Docker, Kubernetes, AWS, and System Design.",
  ),
];

/// Demo accounts seeded into the local auth store.
class DemoAccount {
  final String email;
  final String password;
  final String fullName;
  final String targetRole;
  final String role;
  const DemoAccount(this.email, this.password, this.fullName, this.targetRole, this.role);
}

const List<DemoAccount> kDemoAccounts = [
  DemoAccount("demo@skillgap.ai", "Password123!", "Demo Student", "Full Stack Developer", "Student"),
  DemoAccount("alex@skillgap.ai", "Password123!", "Alex Rivera", "Frontend Engineer", "Professional"),
  DemoAccount("priya@skillgap.ai", "Password123!", "Priya Sharma", "Machine Learning Engineer", "Researcher"),
];
