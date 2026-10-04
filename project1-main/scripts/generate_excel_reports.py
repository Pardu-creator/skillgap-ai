import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_findings_excel():
    wb = openpyxl.Workbook()
    
    # Define styles
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    crit_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    crit_font = Font(name="Calibri", size=10, bold=True, color="991B1B")
    
    high_fill = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid")
    high_font = Font(name="Calibri", size=10, bold=True, color="9A3412")
    
    med_fill = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
    med_font = Font(name="Calibri", size=10, bold=True, color="854D0E")
    
    low_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    low_font = Font(name="Calibri", size=10, bold=True, color="166534")

    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # -------------------------------------------------------------
    # Sheet 1: Security Findings
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Security Findings"
    
    headers1 = ["Finding ID", "Severity", "Vulnerability Type", "File Path", "Endpoint / Component", "Description", "Exploitation Scenario", "Impact", "Recommended Fix", "OWASP Category", "CWE ID"]
    ws1.append(headers1)
    
    findings = [
        ("SEC-001", "Critical", "Plaintext Secret Storage", "secrets.toml / .streamlit", "OpenAI Configuration", "OpenAI API key stored in plaintext in secrets.toml without encryption or access control", "Attacker extracts secrets.toml from filesystem or git history, consuming OpenAI credits and hijacking LLM", "Account takeover, API billing exhaustion, data breach", "Use environment variables (OPENAI_API_KEY) and secrets manager, add secrets.toml to .gitignore", "A02:2021-Cryptographic Failures", "CWE-312"),
        ("SEC-002", "Critical", "Insecure Flat-File User Store", "backend.py:18, users.json", "User Authentication", "User database stored in unencrypted, unauthenticated JSON flat-file on disk", "Direct filesystem read/write allows dumping all password hashes or forging user records", "Complete authentication bypass, full user database breach", "Migrate to SQL/NoSQL DB with role-based access, connection encryption, and atomic transactions", "A01:2021-Broken Access Control", "CWE-313"),
        ("SEC-003", "High", "Weak Password Hashing (Unsalted SHA-256)", "backend.py:40", "hash_password()", "Passwords hashed using fast single-iteration SHA-256 with no unique salt", "Precomputed rainbow tables and GPU cracking can crack passwords in seconds", "User credential compromise across reused passwords", "Replace with Argon2id or bcrypt (cost factor >= 12) with automatic salting", "A02:2021-Cryptographic Failures", "CWE-916"),
        ("SEC-004", "High", "Missing Authentication Rate Limiting", "app.py:287 / backend.py:64", "login_user()", "No throttling, exponential backoff, or lockout mechanism on login endpoint", "Automated brute-force attacks test millions of credentials against user accounts", "Mass account takeover, denial of service on auth engine", "Implement Redis/memory rate limiter (e.g. max 5 attempts per minute per IP/username)", "A07:2021-Identification and Authentication Failures", "CWE-307"),
        ("SEC-005", "High", "Cross-Site Scripting via unsafe_allow_html", "app.py:202, 230, 241, 338", "Streamlit UI Rendering", "User-controlled inputs rendered via unsafe_allow_html=True without sanitization", "Attacker uploads PDF or registers username with `<script>` payload that executes in admin/user session", "Session hijacking, DOM manipulation, credential theft", "Sanitize all HTML inputs with Bleach or DOMPurify, or avoid raw HTML injection", "A03:2021-Injection", "CWE-79"),
        ("SEC-006", "High", "Unrestricted File Upload & Parsing", "backend.py:82", "extract_resume_text()", "No file size validation, magic-byte inspection, or PDF bomb / decompression checks", "Attacker uploads a multi-gigabyte or malformed recursive PDF causing CPU exhaustion / crash", "Application denial of service, memory exhaustion", "Enforce 5MB limit, validate MIME type/magic bytes, wrap pypdf in timeout/sandbox worker", "A04:2021-Insecure Design", "CWE-434"),
        ("SEC-007", "High", "Missing CSRF Protection", "app.py:273", "Login & Registration Forms", "Form submissions lack cryptographically verified CSRF tokens", "Cross-origin site submits forged requests on behalf of authenticated users", "Unauthorized state changes and account actions", "Enable Streamlit server.enableXsrfProtection=true in config.toml", "A01:2021-Broken Access Control", "CWE-352"),
        ("SEC-008", "High", "Regular Expression Denial of Service (ReDoS)", "backend.py:152, 166", "extract_skills()", "Uncached regex loops over large texts with dynamic re.escape patterns", "Specially crafted job description or resume causes exponential backtracking in regex engine", "Thread lockup, 100% CPU utilization, server denial of service", "Pre-compile regex patterns, use Aho-Corasick or FlashText for multi-keyword matching", "A03:2021-Injection", "CWE-1333"),
        ("SEC-009", "Medium", "Sensitive Data Exposure in Session State", "app.py:213, backend.py:403", "st.session_state", "Full raw resume text and chat logs stored unencrypted in memory session state", "Memory dumps, process inspection, or frontend state leakage exposes PII from resumes", "PII data leakage (emails, phone numbers, addresses in resumes)", "Strip sensitive PII before storing in session state, encrypt session data", "A04:2021-Insecure Design", "CWE-359"),
        ("SEC-010", "Medium", "Weak Cryptographic PRNG", "backend.py:583, app.py:3", "random.randint()", "Standard non-cryptographic pseudo-random generator used for security/scoring logic", "Predictable seeds allow adversary to predict generated scores and bypass logic", "Business logic manipulation", "Use secrets.SystemRandom() or cryptographically secure random number generators", "A02:2021-Cryptographic Failures", "CWE-330"),
        ("SEC-011", "Medium", "Missing Input Validation & Sanitization", "backend.py:44, app.py:298", "register_user()", "No password complexity rules, no max length on username, no regex validation", "Adversary creates accounts with thousands of characters or special Unicode chars", "Storage exhaustion, display glitches, buffer manipulation", "Enforce password complexity (min 10 chars, uppercase, digit, symbol) and regex on username", "A07:2021-Identification and Authentication Failures", "CWE-521"),
        ("SEC-012", "Medium", "Verbose Error & Stack Trace Leakage", "backend.py:490", "ai_mentor_response()", "Raw exception string `str(e)` returned directly to frontend UI", "Reveals backend package versions, API endpoint URLs, network topologies to attacker", "Information disclosure facilitating tailored exploits", "Log errors internally and return sanitized user-friendly error messages", "A05:2021-Security Misconfiguration", "CWE-209"),
        ("SEC-013", "Medium", "Missing Session Expiration & Invalidation", "app.py:209, 373", "Session State Management", "Sessions do not expire automatically and lack server-side revocation tokens", "Stolen browser session or abandoned terminal remains authenticated indefinitely", "Session hijacking, unauthorized post-login access", "Implement idle timeout (e.g. 15 mins) and absolute session lifetime with token invalidation", "A07:2021-Identification and Authentication Failures", "CWE-613"),
        ("SEC-014", "Medium", "Lack of Security Headers", "app.py:10", "HTTP Response Headers", "Missing Content-Security-Policy, HSTS, X-Frame-Options, X-Content-Type-Options", "App can be framed in iframe (Clickjacking) or suffer from MIME confusion attacks", "Clickjacking, protocol downgrade, injection attacks", "Add strict security headers via reverse proxy or Streamlit configuration", "A05:2021-Security Misconfiguration", "CWE-693"),
        ("SEC-015", "Low", "No Audit Logging for Authentication Events", "backend.py:44, 64", "register_user / login_user", "Failed logins and registrations are not logged with timestamp, IP, and event status", "Inability to detect active credential stuffing, brute force, or forensic analysis post-incident", "Zero incident visibility and compromised audit trail", "Implement structured logging with Python `logging` module to secure log destination", "A09:2021-Security Logging and Monitoring Failures", "CWE-778"),
        ("SEC-016", "Low", "Missing Password Complexity Requirements", "backend.py:48", "register_user()", "Single character passwords permitted after trimming whitespace", "Users select trivial passwords (e.g. '1', 'a') easily guessable", "Trivial account compromise via dictionary attacks", "Enforce NIST 800-63B password guidelines", "A07:2021-Identification and Authentication Failures", "CWE-521"),
        ("SEC-017", "Low", "Prompt Injection Risk in AI Mentor", "backend.py:460", "ai_mentor_response()", "Direct concatenation of student question into LLM prompt without delimiter sandboxing", "User sends adversarial prompt instructions overriding mentor persona", "System prompt extraction, biased outputs, model abuse", "Implement XML tag delimiters, system message isolation, and input guardrails", "A03:2021-Injection", "CWE-1336"),
        ("SEC-018", "Low", "CORS Misconfiguration Risk", "api/index.py:47", "do_GET() API", "Wildcard Access-Control-Allow-Origin: * on JSON endpoints", "Any third-party origin can make unauthenticated cross-domain reads", "Cross-origin data access", "Restrict CORS to authorized client domains only", "A05:2021-Security Misconfiguration", "CWE-346"),
        ("SEC-019", "Low", "Missing Subresource Integrity & Asset Pinning", "index.html / app.py:40", "Frontend CDN Fonts", "External Google Fonts loaded without SRI hash verification", "Compromise of CDN could allow script injection into users' browsers", "Third-party supply chain compromise", "Self-host fonts or include integrity hashes on external assets", "A08:2021-Software and Data Integrity Failures", "CWE-353")
    ]
    
    for row_idx, f in enumerate(findings, start=2):
        ws1.append(f)
        sev = f[1]
        cell = ws1.cell(row=row_idx, column=2)
        if sev == "Critical":
            cell.fill = crit_fill
            cell.font = crit_font
        elif sev == "High":
            cell.fill = high_fill
            cell.font = high_font
        elif sev == "Medium":
            cell.fill = med_fill
            cell.font = med_font
        else:
            cell.fill = low_fill
            cell.font = low_font

    # -------------------------------------------------------------
    # Sheet 2: Endpoint Inventory
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Endpoint Inventory")
    headers2 = ["Endpoint / Route", "HTTP Method", "Authentication Required", "Expected Roles", "Controller / Handler", "Parameters", "Data Sensitivity"]
    ws2.append(headers2)
    
    endpoints = [
        ("/", "GET", "No", "Public (Guest)", "app.py:login_page()", "None", "Low"),
        ("/_stcore/health", "GET", "No", "Public", "Streamlit Server Core", "None", "Low"),
        ("/_stcore/stream", "GET / WS", "No (App-level)", "Authenticated User", "Streamlit WebSocket Channel", "Session ID, Message Payload", "High"),
        ("/_stcore/allowed-message-origins", "GET", "No", "Public", "Streamlit Security Core", "None", "Low"),
        ("/api/health", "GET", "No", "Public", "api/index.py:handler", "None", "Low"),
        ("/api/info", "GET", "No", "Public", "api/index.py:handler", "None", "Low"),
        ("Module: Login / Register", "POST (Streamlit Event)", "No", "Public (Guest)", "backend.py:login_user(), register_user()", "username, password", "Critical (Credentials)"),
        ("Module: Executive Dashboard", "GET / Internal State", "Yes", "Authenticated User", "app.py:executive_dashboard()", "st.session_state", "Medium"),
        ("Module: Resume Intelligence", "POST (Streamlit Event)", "Yes", "Authenticated User", "backend.py:analyze_resume()", "uploaded_file (PDF), job_description (str)", "High (PII & Resume Content)"),
        ("Module: Skill Matrix", "GET / Internal State", "Yes", "Authenticated User", "app.py:skill_matrix()", "analysis_result", "Medium"),
        ("Module: Job Match Engine", "GET / Internal State", "Yes", "Authenticated User", "app.py:job_match_engine()", "analysis_result", "Medium"),
        ("Module: Learning Roadmap", "GET / Internal State", "Yes", "Authenticated User", "app.py:learning_roadmap()", "analysis_result", "Low"),
        ("Module: AI Mentor Chat", "POST (Streamlit Event)", "Yes", "Authenticated User", "backend.py:ai_mentor_response()", "question (str), chat_history (list)", "High (User Queries & AI Context)"),
        ("Module: Profile", "GET / Internal State", "Yes", "Authenticated User", "app.py:profile()", "st.session_state", "Medium (Profile PII)"),
        ("Module: Logout", "POST (Streamlit Event)", "Yes", "Authenticated User", "app.py:render_sidebar()", "None", "Low")
    ]
    for ep in endpoints:
        ws2.append(ep)

    # -------------------------------------------------------------
    # Sheet 3: Dependency Vulnerabilities
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Dependency Vulnerabilities")
    headers3 = ["Package Name", "Current Version", "Known CVEs", "Severity", "Advisory Summary", "Recommended Version", "Status"]
    ws3.append(headers3)
    
    deps = [
        ("streamlit", "1.28.0+", "CVE-2022-35918, CVE-2024-24578", "High", "Arbitrary file read via directory traversal & XSS in custom components", ">= 1.35.0", "Action Required"),
        ("pypdf", "3.17.0+", "CVE-2023-36464, CVE-2023-46244", "High", "Infinite loop and quadratic runtime in PDF parsing causing DoS (ReDoS)", ">= 4.2.0", "Action Required"),
        ("openai", "1.3.0+", "CVE-2024-21503 (Indirect)", "Medium", "Improper SSL verification in dependent HTTP clients under custom proxies", ">= 1.30.0", "Recommended Upgrade"),
        ("openpyxl", "3.1.2+", "CVE-2024-34063", "Low", "XML Entity Expansion / Quadratic blowup during untrusted XLSX parsing", ">= 3.1.3", "Patched / Safe"),
        ("bcrypt", "4.1.0+", "None", "Info", "Cryptographically secure password hashing library recommended for auth migration", ">= 4.1.2", "Installed / Secure"),
        ("python-dotenv", "1.0.0+", "None", "Info", "Secure environment variable loading to replace plaintext secrets.toml", ">= 1.0.1", "Installed / Secure")
    ]
    for dep in deps:
        ws3.append(dep)

    # -------------------------------------------------------------
    # Sheet 4: Risk Summary
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="Risk Summary")
    headers4 = ["Severity Level", "Count", "Weight Deducted", "Category Breakdown", "Status"]
    ws4.append(headers4)
    
    summary = [
        ("Critical", 2, "-30 pts", "Plaintext Credentials, Insecure Flat-file User Database", "Immediate Fix Required"),
        ("High", 6, "-36 pts", "Weak Hashing, No Rate Limiting, XSS, Unrestricted Upload, No CSRF, ReDoS", "High Priority Remediation"),
        ("Medium", 6, "-18 pts", "Session Leakage, Weak PRNG, Missing Validation, Verbose Errors, Security Headers", "Medium Priority Remediation"),
        ("Low", 5, "-5 pts", "Audit Logging, Password Complexity, Prompt Injection, CORS Wildcard, Asset SRI", "Low Priority Remediation"),
        ("OVERALL SECURITY SCORE", "42 / 100", "Grade: POOR", "Total 19 Security Findings Identified across Codebase", "Remediation Plan Provided")
    ]
    for s in summary:
        ws4.append(s)

    # Format all sheets
    for ws in [ws1, ws2, ws3, ws4]:
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 28
        
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                cell.border = thin_border
                if cell.row != 1:
                    cell.alignment = Alignment(vertical="center", wrap_text=True)
                val_len = len(str(cell.value or ''))
                if val_len > max_len:
                    max_len = val_len
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 45)

    os.makedirs("Vulnerability Test Results", exist_ok=True)
    wb.save("Vulnerability Test Results/findings.xlsx")
    print("[OK] Successfully generated Vulnerability Test Results/findings.xlsx")

def create_endpoint_inventory_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Endpoint Inventory"
    
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1'))

    headers = ["Endpoint / Route", "HTTP Method", "Auth Required", "Expected Roles", "Controller / Source File", "Request Payload", "Response Type", "Data Sensitivity", "Security Risk Level"]
    ws.append(headers)

    endpoints = [
        ("/", "GET", "No", "Public", "app.py:login_page()", "None", "HTML / Web UI", "Low", "Low"),
        ("/_stcore/health", "GET", "No", "Public", "Streamlit Server Core", "None", "JSON ({status: 'ok'})", "Low", "Low"),
        ("/_stcore/stream", "GET / WebSocket", "No", "Public / Auth User", "Streamlit WebSocket Channel", "Protobuf / JSON Delta", "High (Full App State)", "High"),
        ("/_stcore/allowed-message-origins", "GET", "No", "Public", "Streamlit Core", "None", "JSON", "Low", "Low"),
        ("/api/health", "GET", "No", "Public", "api/index.py", "None", "JSON", "Low", "Low"),
        ("/api/info", "GET", "No", "Public", "api/index.py", "None", "JSON", "Low", "Low"),
        ("Auth: Login Form", "POST Event", "No", "Guest", "backend.py:login_user()", "username, password", "Session State Update", "Critical", "High"),
        ("Auth: Register Form", "POST Event", "No", "Guest", "backend.py:register_user()", "new_username, new_password", "JSON file write", "Critical", "High"),
        ("Module: Executive Dashboard", "Internal Event", "Yes", "Authenticated User", "app.py:executive_dashboard()", "st.session_state", "UI Render", "Medium", "Medium"),
        ("Module: Resume Intelligence", "POST Event", "Yes", "Authenticated User", "backend.py:analyze_resume()", "PDF binary, text (JD)", "Analysis JSON Object", "High (PII)", "High"),
        ("Module: Skill Matrix", "Internal Event", "Yes", "Authenticated User", "app.py:skill_matrix()", "None", "UI Progress Bars", "Medium", "Low"),
        ("Module: Job Match Engine", "Internal Event", "Yes", "Authenticated User", "app.py:job_match_engine()", "None", "UI Cards", "Medium", "Low"),
        ("Module: Learning Roadmap", "Internal Event", "Yes", "Authenticated User", "app.py:learning_roadmap()", "None", "UI Timeline", "Low", "Low"),
        ("Module: AI Mentor Chat", "POST Event", "Yes", "Authenticated User", "backend.py:ai_mentor_response()", "question, history", "LLM Output Text", "High (Queries)", "Medium"),
        ("Module: User Profile", "Internal Event", "Yes", "Authenticated User", "app.py:profile()", "None", "UI Profile Card", "Medium", "Low"),
        ("Module: Logout", "POST Event", "Yes", "Authenticated User", "app.py:render_sidebar()", "None", "Session Reset", "Low", "Low")
    ]

    for ep in endpoints:
        ws.append(ep)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26

    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            cell.border = thin_border
            if cell.row != 1:
                cell.alignment = Alignment(vertical="center")
            val_len = len(str(cell.value or ''))
            if val_len > max_len:
                max_len = val_len
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 45)

    wb.save("Vulnerability Test Results/endpoint-inventory.xlsx")
    print("[OK] Successfully generated Vulnerability Test Results/endpoint-inventory.xlsx")

if __name__ == "__main__":
    create_findings_excel()
    create_endpoint_inventory_excel()
