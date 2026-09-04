"""
JobGuard Core Security - Security Rule Catalog Master Volume X
Contains behavioral detection signatures for synthetic recruiter phone number spoofing,
unverified VoIP telephony carriers, and disposable SMS verification gateway abuse.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleX:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterX:
    """Master expanded catalog of behavioral detection rules volume X."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleX] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_x()

    def _seed_rules_x() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-X-001",
                "Disposable VoIP Recruiter Phone Number Lure",
                "TELEPHONY_SPOOFING",
                82.0,
                r"(?:text|sms)\s+our\s+hiring\s+team\s+at\s+\+?1?\s*\(?(?:textnow|google\s+voice|bandwidth\.com)\)?",
                1,
                "Request formal phone meeting via verified corporate enterprise switchboard number.",
                "Detects recruiters operating exclusively via disposable consumer VoIP numbers."
            ),
            (
                "RULE-X-002",
                "Candidate Bank Account Micro-Deposit Reversal Lure",
                "BANKING_EXPLOIT",
                97.0,
                r"(?:we\s+sent|deposited)\s+two\s+micro-deposits\s+to\s+your\s+account.*(?:wire|send)\s+them\s+back\s+immediately",
                1,
                "Do not send money back. Automated micro-deposit verifications do not require manual return wires.",
                "Detects social engineering attempts tricking candidates into sending funds following automated micro-deposits."
            ),
            (
                "RULE-X-003",
                "Pre-Employment Equipment Insurance Policy Mandate",
                "INSURANCE_EXTORTION",
                94.0,
                r"(?:candidate|employee)\s+must\s+purchase\s+(?:a\s+)?remote\s+equipment\s+insurance\s+policy\s+of\s+\$?\d+",
                1,
                "Refuse payment. Corporate equipment insurance is 100% employer-funded and covered under enterprise commercial policies.",
                "Detects extortion demands requiring candidates to buy third-party equipment insurance before dispatch."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleX(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleX]:
        """Scans input text against all compiled volume X rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
