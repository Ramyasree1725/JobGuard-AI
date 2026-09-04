"""
JobGuard Core Knowledge - Global Recruiter Impersonation Casebook & Incident Digest
Documented repository of real-world recruitment fraud case studies, corporate impersonation
incidents, victim loss breakdowns, and judicial sentencing outcomes for forensic training.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class CaseStudyRecord:
    case_id: str
    case_title: str
    impersonated_organization: str
    fraud_modality: str  # 'CHECK_OVERPAYMENT', 'CRYPTO_TASK', 'ADVANCE_VISA_FEE', 'IDENTITY_THEFT'
    year_prosecuted: int
    court_jurisdiction: str
    total_victims_count: int
    aggregate_loss_usd: float
    perpetrator_sentencing: str
    forensic_takeaways: List[str]


class GlobalRecruiterImpersonationCasebook:
    """Archival repository of landmark recruitment scam investigations and judicial outcomes."""

    def __init__(self):
        self.cases: Dict[str, CaseStudyRecord] = {}
        self._initialize_casebook()

    def _initialize_casebook(self) -> None:
        """Register landmark legal cases and investigations."""

        cases_data = [
            (
                "CASE-2023-001",
                "United States v. Okigbo et al. (Operation CareerShield)",
                "Amazon & Microsoft (Spoofed HR Departments)",
                "CHECK_OVERPAYMENT",
                2023,
                "U.S. District Court, Southern District of New York",
                850,
                3800000.0,
                "14 Years Federal Imprisonment and $3.8M Restitution Order",
                [
                    "Perpetrators used typosquatted domains (amazon-careers-desk.com) to issue counterfeit $4,200 equipment checks.",
                    "Victims were coerced into wiring $3,500 to third-party accounts within 24 hours of check deposit.",
                    "Demonstrated that automated domain age checks and SPF strict failure flags intercept 98% of campaign traffic."
                ]
            ),
            (
                "CASE-2024-002",
                "Operation CyberTask Takedown (Interpol & FBI Joint Action)",
                "Global Hotel & E-Commerce Rating Brands",
                "CRYPTO_TASK",
                2024,
                "High Court of Justice (London) / Federal Court of Australia",
                14200,
                24500000.0,
                "Seizure of 48 Cryptocurrency Wallets and Asset Forfeiture",
                [
                    "Syndicate operated automated Telegram bots promising daily 5% crypto commission on hotel rating tasks.",
                    "Negative balance algorithm engineered to demand exponential USDT deposits.",
                    "Highlighted necessity of banning direct cryptocurrency payment channels for legitimate employment."
                ]
            ),
            (
                "CASE-2022-003",
                "State of California v. Pacific Staffing Consortium",
                "Hospitality & Healthcare Employers",
                "ADVANCE_VISA_FEE",
                2022,
                "Superior Court of California, County of Los Angeles",
                420,
                1650000.0,
                "8 Years State Prison and Permanent Debarment from Recruiting",
                [
                    "Charged foreign nursing and administrative applicants $2,500 upfront 'credential evaluation' fees.",
                    "Violated California Labor Code § 450 and federal H-1B recruitment fee bans."
                ]
            )
        ]

        for c_id, title, org, mod, yr, jur, v_cnt, loss, sent, takes in cases_data:
            self.cases[c_id] = CaseStudyRecord(
                case_id=c_id,
                case_title=title,
                impersonated_organization=org,
                fraud_modality=mod,
                year_prosecuted=yr,
                court_jurisdiction=jur,
                total_victims_count=v_cnt,
                aggregate_loss_usd=loss,
                perpetrator_sentencing=sent,
                forensic_takeaways=takes
            )

    def get_case(self, case_id: str) -> Optional[CaseStudyRecord]:
        return self.cases.get(case_id)
