"""
JobGuard AI - FastAPI REST Backend
Full-stack APIs for job scanning, offer letter auditing, recruiter domain verification,
salary sanity benchmarks, scammer phone/UPI blacklist lookup, and cyber complaints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import re
import datetime

try:
    from backend.detector import analyze_job, audit_offer_letter
except ImportError:
    from detector import analyze_job, audit_offer_letter

app = FastAPI(
    title="JobGuard AI Enterprise API",
    description="Intelligent Online Fake Job Detection & Multi-Vector Scam Verification Service",
    version="2.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class JobScanRequest(BaseModel):
    title: Optional[str] = ""
    company: Optional[str] = ""
    salary: Optional[str] = ""
    email: Optional[str] = ""
    website: Optional[str] = ""
    description: str

class OfferAuditRequest(BaseModel):
    offer_text: str

class RecruiterVerifyRequest(BaseModel):
    email: str
    company: Optional[str] = ""
    website: Optional[str] = ""

class SalaryCalcRequest(BaseModel):
    role: str
    experience: str
    time_commitment: str
    offered_pay: float

class LookupRequest(BaseModel):
    query: str

class ComplaintRequest(BaseModel):
    victim_name: str
    victim_phone: str
    victim_city: Optional[str] = ""
    suspect_name: Optional[str] = ""
    suspect_contact: Optional[str] = ""
    loss_amount: Optional[str] = ""
    incident_description: str

class ReportScamRequest(BaseModel):
    company: str
    title: str
    contact: Optional[str] = ""
    scam_type: Optional[str] = "Community Report"
    details: str

# In-Memory Community Database
SCAM_DATABASE_STORE: List[Dict[str, Any]] = [
    {
        "id": "scam_001",
        "title": "VIP YouTube Video Rating & Deposit Scam",
        "company": "Digital Media Matrix Ltd",
        "reporter": "Verified Community Alert",
        "date": "Yesterday",
        "scamType": "Prepaid Task Scam",
        "redFlag": "Demanded ₹2,500 deposit in USDT to unlock salary for liking YouTube videos.",
        "modusOperandi": "Victim receives unsolicited WhatsApp message promising ₹3,000/day. Directed to Telegram group where they are asked to deposit money into a crypto wallet.",
        "financialLoss": "₹15,000 to ₹1,50,000",
        "fakeContacts": "@Nexus_VIP_Mentor, +91 98765-43210",
        "defenseAdvice": "Never deposit money or cryptocurrency to receive salary. Report to 1930 immediately."
    },
    {
        "id": "scam_002",
        "title": "Remote Data Entry Equipment Cashier Check Fraud",
        "company": "Apex Global Logistics Corp",
        "reporter": "Job Seeker Alert",
        "date": "2 days ago",
        "scamType": "Fake Check Overpayment",
        "redFlag": "Sent fake $3,850 cashier check to buy Apple MacBook from unverified vendor.",
        "modusOperandi": "Scammers send a counterfeit check and instruct candidate to deposit it and wire funds to their 'IT equipment vendor'.",
        "financialLoss": "$3,850",
        "fakeContacts": "apexlogistics.hiring@gmail.com",
        "defenseAdvice": "Banks hold you responsible for bounced checks. Never wire money from a deposited check."
    }
]

@app.get("/")
def read_root():
    return {
        "service": "JobGuard AI Enterprise Scam Detection Backend",
        "status": "online",
        "version": "2.5.0",
        "endpoints": [
            "/api/scan-job",
            "/api/audit-offer",
            "/api/verify-recruiter",
            "/api/calculate-salary",
            "/api/lookup-scammer",
            "/api/generate-complaint",
            "/api/scam-database",
            "/api/report-scam"
        ],
        "docs": "/docs"
    }

@app.post("/api/scan-job")
def scan_job_endpoint(payload: JobScanRequest):
    if not payload.description and not payload.title:
        raise HTTPException(status_code=400, detail="Job title or description is required.")
    
    result = analyze_job(
        title=payload.title or "",
        company=payload.company or "",
        salary=payload.salary or "",
        email=payload.email or "",
        website=payload.website or "",
        description=payload.description or ""
    )
    return result

@app.post("/api/audit-offer")
def audit_offer_endpoint(payload: OfferAuditRequest):
    if not payload.offer_text or not payload.offer_text.strip():
        raise HTTPException(status_code=400, detail="Offer letter text is required.")
    
    result = audit_offer_letter(payload.offer_text)
    return result

@app.post("/api/verify-recruiter")
def verify_recruiter_endpoint(payload: RecruiterVerifyRequest):
    email = payload.email.lower().strip()
    company = payload.company.strip() if payload.company else ""
    domain = email.split("@")[-1] if "@" in email else ""
    
    free_providers = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "protonmail.com"]
    is_free = domain in free_providers
    
    if is_free:
        return {
            "status": "HIGH_RISK_FREE_EMAIL",
            "score": 85,
            "verdict": "Unverified Free Email Provider",
            "details": f"Recruiter claims to represent '{company or 'Company'}' but is using a free public email ({domain}). Real corporate recruiters use verified enterprise domains.",
            "is_free_email": True
        }
    
    return {
        "status": "VERIFIED_DOMAIN",
        "score": 10,
        "verdict": "Corporate Domain Registered",
        "details": f"Domain '{domain}' appears to be an official custom corporate email handle.",
        "is_free_email": False
    }

@app.post("/api/calculate-salary")
def calculate_salary_endpoint(payload: SalaryCalcRequest):
    benchmarks = {
        "data_entry": {"fresher": (10000, 18000, 14000), "entry": (14000, 24000, 19000), "mid": (20000, 35000, 26000)},
        "task_rating": {"fresher": (0, 2000, 800), "entry": (0, 3000, 1200), "mid": (0, 5000, 2000)},
        "customer_support": {"fresher": (15000, 25000, 20000), "entry": (22000, 35000, 28000), "mid": (30000, 55000, 42000)},
        "software_dev": {"fresher": (25000, 55000, 38000), "entry": (45000, 85000, 62000), "mid": (80000, 160000, 110000)}
    }
    
    role_bench = benchmarks.get(payload.role, benchmarks["data_entry"])
    min_pay, max_pay, avg_pay = role_bench.get(payload.experience, role_bench["fresher"])
    
    factor = 0.35 if payload.time_commitment == "part_time" else 1.0
    adj_min = int(min_pay * factor)
    adj_max = int(max_pay * factor)
    adj_avg = max(1, int(avg_pay * factor))
    
    ratio = round(payload.offered_pay / adj_avg, 2)
    is_scam_bait = ratio >= 2.2 or (payload.role == "task_rating" and payload.offered_pay > 5000)
    
    return {
        "role": payload.role,
        "experience": payload.experience,
        "time_commitment": payload.time_commitment,
        "offered_pay": payload.offered_pay,
        "benchmark_range": f"₹{adj_min:,} - ₹{adj_max:,} / mo",
        "multiplier": f"{ratio}x",
        "is_scam_bait": is_scam_bait,
        "verdict": "🚨 Extreme Scam Bait Payout" if is_scam_bait else ("⚠️ Elevated Compensation" if ratio >= 1.5 else "✅ Realistic Market Rate")
    }

@app.post("/api/lookup-scammer")
def lookup_scammer_endpoint(payload: LookupRequest):
    q = payload.query.lower().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    known_scams = [
        {"query": "+919876543210", "formatted": "+91 98765-43210", "type": "WhatsApp", "category": "Crypto VIP Task Fraud", "complaints": 14, "risk": "CRITICAL"},
        {"query": "@nexus_vip_mentor", "formatted": "@Nexus_VIP_Mentor", "type": "Telegram", "category": "Prepaid Task Scam", "complaints": 28, "risk": "CRITICAL"},
        {"query": "hr.globalcloud@okaxis", "formatted": "hr.globalcloud@okaxis", "type": "UPI VPA", "category": "Registration Fee Trap", "complaints": 9, "risk": "CRITICAL"}
    ]
    
    for item in known_scams:
        if item["query"] in q or q in item["query"]:
            return {"found": True, "data": item}
            
    return {"found": False, "message": "No community fraud records found for this query."}

@app.post("/api/generate-complaint")
def generate_complaint_endpoint(payload: ComplaintRequest):
    now_str = datetime.datetime.now().strftime("%d-%b-%Y")
    letter = f"""TO:
The Superintendent of Police / Cyber Crime Investigation Cell,
National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in)

DATE: {now_str}

SUBJECT: Formal Criminal Complaint against Employment Fraud, Impersonation and Cyber Cheating under Section 66D of Information Technology Act, 2000 & Section 420 of Indian Penal Code (IPC).

RESPECTED SIR/MADAM,

I, {payload.victim_name}, residing at {payload.victim_city or 'India'}, Contact: {payload.victim_phone}, hereby submit this formal complaint regarding online job fraud perpetrated against me.

1. PARTICULARS OF THE SUSPECTED ENTITY:
   - Impersonated Employer / Entity: {payload.suspect_name or 'Unverified Scammer'}
   - Scammer Contact / Payment Handles: {payload.suspect_contact or 'Unverified Handle'}

2. FINANCIAL EXTORTION / LOSS DETAILS:
   - Financial Loss Incurred: {payload.loss_amount or 'Not specified'}

3. SUMMARY OF INCIDENT & MODUS OPERANDI:
   {payload.incident_description}

4. PRAYER / RELIEF SOUGHT:
   a) Register an FIR under relevant sections of the IT Act and IPC.
   b) Order beneficiary banks to freeze the suspect accounts.
   c) Take appropriate legal action to recover the defrauded amount.

Yours Faithfully,
{payload.victim_name}
Contact: {payload.victim_phone}
Date: {now_str}
"""
    return {"status": "SUCCESS", "complaint_letter": letter}

@app.get("/api/scam-database")
def get_scam_database():
    return {"status": "SUCCESS", "count": len(SCAM_DATABASE_STORE), "scams": SCAM_DATABASE_STORE}

@app.post("/api/report-scam")
def report_scam_endpoint(payload: ReportScamRequest):
    new_report = {
        "id": f"scam_{len(SCAM_DATABASE_STORE)+1:03d}",
        "title": payload.title,
        "company": payload.company,
        "reporter": "Community Contributor",
        "date": "Today",
        "scamType": payload.scam_type or "Community Report",
        "redFlag": payload.details[:120] + "...",
        "modusOperandi": payload.details,
        "financialLoss": "Under Investigation",
        "fakeContacts": payload.contact or "Unspecified",
        "defenseAdvice": "Cease communication and contact 1930 helpline."
    }
    SCAM_DATABASE_STORE.insert(0, new_report)
    return {"status": "SUCCESS", "message": "Scam report successfully submitted to public database.", "data": new_report}

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)


