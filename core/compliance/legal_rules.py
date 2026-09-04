"""
JobGuard Core Compliance - Jurisdictional Labor Law Rules & Statutory Evaluator
Evaluates recruitment and offer letter text against legal frameworks including:
- Indian Information Technology Act (Section 66D - Cheating by Personation)
- US FTC Act (Section 5 - Unfair/Deceptive Practices)
- EU AI Act & GDPR Article 22 (Automated decision safeguards)
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class LegalViolation:
    statute_code: str
    jurisdiction: str  # "IN", "US", "EU", "GLOBAL"
    title: str
    severity: str  # "felony", "misdemeanor", "civil_penalty", "regulatory_breach"
    matched_clause: str
    description: str
    recommended_complaint_authority: str


@dataclass
class JurisdictionalCheck:
    jurisdiction: str
    is_compliant: bool
    violations: List[LegalViolation] = field(default_factory=list)
    statutory_citations: List[str] = field(default_factory=list)


class LegalRuleEvaluator:
    """Evaluates offer text and job postings for statutory employment violations."""

    LEGAL_DATABASE = [
        {
            "code": "IT_ACT_66D",
            "jurisdiction": "IN",
            "title": "IT Act Section 66D - Cheating by Impersonation via Computer Resource",
            "severity": "felony",
            "pattern": r"\b(registration fee|security deposit|refundable fee|pay.*before interview|task recharge|like videos to earn)\b",
            "description": "Demanding fees or task recharges by masquerading as legitimate corporate employers constitutes punishable cyber fraud (up to 3 years imprisonment).",
            "authority": "National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in)"
        },
        {
            "code": "US_FTC_SEC5",
            "jurisdiction": "US",
            "title": "FTC Act Section 5 - Deceptive Equipment Check & Work-From-Home Scam",
            "severity": "civil_penalty",
            "pattern": r"\b(deposit the.*check|cashier'?s check|wire transfer to.*vendor|purchase.*materials from.*vendor)\b",
            "description": "Fake check equipment schemes and deceptive earnings claims violate Federal Trade Commission business opportunity rules.",
            "authority": "FTC Fraud Division (reportfraud.ftc.gov) & FBI IC3 (ic3.gov)"
        },
        {
            "code": "GDPR_ART22",
            "jurisdiction": "EU",
            "title": "GDPR Article 22 - Solely Automated Candidate Profiling & Rejection",
            "severity": "regulatory_breach",
            "pattern": r"\b(automated decision final|no human appeal permitted|instant rejection by algorithm without recourse)\b",
            "description": "Candidates retain right to human intervention and meaningful explanation for significant automated employment decisions.",
            "authority": "National Data Protection Authority (DPA)"
        },
        {
            "code": "MIN_WAGE_ACT",
            "jurisdiction": "GLOBAL",
            "title": "Statutory Minimum Wage & Unpaid Mandatory Training Prohibition",
            "severity": "misdemeanor",
            "pattern": r"\b(unpaid training for \d+ (months|weeks)|pay for mandatory training material)\b",
            "description": "Employers are legally obligated to bear all mandatory training expenses and pay standard wages.",
            "authority": "Ministry / Department of Labor"
        }
    ]

    def __init__(self):
        self._compiled = [
            (item, re.compile(item["pattern"], re.IGNORECASE))
            for item in self.LEGAL_DATABASE
        ]

    def evaluate(self, text: str, target_jurisdiction: str = "ALL") -> List[JurisdictionalCheck]:
        """Evaluate text against relevant jurisdictional statutes."""
        violations_by_jur: Dict[str, List[LegalViolation]] = {"IN": [], "US": [], "EU": [], "GLOBAL": []}
        citations_by_jur: Dict[str, List[str]] = {"IN": [], "US": [], "EU": [], "GLOBAL": []}

        for item, pat in self._compiled:
            jur = item["jurisdiction"]
            if target_jurisdiction != "ALL" and target_jurisdiction != jur and jur != "GLOBAL":
                continue

            match = pat.search(text)
            if match:
                viol = LegalViolation(
                    statute_code=item["code"],
                    jurisdiction=jur,
                    title=item["title"],
                    severity=item["severity"],
                    matched_clause=match.group(0),
                    description=item["description"],
                    recommended_complaint_authority=item["authority"]
                )
                violations_by_jur[jur].append(viol)
                citations_by_jur[jur].append(item["code"])

        results = []
        for jur, viols in violations_by_jur.items():
            if target_jurisdiction == "ALL" or target_jurisdiction == jur or jur == "GLOBAL":
                results.append(JurisdictionalCheck(
                    jurisdiction=jur,
                    is_compliant=len(viols) == 0,
                    violations=viols,
                    statutory_citations=citations_by_jur[jur]
                ))

        return results
