# 🛡️ JobGuard AI - Online Fraud & Fake Job Detection Platform

**JobGuard AI** is a state-of-the-art, humanized AI-powered platform designed to protect job seekers worldwide against fraudulent job postings, fake offer letters, recruiter impersonation scams, and predatory financial traps.

---

## 🌟 Key Features & Subsystems

1. **🔍 AI Job Posting Scanner**:
   - Evaluates job posts, recruiter emails, and WhatsApp/Telegram chat snippets against **150+ scam signature heuristics**.
   - Identifies upfront registration fee demands, fake check overpayment traps, crypto/task rating schemes, and artificial urgency.
   - Calculates **Fraud Risk Score (0-100%)** with interactive radar threat distribution charts.
   - Provides **Humanized & Actionable Candidate Advice** on what to do next.

2. **📄 Offer Letter & Contract Auditor (Single & Batch Folder Upload)**:
   - Drag & drop PDF/document offer letters or upload entire folders. Built-in **PDF.js** automatically extracts text in real-time.
   - Parses appointment letters for counterfeit equipment check clauses, mandatory deposit requirements, and premature banking credential requests.
   - Multi-vector research verification ensuring a **0% Zero Risk Guarantee** for authentic employment contracts.

3. **💰 Real Market vs Scam Bait Salary Sanity Evaluator**:
   - Role & Experience Benchmarks across 8 job roles (Data Entry, Video Task Rating, Support, Content, Dev, Design, Package Reshipping).
   - Calculates **Scam Bait Multiplier** (e.g. 4.5x normal pay) to alert users before they fall for upfront fee traps.

4. **🛡️ Recruiter Email & Domain Verifier**:
   - Flags typosquatting and lookalike domains (e.g. `google-careers-jobs.com` vs `google.com`).
   - Alerts candidates when free public email services (`@gmail.com`, `@yahoo.com`) are used by alleged Fortune 500 recruiters.

5. **📱 Scammer Phone, Telegram Handle & UPI Blacklist Lookup**:
   - Search phone numbers, Telegram handles (@username), or UPI VPAs against known fraud databases.

6. **📜 Official Cyber Crime Police Complaint Generator**:
   - Formats a comprehensive formal criminal cyber complaint under **Section 66D IT Act** and **Section 420 IPC** ready to copy/print for National Cyber Crime Portal (1930 / cybercrime.gov.in).

7. **❓ 60-Second Scam Self-Assessment Quiz**:
   - Diagnostic 5-question interactive checklist for candidates to assess immediate risk.

8. **🚨 Community Scam Database & Reporting Hub**:
   - Searchable repository of real-world scam patterns and public contribution forms with evidence modal.

9. **🌐 Multi-Language Support (English / తెలుగు / हिन्दी)**:
   - Seamless one-click translation across English, Telugu, and Hindi.

---

## 🚀 Quick Start Guide

### Option 1: Instant Zero-Setup Web App (Recommended)
1. Open folder in File Explorer: `c:\Users\RAMYA SRI\Downloads\research`
2. Double-click **`index.html`** in any browser (Chrome, Edge, Firefox, Brave, Safari).
3. Everything runs 100% locally and offline!

### Option 2: Python FastAPI REST API Backend
```bash
# 1. Install dependencies
pip install fastapi uvicorn pydantic

# 2. Start the server
python backend/server.py

# 3. View Swagger API Docs in browser
http://127.0.0.1:8000/docs
```

---

## 📂 Project Structure

```
research/
├── index.html                   # Master responsive Web Application
├── assets/
│   ├── css/
│   │   └── style.css            # Glassmorphism UI & custom styling
│   └── js/
│       ├── detector_engine.js   # Client-side NLP & Heuristic Rule Engine
│       ├── sample_jobs.js       # Verified Real vs Scam Sample Datasets
│       └── app.js               # UI Controllers, Chart.js, and Quiz Logic
├── backend/
│   ├── detector.py              # Python detection module
│   ├── server.py                # FastAPI REST API backend
│   └── requirements.txt         # Backend Python packages
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore specifications
```

---

## 💡 Top Red Flags Detected by JobGuard AI

- **Upfront Fees:** Demanding registration, ID card, or training fees before employment.
- **Fake Checks:** Mailing a check to purchase equipment from an "approved vendor".
- **Chat-Only Hiring:** Conducting entire interviews exclusively over Telegram or WhatsApp.
- **Unrealistic Compensation:** Offering $50+/hr for simple data entry, typing, or liking videos.
- **Free Email Domains:** High-profile corporate recruiters using `@gmail.com` or `@yahoo.com`.
