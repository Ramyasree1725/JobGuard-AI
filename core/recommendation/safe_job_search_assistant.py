"""
JobGuard Core Recommendation - Safe Job Search & Recruiter Routing Assistant
Provides trusted career endpoint directories, interview security checklists,
and verified direct company career hub discovery for job seekers worldwide.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class VerifiedCareerHub:
    company_name: str
    official_root_url: str
    official_careers_url: str
    verified_ats_subdomain: str
    recruiter_contact_email: str
    fraud_alert_page: Optional[str] = None


@dataclass
class SafetyChecklist:
    checklist_id: str
    stage_name: str
    mandatory_verification_points: List[str]
    red_flag_warnings: List[str]
    emergency_contact: str


class SafeJobSearchAssistant:
    """Guides job seekers to authentic application portals and provides safe hiring checklists."""

    def __init__(self):
        self.verified_hubs: Dict[str, VerifiedCareerHub] = {}
        self._initialize_hubs()

    def _initialize_hubs(self) -> None:
        """Register verified hiring hubs for global enterprise employers."""

        self.verified_hubs["google"] = VerifiedCareerHub(
            company_name="Google",
            official_root_url="https://www.google.com",
            official_careers_url="https://careers.google.com",
            verified_ats_subdomain="careers.google.com",
            recruiter_contact_email="careers@google.com",
            fraud_alert_page="https://support.google.com/faqs/answer/6328224"
        )

        self.verified_hubs["microsoft"] = VerifiedCareerHub(
            company_name="Microsoft",
            official_root_url="https://www.microsoft.com",
            official_careers_url="https://careers.microsoft.com",
            verified_ats_subdomain="careers.microsoft.com",
            recruiter_contact_email="staffing@microsoft.com"
        )

        self.verified_hubs["amazon"] = VerifiedCareerHub(
            company_name="Amazon",
            official_root_url="https://www.amazon.com",
            official_careers_url="https://www.amazon.jobs",
            verified_ats_subdomain="amazon.jobs",
            recruiter_contact_email="recruiting@amazon.com"
        )

        self.verified_hubs["apple"] = VerifiedCareerHub(
            company_name="Apple",
            official_root_url="https://www.apple.com",
            official_careers_url="https://jobs.apple.com",
            verified_ats_subdomain="jobs.apple.com",
            recruiter_contact_email="careers@apple.com"
        )

    def get_interview_safety_checklist(self) -> SafetyChecklist:
        """Returns the gold-standard 5-point verification checklist before signing an offer."""
        return SafetyChecklist(
            checklist_id="CHK-INT-001",
            stage_name="Pre-Offer & Interview Verification",
            mandatory_verification_points=[
                "Confirm recruiter email domain matches the exact official corporate website (e.g. @google.com, NOT @google-jobs.com or @gmail.com).",
                "Insist on a live interactive video interview via Google Meet, Zoom, or Teams with cameras enabled.",
                "Verify the job listing directly on the company's official career portal (e.g. company.com/careers).",
                "Ensure zero upfront fees are requested for background checks, onboarding software, or equipment shipping.",
                "Verify that no check has been mailed with instructions to transfer surplus funds back to an 'approved vendor'."
            ],
            red_flag_warnings=[
                "Interview conducted solely via Telegram, WhatsApp, or Signal text chat.",
                "Immediate job offer received within hours without a live technical or behavioral interview.",
                "Employer sends a check for thousands of dollars and instructs you to buy equipment from a specific vendor.",
                "Payment requested via Bitcoin, Zelle, CashApp, or retail gift cards."
            ],
            emergency_contact="JobGuard 24/7 Security Advisory Hub: support@jobguard.ai"
        )

    def route_to_official_career_portal(self, company_name: str) -> Optional[VerifiedCareerHub]:
        """Looks up authentic direct application portal for a target employer."""
        clean_name = company_name.lower().strip()
        for key, hub in self.verified_hubs.items():
            if key in clean_name or hub.company_name.lower() in clean_name:
                return hub
        return None
