"""
JobGuard Core Recommendation - Incident Response Playbook Repository
Provides actionable step-by-step incident containment procedures for victims
of bounced fake checks, identity theft dossiers, compromised banking credentials,
and extortion or harassment threats.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class IncidentType(Enum):
    BOUNCED_FAKE_CHECK = "BOUNCED_FAKE_CHECK"
    COMPROMISED_SSN_ID = "COMPROMISED_SSN_ID"
    UNAUTHORIZED_BANK_DRAIN = "UNAUTHORIZED_BANK_DRAIN"
    EXTORTION_THREAT = "EXTORTION_THREAT"
    ACCIDENTAL_PACKAGE_MULE = "ACCIDENTAL_PACKAGE_MULE"


@dataclass
class PlaybookStep:
    step_number: int
    action_title: str
    target_institution: str
    script_template: str
    urgency_minutes: int
    statute_reference: str


@dataclass
class IncidentPlaybook:
    incident_type: IncidentType
    playbook_title: str
    severity_level: str
    estimated_recovery_time_days: int
    steps: List[PlaybookStep]
    reporting_authorities: List[str]


class IncidentResponsePlaybookRepository:
    """Provides playbooks and phone scripts for victims in active scam crises."""

    def __init__(self):
        self.playbooks: Dict[IncidentType, IncidentPlaybook] = {}
        self._initialize_playbooks()

    def _initialize_playbooks(self) -> None:
        """Register playbooks for all major recruitment fraud incident scenarios."""

        # 1. Bounced Fake Check
        self.playbooks[IncidentType.BOUNCED_FAKE_CHECK] = IncidentPlaybook(
            incident_type=IncidentType.BOUNCED_FAKE_CHECK,
            playbook_title="Counterfeit Employment Check Deposit Remediation",
            severity_level="CRITICAL",
            estimated_recovery_time_days=14,
            steps=[
                PlaybookStep(
                    step_number=1,
                    action_title="Call Bank Fraud Department",
                    target_institution="Your Bank / Credit Union",
                    script_template="Hello, I believe I was the victim of a recruitment scam and inadvertently deposited a fraudulent check (Check #{check_num}) on {date}. I have not spent the funds and request that the check be intercepted before chargeback fees are assessed.",
                    urgency_minutes=30,
                    statute_reference="UCC § 4-214 - Right of Charge-Back or Refund"
                ),
                PlaybookStep(
                    step_number=2,
                    action_title="Freeze Mobile Deposit Feature",
                    target_institution="Your Bank",
                    script_template="Please place a temporary security hold on incoming check deposits to ensure no unauthorized items clear.",
                    urgency_minutes=120,
                    statute_reference="Electronic Fund Transfer Act (EFTA)"
                ),
                PlaybookStep(
                    step_number=3,
                    action_title="File Police Incident Report",
                    target_institution="Local Police Precinct",
                    script_template="I need to file a formal report for check fraud by an impersonated employer for submission to my bank's fraud investigator.",
                    urgency_minutes=1440,
                    statute_reference="18 U.S. Code § 1344 - Bank Fraud"
                )
            ],
            reporting_authorities=["Federal Trade Commission (ReportFraud.ftc.gov)", "FBI Internet Crime Complaint Center (IC3.gov)", "US Postal Inspection Service (USPIS)"]
        )

        # 2. Compromised SSN & ID
        self.playbooks[IncidentType.COMPROMISED_SSN_ID] = IncidentPlaybook(
            incident_type=IncidentType.COMPROMISED_SSN_ID,
            playbook_title="Government ID & SSN Compromise Containment",
            severity_level="HIGH",
            estimated_recovery_time_days=30,
            steps=[
                PlaybookStep(
                    step_number=1,
                    action_title="Place Extended Fraud Alert",
                    target_institution="Experian, TransUnion, Equifax",
                    script_template="Place a 7-year extended fraud alert and credit freeze on my credit file. I am a victim of identity theft.",
                    urgency_minutes=60,
                    statute_reference="Fair Credit Reporting Act (FCRA) § 605A"
                ),
                PlaybookStep(
                    step_number=2,
                    action_title="Create IdentityTheft.gov Recovery Plan",
                    target_institution="FTC Identity Theft Portal",
                    script_template="Complete online affidavit on IdentityTheft.gov to generate official FTC Identity Theft Report.",
                    urgency_minutes=180,
                    statute_reference="FTC Identity Theft Red Flags Rule"
                ),
                PlaybookStep(
                    step_number=3,
                    action_title="Lock Social Security Number with SSA",
                    target_institution="Social Security Administration (SSA)",
                    script_template="Enroll in SSA e-Verify Self Lock to prevent unauthorized electronic employment verification requests.",
                    urgency_minutes=360,
                    statute_reference="Social Security Act § 208"
                )
            ],
            reporting_authorities=["IdentityTheft.gov", "Social Security Administration Fraud Hotline", "State Attorney General Consumer Protection"]
        )

        # 3. Accidental Package Mule
        self.playbooks[IncidentType.ACCIDENTAL_PACKAGE_MULE] = IncidentPlaybook(
            incident_type=IncidentType.ACCIDENTAL_PACKAGE_MULE,
            playbook_title="Reshipping / Package Mule Operation Extrication",
            severity_level="CRITICAL",
            estimated_recovery_time_days=7,
            steps=[
                PlaybookStep(
                    step_number=1,
                    action_title="Cease All Forwarding Immediately",
                    target_institution="Home Residence",
                    script_template="Do not open, re-box, or ship any packages currently at your address. Keep them untouched in a secure area.",
                    urgency_minutes=15,
                    statute_reference="18 U.S. Code § 1708 - Theft or Receipt of Stolen Mail"
                ),
                PlaybookStep(
                    step_number=2,
                    action_title="Contact USPIS Postal Inspectors",
                    target_institution="U.S. Postal Inspection Service",
                    script_template="Report that a fraudulent work-from-home employer sent packages purchased with stolen credit cards to your address under false pretenses.",
                    urgency_minutes=60,
                    statute_reference="Postal Reorganization Act"
                )
            ],
            reporting_authorities=["US Postal Inspection Service", "IC3.gov", "Local Law Enforcement"]
        )

    def get_playbook(self, incident: IncidentType) -> Optional[IncidentPlaybook]:
        return self.playbooks.get(incident)
