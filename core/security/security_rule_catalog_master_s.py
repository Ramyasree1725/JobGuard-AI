"""
JobGuard Core Security - Security Rule Catalog Master Volume S
Contains behavioral detection signatures for simulated background check clearance tokens,
third-party identity verification API spoofing, and unverified notary portal credentials.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleS:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterS:
    """Master expanded catalog of behavioral detection rules volume S."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleS] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_s()

    def _seed_rules_s() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-S-001",
                "Simulated Identity Verification Token Purchase",
                "IDENTITY_FRAUD",
                97.0,
                r"(?:purchase|buy)\s+(?:a\s+)?(?:candidate|employment|id)\s+(?:verification|clearance)\s+token\s+for\s+\$?\d+",
                1,
                "Refuse payment. Legitimate corporate identity verification (e.g. Persona, ID.me) is 100% employer-funded.",
                "Detects demands requiring candidates to buy proprietary identity clearance tokens or voucher codes."
            ),
            (
                "RULE-S-002",
                "Lookalike Identity Verification Domain Lure",
                "PHISHING_INFRASTRUCTURE",
                95.0,
                r"https?://(?:verify-persona|idme-candidate-portal|checkr-verification)-[a-z0-9]+\.[a-z]{2,}",
                1,
                "Do not submit biometric scans or ID photos. Confirm verification link on official vendor domain.",
                "Detects typosquatted identity verification domains engineered to harvest biometric facial scans and government IDs."
            ),
            (
                "RULE-S-003",
                "Remote Notarization Fee Shifting Mandate",
                "FEE_SHIFTING",
                89.0,
                r"(?:candidate|applicant)\s+must\s+(?:remit|pay)\s+\$?\d+\s+for\s+remote\s+online\s+notarization",
                1,
                "Notify recruiter that remote notarization fees for employment onboarding must be borne by the employer.",
                "Detects unlawful fee shifting for mandatory pre-employment document notarizations."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleS(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleS]:
        """Scans input text against all compiled volume S rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
