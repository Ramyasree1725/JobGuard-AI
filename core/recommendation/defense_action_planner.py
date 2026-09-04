"""
JobGuard Core Recommendation - Dynamic Candidate Defense Action Planner
Generates prioritized, contextual, and step-by-step risk mitigation checklists
customized to the candidate's exact threat exposure level and vulnerability profile.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ActionUrgency(Enum):
    IMMEDIATE_STOP = "IMMEDIATE_STOP"
    WITHIN_24_HOURS = "WITHIN_24_HOURS"
    PRIOR_TO_SIGNING = "PRIOR_TO_SIGNING"
    POST_INCIDENT_MONITORING = "POST_INCIDENT_MONITORING"
    BEST_PRACTICE = "BEST_PRACTICE"


@dataclass
class DefenseActionItem:
    item_id: str
    urgency: ActionUrgency
    title: str
    instructions: str
    rationale: str
    target_vector: str
    is_completed: bool = False
    external_resource_url: Optional[str] = None


@dataclass
class DefensePlan:
    plan_id: str
    aggregate_risk_score: float
    threat_summary: str
    actions: List[DefenseActionItem]
    statutory_rights_summary: str
    candidate_emergency_hotline: str


class DefenseActionPlanner:
    """Generates personalized action plans tailored to detected fraud vectors."""

    def __init__(self):
        pass

    def synthesize_defense_plan(
        self,
        risk_score: float,
        detected_vectors: List[str],
        has_sent_funds: bool = False,
        has_shared_ssn: bool = False,
        has_deposited_check: bool = False
    ) -> DefensePlan:
        """Synthesizes a tailored mitigation action plan based on user state."""
        actions: List[DefenseActionItem] = []

        # 1. Emergency stop actions if money/check is involved
        if has_deposited_check:
            actions.append(DefenseActionItem(
                item_id="ACT-CHK-01",
                urgency=ActionUrgency.IMMEDIATE_STOP,
                title="Immediately Contact Your Bank Fraud Department",
                instructions="Inform your bank that you deposited a counterfeit employment check. Request that the funds be put on hold so your account is not frozen for bank fraud.",
                rationale="Counterfeit checks take 5-10 business days to clear the Federal Reserve. You are personally liable for all withdrawn amounts when it bounces.",
                target_vector="COUNTERFEIT_CHECK",
                external_resource_url="https://www.consumerfinance.gov/consumer-tools/bank-accounts/"
            ))

        if has_sent_funds:
            actions.append(DefenseActionItem(
                item_id="ACT-PAY-01",
                urgency=ActionUrgency.IMMEDIATE_STOP,
                title="Initiate Immediate Wire / Payment Recall",
                instructions="Contact the payment platform (Zelle, CashApp, Wire Department) immediately to submit a fraud recall ticket. File a local police report to obtain an incident number.",
                rationale="Instant payment rails are irrevocable once settled, but immediate flagging can freeze mule recipient accounts.",
                target_vector="FINANCIAL_LOSS",
                external_resource_url="https://www.ic3.gov/"
            ))

        if has_shared_ssn:
            actions.append(DefenseActionItem(
                item_id="ACT-SSN-01",
                urgency=ActionUrgency.WITHIN_24_HOURS,
                title="Place a Free Credit Freeze with Experian, Equifax & TransUnion",
                instructions="Freeze your credit reports online at the three major bureaus to prevent scammers from opening loans or credit cards in your name.",
                rationale="A credit freeze blocks unauthorized credit checks and is free by federal law.",
                target_vector="IDENTITY_THEFT",
                external_resource_url="https://www.identitytheft.gov/"
            ))

        # 2. Vector-specific standard mitigations
        for vec in detected_vectors:
            v_upper = vec.upper()
            if "TELEGRAM" in v_upper or "WHATSAPP" in v_upper or "CHAT" in v_upper:
                actions.append(DefenseActionItem(
                    item_id="ACT-VEC-CHAT",
                    urgency=ActionUrgency.PRIOR_TO_SIGNING,
                    title="Demand Live Video Evaluation with Verified Corporate Recruiter",
                    instructions="Request a formal Zoom/Google Meet video interview with a recruiter using an @company.com official email address. Cease text-only communications.",
                    rationale="Legitimate corporate hiring requires face-to-face visual and identity verification before issuing legal contracts.",
                    target_vector="CHAT_ONLY_INTERVIEW"
                ))
            elif "FEE" in v_upper or "UPFRONT" in v_upper:
                actions.append(DefenseActionItem(
                    item_id="ACT-VEC-FEE",
                    urgency=ActionUrgency.IMMEDIATE_STOP,
                    title="Refuse All Upfront Payments, Deposits, or Background Fees",
                    instructions="Do not send money for laptops, background checks, training, or onboarding software. Reiterate that legitimate employers cover all hiring expenses.",
                    rationale="Federal and state labor laws mandate that employers bear all necessary onboarding and equipment costs.",
                    target_vector="UPFRONT_FEE"
                ))
            elif "DOMAIN" in v_upper or "IMPERSONATION" in v_upper:
                actions.append(DefenseActionItem(
                    item_id="ACT-VEC-DOM",
                    urgency=ActionUrgency.PRIOR_TO_SIGNING,
                    title="Cross-Reference Opportunity on Official Careers Webpage",
                    instructions="Navigate directly to the claimed company's verified website (e.g. google.com/careers) and search for the specific Job ID. Contact public HR phone line.",
                    rationale="Impersonators use lookalike domains (e.g. company-jobs.com) to mimic genuine brands.",
                    target_vector="DOMAIN_IMPERSONATION"
                ))

        # Best practice default
        actions.append(DefenseActionItem(
            item_id="ACT-GEN-01",
            urgency=ActionUrgency.BEST_PRACTICE,
            title="Archive Full Communication Records & Receipts",
            instructions="Export chat transcripts, email headers, contract PDFs, and wire receipts as evidence in case legal reporting or bank dispute is required.",
            rationale="Digital forensics and headers are essential for cybercrime investigators and FTC submissions.",
            target_vector="GENERAL_RECORDKEEPING"
        ))

        # Summary construction
        if risk_score >= 70.0:
            summary = "HIGH FRAUD ALERT: Multiple severe threat signatures detected. Immediate protective intervention required."
        elif risk_score >= 35.0:
            summary = "ELEVATED RISK: Inconsistencies detected in recruitment channel. Do not advance until verified."
        else:
            summary = "LOW RISK: General employment precautions apply."

        return DefensePlan(
            plan_id="PLAN-GEN-001",
            aggregate_risk_score=risk_score,
            threat_summary=summary,
            actions=actions,
            statutory_rights_summary="Under FTC regulations and Fair Credit Reporting Act (FCRA), you have the right to free credit freezes and fraud dispute investigations.",
            candidate_emergency_hotline="FTC Fraud Hotline: 1-877-FTC-HELP (1-877-382-4357)"
        )
