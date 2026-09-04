"""
JobGuard Core Security - Security Rule Catalog Master Volume P
Contains behavioral detection signatures for synthetic AI-generated recruiter headshots,
lookalike corporate logo vector overlays, and deceptive employment authorization badges.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleP:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterP:
    """Master expanded catalog of behavioral detection rules volume P."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleP] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_p()

    def _seed_rules_p() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-P-001",
                "Simulated US Work Authorization Badge Lure",
                "IMMIGRATION_DECEPTION",
                88.0,
                r"(?:we\s+issue|provide)\s+(?:instant|expedited)\s+uscis\s+(?:work\s+permits?|ead\s+cards?|sponsorship\s+badges?)\s+upon\s+payment",
                1,
                "Immediate fraud alert. USCIS work authorization can never be purchased directly from private recruiters.",
                "Detects claims by fraudulent overseas recruitment agencies offering instant US work authorization cards for purchase."
            ),
            (
                "RULE-P-002",
                "Synthetic Corporate Seal Watermark Claim",
                "DOCUMENT_FABRICATION",
                85.0,
                r"(?:authenticated|guaranteed)\s+by\s+(?:the\s+global\s+corporate\s+hiring\s+seal|united\s+states\s+recruitment\s+board)",
                1,
                "Cross-reference corporate issuer against official federal registry.",
                "Detects fabricated corporate seal watermarks added to scam offer letters."
            ),
            (
                "RULE-P-003",
                "Unregistered Overseas Employment Intermediary Lure",
                "UNLICENSED_AGENCY",
                92.0,
                r"(?:unlicensed|private)\s+overseas\s+staffing\s+without\s+(?:dmw|poea|emigrate|glaa)\s+clearance",
                1,
                "Demand official state emigration registry verification number before sharing documents.",
                "Detects overseas employment recruiters operating without statutory accreditation."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleP(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleP]:
        """Scans input text against all compiled volume P rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
