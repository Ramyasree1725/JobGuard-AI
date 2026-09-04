"""
JobGuard Core Security - Security Rule Catalog Master Volume Y
Contains behavioral detection signatures for simulated background check clearance tokens,
fake corporate training LMS paywalls, and unverified digital signature validation requests.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleY:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterY:
    """Master expanded catalog of behavioral detection rules volume Y."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleY] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_y()

    def _seed_rules_y() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-Y-001",
                "Pre-Employment LMS Training Paywall Lure",
                "TRAINING_PAYWALL",
                95.0,
                r"(?:complete|enroll\s+in)\s+mandatory\s+pre-employment\s+(?:certification|training\s+module)\s+for\s+\$?\d+",
                1,
                "Refuse payment. Mandatory pre-employment training is legally an employer-funded expense under the Fair Labor Standards Act.",
                "Detects extortion schemes requiring candidates to pay for private LMS training courses before hiring."
            ),
            (
                "RULE-Y-002",
                "Lookalike LMS Portal Authentication Lure",
                "CREDENTIAL_PHISHING",
                93.0,
                r"https?://(?:cornerstone-careers|workday-learning|udemy-enterprise)-[a-z0-9]+\.[a-z]{2,}/login",
                1,
                "Do not enter passwords. Verify learning portal URLs with official corporate IT support.",
                "Detects typosquatted Learning Management System portals engineered to harvest corporate candidate logins."
            ),
            (
                "RULE-Y-003",
                "Simulated Drug Screening Clearance Voucher Fee",
                "FEE_SHIFTING",
                91.0,
                r"(?:purchase|pay\s+for)\s+(?:a\s+)?pre-employment\s+drug\s+(?:screen|test)\s+voucher\s+of\s+\$?\d+",
                1,
                "Notify recruiter that pre-employment drug screening vouchers must be provided at employer expense.",
                "Detects unlawful fee shifting for mandatory pre-employment drug screening tests."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleY(
                rule_id=r_id,
                rule_name=name,
                category=cat,
                risk_score_impact=impact,
                regex_pattern=pat,
                min_word_match_threshold=min_w,
                remediation_action=rem,
                technical_description=desc
            )
            self.rules[r_id] = rule
            self._compiled[r_id] = re.compile(pat, re.IGNORECASE)

    def scan_text(self, text: str) -> List[MasterSecurityRuleY]:
        """Scans input text against all compiled volume Y rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
