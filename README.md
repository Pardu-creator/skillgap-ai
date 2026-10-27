# SkillGap AI — Career Intelligence Platform

Analyze your resume against any job description and get an instant,
AI-powered skills-gap report: employability score, matched & missing skills,
role compatibility across 9 career blueprints, a personalized 12-week learning
roadmap, and an AI mentor you can chat with.

## What the app does

| Feature | Description |
|---|---|
| Auth | Sign-in / register / reset-password with PBKDF2-SHA256 hashing, 5-attempt lockout, password-strength meter, seeded demo accounts |
| Skill Analyzer | Upload a resume (PDF/TXT) or paste text, pick a job role template → extracted skills vs. ~120-skill taxonomy → employability gauge, match %, matched/missing/extra skill clouds, resume suggestions |
| Role Analytics | Compatibility score + salary estimate for Full-Stack, Frontend, Backend, ML, Data, Cloud/DevOps, Cyber Security, Mobile, AI/LLM roles |
| Roadmap | Auto-generated phased learning plan with curated resources and progress tracking |
| AI Mentor | Chat assistant — Gemini 2.0 Flash when an API key is configured, offline expert fallback otherwise |
| Settings | Profile, target role, engine status |

## Repository layout

```
├── app.py                  # Streamlit app (primary web UI, port 8501)
├── backend.py              # Core logic: auth, resume analysis, mentor
├── database.py             # SQLite user store (skillgap_users.db)
├── index.html + app.js + style.css   # Static vanilla-JS frontend
├── api/                    # Vercel serverless functions (analyze, chat)
├── skillgap_flutter/       # Flutter mobile/web/desktop port (Dart)
├── selenium-tests/         # Mocha + WebDriver E2E suite (~300 cases)
├── appium-tests/           # WebdriverIO + UiAutomator2 mobile suite
├── load-tests/             # k6 load test (100 VUs, GET-only)
├── scripts/                # Excel report generators
├── Vulnerability Test Results/   # Security scan outputs
└── .github/workflows/      # CI: test_suite.yml, all-tests.yml, build-and-deploy.yml, security-review.yml
```

---

## A–Z: run everything

### 0. Prerequisites

| Tool | Version | Install |
|---|---|---|
| Python | 3.11+ | python.org |
| Node.js | 20+ | nodejs.org |
| Flutter | stable | `flutter doctor` |
| Chrome | latest | for Selenium |
| k6 | latest | `choco install k6` / grafana.com/docs/k6 |
| Appium 2 | optional | `npm i -g appium` + `appium driver install uiautomator2` |

### 1. Python dependencies (once)

```bash
pip install -r requirements.txt
```

(`streamlit pypdf openai openpyxl bcrypt python-dotenv`)

### 2. Run the Streamlit web app

```bash
streamlit run app.py
```

Opens at **http://localhost:8501**. This is the main UI and the target of
the Selenium / load-test suites.

### 3. Run the static frontend

```bash
python -m http.server 8080
```

then open `http://localhost:8080/index.html`. The `api/` serverless functions
run on Vercel (`vercel dev`), not in this static server.

### 4. Demo accounts

| Email / User | Password | Profile |
|---|---|---|
| `demo@skillgap.ai` | `Password123!` | Full demo analysis |
| `alex` | `Password123!` | Mid-level developer |
| `priya` | `Password123!` | Data-science track |

### 5. Run the Flutter app

```bash
cd skillgap_flutter
flutter pub get

flutter run -d chrome      # web
flutter run -d windows     # windows desktop
flutter run                # connected Android device/emulator
```

Build artifacts:

```bash
flutter build apk --release     # → build/app/outputs/flutter-apk/app-release.apk
flutter build web --release     # → build/web/
flutter analyze && flutter test # lint + unit tests
```

### 6. Run the Selenium suite (needs app on :8501 + Chrome)

```bash
streamlit run app.py &            # terminal 1
cd selenium-tests
npm install
npm test                          # terminal 2 — mocha spec output
npm run test:full                 # JSON results + Excel report
```

Reports land in `selenium-tests/reports/` + `selenium-test-summary.xlsx`.

### 7. Run the Appium suite (needs Android emulator/device)

```bash
appium --port 4723 &              # terminal 1
cd appium-tests
npm install
BASE_URL=http://localhost:8501 npm test
npm run report                    # → appium-test-report.xlsx
```

Default target: Android 13 emulator `emulator-5554` against
`https://skill-gap-ai.streamlit.app` — override with `BASE_URL`.

### 8. Run the k6 load test

```bash
streamlit run app.py &            # app must be reachable
k6 run --env BASE_URL=http://localhost:8501 load-tests/load-test.js
```

Thresholds: p50 < 500 ms, p90 < 1500 ms, p95 < 2500 ms, p99 < 5000 ms,
error & HTTP-failure rates < 5%. Reports → `load-tests/reports/`.

### 9. Generate Excel reports

```bash
python scripts/generate_excel_reports.py   # findings + endpoint inventory
python scripts/generate_test_excels.py     # selenium + appium workbooks
```

### 10. Security scans

```bash
pip install bandit pip-audit semgrep
bandit -r .
pip-audit -r requirements.txt
semgrep scan --config auto
```

Outputs are collected under `Vulnerability Test Results/`.

---

## CI / GitHub Actions

Pushing to `main` runs **`test_suite.yml`**:

```
setup-node ─┬─ Unit Tests — API (300) ─────→ Deployment Status (300) ─┐
            ├─ Selenium — Website Tests (300)                          │
            ├─ Appium — Android Tests (300)                            ├─→ Compile Master Report & Deploy
            ├─ Validation Tests (300)                                  │
            ├─ Load Testing — Performance (300)                        │
            ├─ security-assessment                                     │
            └─ web-build (Flutter web)                                 ┘
```

Artifacts per run: `web-build`, `selenium-report`, `appium-report`,
`load-report`, `security-report`, `unit-test-report`, `validation-report`,
`deployment-status-report`, `master-report` (90-day retention).

Other workflows: `all-tests.yml` (security audit + all 4 suites + Excel),
`build-and-deploy.yml` (APK + website deploy), `security-review.yml`.
