"""
JobGuard Backend Service - Candidate Protection & Safety Advisor
Provides real-time interactive risk mitigation advice, personalized defensive guidance,
and crisis hotlines for job seekers navigating suspicious recruitment offers.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SafetyGuidanceReport:
    session_id: str
    risk_level: str  # 'SAFE', 'MODERATE_CAUTION', 'CRITICAL_DANGER'
    primary_threat: str
    actionable_advice_steps: List[str]
    sample_response_message_to_recruiter: str
    legal_statutory_rights: List[str]
    emergency_reporting_contacts: Dict[str, str]


class CandidateProtectionAdvisor:
    """Synthesizes humanized and legally grounded advice for candidates."""

    def __init__(self):
        pass

    def evaluate_and_advise(
        self,
        risk_score: float,
        detected_categories: List[str],
        claimed_company: str = "the employer"
    ) -> SafetyGuidanceReport:
        """Generates clear, empowering guidance and message templates for the candidate."""
        categories_upper = [c.upper() for c in detected_categories]

        if risk_score >= 60.0 or any("CHECK" in c or "FEE" in c or "CRYPTO" in c for c in categories_upper):
            level = "CRITICAL_DANGER"
            primary_threat = "Confirmed predatory employment scam (financial extortion / counterfeit check)."
            steps = [
                "1. STOP all communication immediately. Do not send funds, gift cards, or cryptocurrency.",
                "2. DO NOT deposit any check they sent you. If already deposited, notify your bank fraud department right away.",
                "3. DO NOT share your Social Security Number, photo ID, or direct deposit banking login.",
                "4. Report this incident to JobGuard and the FBI Internet Crime Complaint Center (IC3.gov)."
            ]
            response_msg = (
                f"Thank you for the update. Due to enterprise compliance requirements, I cannot process third-party check disbursements "
                f"or submit upfront fees. Please provide an official application link on {claimed_company}'s verified corporate career portal."
            )
        elif risk_score >= 25.0 or any("CHAT" in c or "TELEGRAM" in c for c in categories_upper):
            level = "MODERATE_CAUTION"
            primary_threat = "Unverified recruitment channel / chat-only screening process."
            steps = [
                "1. Request an official video conference (Zoom, Google Meet, MS Teams) with cameras turned on.",
                "2. Require that all emails originate from an authentic corporate domain (not @gmail.com or @yahoo.com).",
                "3. Verify that the open position exists on the official careers page of the company."
            ]
            response_msg = (
                f"Thank you for reaching out regarding the opportunity at {claimed_company}. Before proceeding further with text questionnaires, "
                f"I would appreciate scheduling a brief live video meeting or phone call with the hiring team."
            )
        else:
            level = "SAFE"
            primary_threat = "No major predatory signatures detected."
            steps = [
                "1. Proceed with standard hiring process while maintaining standard privacy safeguards.",
                "2. Confirm contract terms and job duties in writing before commencing employment."
            ]
            response_msg = "Thank you for the information. I look forward to advancing to the next interview stage."

        return SafetyGuidanceReport(
            session_id=f"ADV-SESSION-{risk_score:.0f}",
            risk_level=level,
            primary_threat=primary_threat,
            actionable_advice_steps=steps,
            sample_response_message_to_recruiter=response_msg,
            legal_statutory_rights=[
                "Fair Labor Standards Act (FLSA): Employers cannot charge employees for mandatory tools of the trade.",
                "FTC Act Section 5: Protection against deceptive commercial offers and misrepresentations.",
                "Right to Dispute: You are entitled to contest fraudulent credit inquiries without penalty."
            ],
            emergency_reporting_contacts={
                "JobGuard Safety Center": "safety@jobguard.ai",
                "FTC ReportFraud": "https://reportfraud.ftc.gov",
                "FBI IC3": "https://www.ic3.gov",
                "US Identity Theft Portal": "https://www.identitytheft.gov"
            }
        )
