/**
 * SkillGap AI - Full Engine with Real Gemini AI Integration
 * Client-side analysis + Serverless AI Mentor + AI Resume Feedback
 */

// ─── Skill Taxonomy ───────────────────────────────────────────
const SKILL_DATABASE = [
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
];

// ─── Role Blueprints ──────────────────────────────────────────
const ROLE_BLUEPRINTS = {
  "Full Stack Developer": ["JavaScript", "TypeScript", "React", "Node.js", "SQL", "MongoDB", "REST API", "Git", "HTML", "CSS", "Docker"],
  "Frontend Engineer": ["JavaScript", "TypeScript", "React", "Next.js", "HTML", "CSS", "Tailwind CSS", "Git", "REST API", "Unit Testing"],
  "Backend Engineer": ["Python", "Java", "Node.js", "FastAPI", "SQL", "PostgreSQL", "Redis", "Docker", "REST API", "System Design"],
  "Machine Learning Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NumPy", "Pandas", "Scikit-Learn", "SQL", "Docker"],
  "Data Scientist / Analyst": ["Python", "SQL", "Data Analysis", "Statistics", "Pandas", "NumPy", "Power BI", "Tableau", "Excel", "Machine Learning"],
  "Cloud & DevOps Engineer": ["AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Terraform", "Git", "Azure", "Serverless", "Jenkins"],
  "Cyber Security Analyst": ["Cyber Security", "Network Security", "Ethical Hacking", "Linux", "Cryptography", "Python", "OAuth"],
  "Mobile App Developer": ["React Native", "Flutter", "Kotlin", "Swift", "Firebase", "REST API", "Git", "JavaScript"],
  "AI/LLM Engineer": ["Python", "LLMs", "LangChain", "Prompt Engineering", "NLP", "Deep Learning", "FastAPI", "Docker", "Git"]
};

// ─── Learning Resources ──────────────────────────────────────
const LEARNING_COURSES = {
  "Python": "Python for Everybody (Coursera) & Python Crash Course",
  "JavaScript": "The Complete JavaScript Course (Udemy / MDN Web Docs)",
  "TypeScript": "TypeScript Handbook & Total TypeScript",
  "React": "Full Modern React 19 Tutorial & Epic React",
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
  "Next.js": "Next.js Official Learn Course & Vercel Docs"
};

// ─── Sample Presets ───────────────────────────────────────────
const PRESETS = {
  frontend: {
    resume: `ALEX RIVERA\nFrontend Developer\nEmail: alex@example.com | Portfolio: alexrivera.dev\n\nSKILLS:\nJavaScript, TypeScript, React, HTML5, CSS3, Tailwind CSS, Git, GitHub, REST APIs, Redux, Responsive Web Design\n\nEXPERIENCE:\nFrontend Developer at TechNova (2023 - Present)\n- Built responsive single-page web applications using React and TypeScript.\n- Integrated RESTful APIs and optimized web performance achieving 95+ Lighthouse scores.\n- Collaborated with UX designers and backend engineers in an Agile sprint environment.\n\nPROJECTS:\n- E-Commerce Web Platform: React, Redux Toolkit, Tailwind CSS\n- Analytics Dashboard: Chart.js, TypeScript, REST API\n\nEDUCATION:\nB.Tech in Computer Science - 8.5 CGPA`,
    jd: `Looking for a Senior Frontend Engineer proficient in JavaScript, TypeScript, React, Next.js, HTML, CSS, Tailwind CSS, GraphQL, Unit Testing, and Git. Experience with Web Performance, Microservices, and CI/CD pipelines is a plus.`
  },
  ai: {
    resume: `PRIYA SHARMA\nAI & Data Science Specialist\n\nSKILLS:\nPython, Machine Learning, Deep Learning, TensorFlow, PyTorch, Pandas, NumPy, Scikit-Learn, SQL, Data Analysis, Matplotlib, Git\n\nEXPERIENCE:\nData Scientist Intern at Apex AI (2024)\n- Developed deep learning models for classification with 94% accuracy.\n- Extracted and cleaned tabular datasets using Pandas and SQL queries.\n- Fine-tuned transformer models for sentiment analysis.\n\nPROJECTS:\n- Sentiment Analyzer: Built NLP pipeline with 91% accuracy using BERT\n- Image Classifier: CNN model with TensorFlow, deployed on Flask\n\nEDUCATION:\nM.Tech in AI & ML - 9.1 CGPA`,
    jd: `We are hiring a Machine Learning Engineer with strong experience in Python, PyTorch, TensorFlow, LLMs, NLP, LangChain, Docker, AWS, FastAPI, and SQL. You will build and deploy production ML microservices.`
  },
  fullstack: {
    resume: `JORDAN LEE\nSoftware Engineer\n\nSKILLS:\nPython, Django, JavaScript, React, Node.js, Express.js, PostgreSQL, MongoDB, Docker, Git, REST API, Linux\n\nEXPERIENCE:\nFull Stack Engineer at CloudCraft (2022 - Present)\n- Developed full stack web applications with React and Node.js/PostgreSQL.\n- Designed REST APIs and deployed containerized services using Docker and Git.\n- Mentored 3 junior developers and led code review sessions.\n\nPROJECTS:\n- Task Management SaaS: React, Node.js, MongoDB, JWT Auth\n- Real-time Chat App: Socket.io, Express, Redis\n\nEDUCATION:\nB.Sc. Computer Science - 3.8 GPA`,
    jd: `Seeking a Full Stack Developer experienced in TypeScript, React, Next.js, Node.js, Express.js, PostgreSQL, Redis, Docker, Kubernetes, AWS, and System Design.`
  }
};

// ─── State ────────────────────────────────────────────────────
let currentAnalysis = null;

// ─── Init ─────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupPresets();
  setupDragAndDrop();
  setupForm();
  setupChat();
});

// ─── Tab Switcher ─────────────────────────────────────────────
function setupTabs() {
  const tabBtns = document.querySelectorAll(".nav-tab-btn");
  const panels = document.querySelectorAll(".tab-content-panel");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      panels.forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add("active");
    });
  });
}

// ─── Presets ──────────────────────────────────────────────────
function setupPresets() {
  const chips = document.querySelectorAll(".preset-chips .chip-btn");
  const resumeTextarea = document.getElementById("resumeText");
  const jdTextarea = document.getElementById("jobDesc");

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      const presetKey = chip.dataset.preset;
      if (PRESETS[presetKey]) {
        resumeTextarea.value = PRESETS[presetKey].resume;
        jdTextarea.value = PRESETS[presetKey].jd;
        document.getElementById("fileStatus").style.display = "none";
      }
    });
  });
}

// ─── Drag & Drop / PDF Upload ─────────────────────────────────
function setupDragAndDrop() {
  const zone = document.getElementById("uploadZone");
  const fileInput = document.getElementById("resumeFile");
  const status = document.getElementById("fileStatus");
  const resumeTextarea = document.getElementById("resumeText");

  zone.addEventListener("click", () => fileInput.click());
  zone.addEventListener("dragover", (e) => { e.preventDefault(); zone.classList.add("dragover"); });
  zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
  zone.addEventListener("drop", (e) => {
    e.preventDefault();
    zone.classList.remove("dragover");
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) handleFile(fileInput.files[0]);
  });

  async function handleFile(file) {
    status.style.display = "flex";
    status.innerHTML = `⏳ Reading <b>${file.name}</b>...`;
    if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
      try {
        const text = await extractTextFromPdf(file);
        resumeTextarea.value = text;
        status.innerHTML = `✅ Extracted text from <b>${file.name}</b> (${Math.round(file.size / 1024)} KB)`;
      } catch (err) {
        status.innerHTML = `⚠️ Could not parse PDF. Please paste text manually.`;
      }
    } else {
      const reader = new FileReader();
      reader.onload = (e) => {
        resumeTextarea.value = e.target.result;
        status.innerHTML = `✅ Loaded <b>${file.name}</b>`;
      };
      reader.readAsText(file);
    }
  }
}

async function extractTextFromPdf(file) {
  const arrayBuffer = await file.arrayBuffer();
  if (window.pdfjsLib) {
    const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let fullText = "";
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      fullText += textContent.items.map(item => item.str).join(" ") + "\n";
    }
    return fullText;
  }
  const decoder = new TextDecoder("utf-8");
  return decoder.decode(arrayBuffer).replace(/[^\x20-\x7E\n]/g, " ").replace(/\s+/g, " ");
}

// ─── Analysis Engine ──────────────────────────────────────────
function setupForm() {
  document.getElementById("analyzeBtn").addEventListener("click", performAnalysis);
}

function normalize(text) {
  return text.toLowerCase().replace(/[-_]/g, " ").replace(/[^a-z0-9+#. ]/g, " ").replace(/\s+/g, " ").trim();
}

function extractSkills(text) {
  const norm = normalize(text);
  const found = [];
  SKILL_DATABASE.forEach(skill => {
    const regex = new RegExp(`\\b${escapeRegExp(normalize(skill))}\\b`, "i");
    if (regex.test(norm)) found.push(skill);
  });
  return [...new Set(found)].sort();
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

async function performAnalysis() {
  const resumeText = document.getElementById("resumeText").value.trim();
  const jdText = document.getElementById("jobDesc").value.trim();

  if (!resumeText) {
    alert("Please upload a resume or paste your resume text to begin analysis.");
    return;
  }

  // Show loading state
  const analyzeBtn = document.getElementById("analyzeBtn");
  const originalBtnText = analyzeBtn.innerHTML;
  analyzeBtn.innerHTML = `<span class="btn-spinner"></span> Analyzing with AI...`;
  analyzeBtn.disabled = true;

  const resumeSkills = extractSkills(resumeText);
  let requiredSkills = jdText ? extractSkills(jdText) : [];
  if (requiredSkills.length === 0) {
    requiredSkills = ["JavaScript", "TypeScript", "React", "Node.js", "SQL", "Git", "REST API", "Docker"];
  }

  const matched = requiredSkills.filter(s => resumeSkills.some(rs => rs.toLowerCase() === s.toLowerCase()));
  const missing = requiredSkills.filter(s => !resumeSkills.some(rs => rs.toLowerCase() === s.toLowerCase()));
  const extra = resumeSkills.filter(s => !requiredSkills.some(rs => rs.toLowerCase() === s.toLowerCase()));

  const matchScore = requiredSkills.length > 0 ? Math.round((matched.length / requiredSkills.length) * 100) : 0;
  let skillWeight = Math.min(resumeSkills.length * 5, 40);
  let matchWeight = Math.round(matchScore * 0.45);
  let bonusWeight = matched.length >= 4 ? 15 : (matched.length * 3);
  let employabilityScore = Math.min(Math.round(skillWeight + matchWeight + bonusWeight), 100);

  const roles = suggestRoles(resumeSkills);

  currentAnalysis = { resumeSkills, requiredSkills, matched, missing, extra, matchScore, employabilityScore, roles };

  renderResults(currentAnalysis);

  // Now call AI for deep feedback (async, non-blocking)
  fetchAIFeedback(resumeText, jdText, currentAnalysis);

  // Restore button
  analyzeBtn.innerHTML = originalBtnText;
  analyzeBtn.disabled = false;
  // Re-init lucide icons for the button
  if (window.lucide) window.lucide.createIcons();
}

function suggestRoles(skills) {
  const sLower = skills.map(s => s.toLowerCase());
  const suggestions = [];
  for (const [role, reqs] of Object.entries(ROLE_BLUEPRINTS)) {
    const hits = reqs.filter(r => sLower.includes(r.toLowerCase())).length;
    if (hits >= 2) suggestions.push({ role, count: hits });
  }
  suggestions.sort((a, b) => b.count - a.count);
  return suggestions.length > 0 ? suggestions.map(s => s.role) : ["Software Developer Trainee", "Junior Web Developer"];
}

// ─── AI Feedback (Gemini) ─────────────────────────────────────
async function fetchAIFeedback(resumeText, jobDesc, analysis) {
  const feedbackEl = document.getElementById("aiFeedbackContainer");
  const loadingEl = document.getElementById("aiFeedbackLoading");
  const contentEl = document.getElementById("aiFeedbackContent");

  feedbackEl.style.display = "block";
  loadingEl.style.display = "flex";
  contentEl.style.display = "none";
  contentEl.innerHTML = "";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resumeText,
        jobDesc,
        matched: analysis.matched,
        missing: analysis.missing,
        extra: analysis.extra,
        matchScore: analysis.matchScore,
        employabilityScore: analysis.employabilityScore,
        roles: analysis.roles
      })
    });

    if (!res.ok) throw new Error("API error");
    const data = await res.json();

    loadingEl.style.display = "none";
    contentEl.style.display = "block";
    renderAIFeedback(contentEl, data);

  } catch (err) {
    console.warn("AI feedback failed, using fallback:", err);
    loadingEl.style.display = "none";
    contentEl.style.display = "block";
    renderFallbackFeedback(contentEl, analysis);
  }
}

function renderAIFeedback(container, data) {
  const atsScore = data.atsScore || 50;
  const atsColor = atsScore >= 75 ? "var(--accent-emerald)" : atsScore >= 50 ? "var(--accent-amber)" : "var(--accent-rose)";

  container.innerHTML = `
    <div class="ai-verdict">
      <div class="verdict-icon">🤖</div>
      <div class="verdict-text">
        <h4>AI Verdict</h4>
        <p>${data.overallVerdict || "Analysis complete — check details below."}</p>
      </div>
      <div class="ats-badge" style="border-color: ${atsColor}; color: ${atsColor};">
        <span class="ats-score-num">${atsScore}</span>
        <span class="ats-label">ATS</span>
      </div>
    </div>

    ${data.resumeStrengths && data.resumeStrengths.length > 0 ? `
    <div class="feedback-section">
      <h5><span class="fb-icon">💪</span> Strengths</h5>
      <ul>${data.resumeStrengths.map(s => `<li>${s}</li>`).join("")}</ul>
    </div>` : ""}

    ${data.criticalImprovements && data.criticalImprovements.length > 0 ? `
    <div class="feedback-section improvements">
      <h5><span class="fb-icon">🎯</span> Critical Improvements</h5>
      <ul>${data.criticalImprovements.map(s => `<li>${s}</li>`).join("")}</ul>
    </div>` : ""}

    ${data.atsTips && data.atsTips.length > 0 ? `
    <div class="feedback-section ats-tips">
      <h5><span class="fb-icon">📋</span> ATS Optimization Tips</h5>
      <ul>${data.atsTips.map(s => `<li>${s}</li>`).join("")}</ul>
    </div>` : ""}

    ${data.interviewTopics && data.interviewTopics.length > 0 ? `
    <div class="feedback-section">
      <h5><span class="fb-icon">💼</span> Likely Interview Topics</h5>
      <div class="interview-tags">
        ${data.interviewTopics.map(t => `<span class="interview-tag">${t}</span>`).join("")}
      </div>
    </div>` : ""}
  `;
}

function renderFallbackFeedback(container, analysis) {
  const tips = [];
  if (analysis.missing.length > 0) tips.push(`Bridge your top skill gaps: <strong>${analysis.missing.slice(0, 3).join(", ")}</strong>`);
  tips.push("Add quantifiable metrics to your experience bullets (e.g., <em>'Improved API response time by 40%'</em>)");
  tips.push("Include links to live deployed projects and clean GitHub repos");
  if (analysis.matched.length < 5) tips.push("Consider obtaining a relevant certification to strengthen your profile");

  container.innerHTML = `
    <div class="ai-verdict">
      <div class="verdict-icon">📊</div>
      <div class="verdict-text">
        <h4>Quick Analysis</h4>
        <p>Matched ${analysis.matched.length} of ${analysis.requiredSkills.length} target skills. ${analysis.missing.length > 0 ? `Focus on bridging ${analysis.missing.length} gap${analysis.missing.length > 1 ? 's' : ''}.` : 'Great skill coverage!'}</p>
      </div>
    </div>
    <div class="feedback-section improvements">
      <h5><span class="fb-icon">🎯</span> Improvement Tips</h5>
      <ul>${tips.map(t => `<li>${t}</li>`).join("")}</ul>
    </div>
  `;
}

// ─── Render Results ───────────────────────────────────────────
function renderResults(data) {
  document.getElementById("emptyResultState").style.display = "none";
  document.getElementById("resultsContainer").style.display = "block";

  // Gauge
  const gaugeVal = document.getElementById("gaugeValue");
  const gaugeProg = document.getElementById("gaugeProgress");
  gaugeVal.textContent = `${data.employabilityScore}%`;
  const circumference = 408;
  gaugeProg.style.strokeDashoffset = circumference - (data.employabilityScore / 100) * circumference;

  // Metric Bars
  document.getElementById("matchScoreVal").textContent = `${data.matchScore}%`;
  document.getElementById("matchScoreFill").style.width = `${data.matchScore}%`;
  const breadthPct = Math.min(Math.round((data.resumeSkills.length / 15) * 100), 100);
  document.getElementById("breadthScoreVal").textContent = `${breadthPct}%`;
  document.getElementById("breadthScoreFill").style.width = `${breadthPct}%`;

  // Roles
  document.getElementById("topRoleTitle").textContent = data.roles.slice(0, 2).join(" • ");

  // Skill Tags
  renderBadges("matchedCloud", data.matched, "matched", "✓ ");
  renderBadges("missingCloud", data.missing, "missing", "✗ ");
  renderBadges("extraCloud", data.extra, "extra", "+ ");
  document.getElementById("matchedCount").textContent = `${data.matched.length} Skills`;
  document.getElementById("missingCount").textContent = `${data.missing.length} Gaps`;
  document.getElementById("extraCount").textContent = `${data.extra.length} Additional`;

  // Roadmap
  renderRoadmap(data.missing, data.roles[0]);

  // Re-init icons
  if (window.lucide) window.lucide.createIcons();

  // Scroll to results on mobile
  if (window.innerWidth < 1024) {
    document.getElementById("resultsContainer").scrollIntoView({ behavior: "smooth" });
  }
}

function renderBadges(containerId, list, typeClass, prefix) {
  const container = document.getElementById(containerId);
  if (list.length === 0) {
    container.innerHTML = `<span style="font-size:0.8rem; color:var(--text-muted);">None detected</span>`;
    return;
  }
  container.innerHTML = list.map(skill =>
    `<span class="skill-badge ${typeClass}">${prefix}${skill}</span>`
  ).join("");
}

// ─── Roadmap Timeline ─────────────────────────────────────────
function renderRoadmap(missingSkills, targetRole) {
  const container = document.getElementById("roadmapList");
  if (!container) return;

  const getResource = (skill) => LEARNING_COURSES[skill] || "Search for top-rated courses on Coursera/Udemy";

  const steps = [
    {
      phase: "Phase 1: High Priority Skill Gaps (Weeks 1-3)",
      desc: missingSkills.length > 0
        ? `Master core requirements: ${missingSkills.slice(0, 3).join(", ")}`
        : "Deepen expertise in your strongest skills and explore advanced patterns",
      skills: missingSkills.slice(0, 3).map(s => ({ name: s, resource: getResource(s) }))
    },
    {
      phase: "Phase 2: Project-Based Application (Weeks 4-6)",
      desc: `Build a production-grade portfolio project matching real ${targetRole} requirements.`,
      skills: [
        { name: "Hands-on Projects", resource: "Build 2-3 real-world projects with deployment" },
        { name: "Clean Code", resource: "Clean Code by Robert Martin & Refactoring Guru" },
        { name: "Unit Testing", resource: "Jest/Pytest + TDD methodology" }
      ]
    },
    {
      phase: "Phase 3: Cloud & Deployment (Weeks 7-8)",
      desc: "Containerize and deploy with CI/CD pipelines and monitoring.",
      skills: [
        { name: "Docker", resource: getResource("Docker") },
        { name: "CI/CD", resource: "GitHub Actions + Vercel/AWS deployment" },
        { name: "Cloud Hosting", resource: "AWS Free Tier / Vercel / Railway" }
      ]
    },
    {
      phase: "Phase 4: Interview Mastery (Week 9-10)",
      desc: "Technical interviews, system design, and behavioral prep with STAR method.",
      skills: [
        { name: "DSA Practice", resource: "LeetCode 75 + NeetCode roadmap" },
        { name: "System Design", resource: getResource("System Design") },
        { name: "Mock Interviews", resource: "Pramp.com + interviewing.io" }
      ]
    }
  ];

  container.innerHTML = steps.map(s => `
    <div class="timeline-step">
      <div class="timeline-node"></div>
      <div class="timeline-content">
        <h5>${s.phase}</h5>
        <p>${s.desc}</p>
        <div class="timeline-tags">
          ${s.skills.map(sk => `<span class="timeline-tag" title="${sk.resource}">${sk.name}</span>`).join("")}
        </div>
      </div>
    </div>
  `).join("");
}

// ─── AI Mentor Chat (Real Gemini) ─────────────────────────────
function setupChat() {
  const chatMessagesEl = document.getElementById("chatMessages");
  const chatInput = document.getElementById("chatInput");
  const chatSendBtn = document.getElementById("chatSendBtn");
  const promptChips = document.querySelectorAll(".chat-chips .chip-btn");

  promptChips.forEach(chip => {
    chip.addEventListener("click", () => {
      chatInput.value = chip.textContent.replace(/^[^\w]*/, '').trim();
      sendChatMessage();
    });
  });

  chatSendBtn.addEventListener("click", sendChatMessage);
  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChatMessage();
  });

  async function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendBubble("user", text);
    chatInput.value = "";
    chatInput.disabled = true;
    chatSendBtn.disabled = true;

    // Show typing indicator
    const typingEl = showTypingIndicator();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          analysis: currentAnalysis
        })
      });

      removeTypingIndicator(typingEl);

      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      appendBubble("ai", data.reply);

    } catch (err) {
      removeTypingIndicator(typingEl);
      // Fallback to local response
      const fallback = generateLocalReply(text, currentAnalysis);
      appendBubble("ai", fallback);
    }

    chatInput.disabled = false;
    chatSendBtn.disabled = false;
    chatInput.focus();
  }

  function appendBubble(sender, text) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${sender}`;
    bubble.innerHTML = formatMarkdown(text);
    chatMessagesEl.appendChild(bubble);
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
  }

  function showTypingIndicator() {
    const typing = document.createElement("div");
    typing.className = "chat-bubble ai typing-indicator";
    typing.innerHTML = `
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
      <span class="typing-text">AI is thinking...</span>
    `;
    chatMessagesEl.appendChild(typing);
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
    return typing;
  }

  function removeTypingIndicator(el) {
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }
}

// Fallback local responses if API fails
function generateLocalReply(userPrompt, analysis) {
  const p = userPrompt.toLowerCase();

  if (!analysis) {
    return "💡 I'd love to give you personalized advice! Run an analysis on the **Smart Analyzer** tab first by uploading your resume, then come back here. In the meantime — focus on building real projects and keeping your GitHub active!";
  }

  if (p.includes("score") || p.includes("improve")) {
    return `🎯 **Your Score: ${analysis.employabilityScore}%**\n\nTo improve:\n1. **Bridge gaps**: Learn ${analysis.missing.slice(0, 3).join(", ") || "advanced topics"}\n2. **Add metrics**: Quantify achievements (e.g., *"Reduced load time by 40%"*)\n3. **Deploy projects**: Add live links & clean GitHub repos\n4. **Get certified**: Consider AWS/Google Cloud certifications`;
  }

  if (p.includes("roadmap") || p.includes("learn")) {
    return `🚀 **Personalized Roadmap for ${analysis.roles[0]}**:\n\n**Weeks 1-3**: Master ${analysis.missing.slice(0, 2).join(" & ") || "core fundamentals"}\n**Weeks 4-6**: Build 2 portfolio projects with deployment\n**Weeks 7-8**: Learn Docker + CI/CD\n**Week 9-10**: LeetCode practice + mock interviews\n\n📍 Check the **Career Roadmaps** tab for the full timeline!`;
  }

  if (p.includes("interview") || p.includes("question")) {
    return `💼 **Interview Prep for ${analysis.roles[0]}**:\n\n1. *"Walk me through a project using ${analysis.matched.slice(0, 2).join(" and ")}"*\n2. *"How would you design a scalable ${analysis.roles[0].includes("Full") ? "REST API" : "data pipeline"}?"*\n3. *"What's the difference between ${analysis.matched[0] || "SQL"} and alternatives?"*\n\n💡 **Tip**: Use the STAR method for behavioral questions!`;
  }

  return `🤖 With **${analysis.matched.length} matched skills** and **${analysis.employabilityScore}%** employability, you're on a great track for **${analysis.roles[0]}**!\n\nAsk me about:\n• How to improve your score\n• Learning roadmap recommendations\n• Interview question prep\n• Resume optimization tips`;
}

function formatMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code style="background:rgba(255,255,255,0.1);padding:2px 6px;border-radius:4px;">$1</code>')
    .replace(/\n/g, '<br>');
}
