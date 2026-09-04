"""
JobGuard Core Security - Security Rule Catalog Master Volume N
Contains behavioral signatures for detecting fake executive digital signatures,
tampered Adobe Acrobat certificates, and synthetic corporate letterhead graphics.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleN:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterN:
    """Master expanded catalog of behavioral detection rules volume N."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleN] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_n()

    def _seed_rules_n() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-N-001",
                "Altered Document Signing Date Inconsistency",
                "DOCUMENT_FORGERY",
                82.0,
                r"(?:signed|executed)\s+on\s+(?:the\s+)?(?:\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+[A-Za-z]+,\s+20\d\d).*(?:effective\s+immediately|valid\s+for\s+24\s+hours)",
                1,
                "Examine PDF metadata creation date versus displayed contract text date.",
                "Detects chronological discrepancies between digital PDF timestamp creation and printed contract dates."
            ),
            (
                "RULE-N-002",
                "Generic Free Domain Recruiter Footer",
                "EMAIL_AUTHENTICATION",
                90.0,
                r"(?:sent\s+from|email\s+us\s+at)\s+[a-zA-Z0-9._%+-]+@(?:gmail|yahoo|hotmail|outlook|protonmail|aol)\.com",
                1,
                "Refuse communication. Enterprise recruiters communicate exclusively from verified company domains.",
                "Detects corporate recruiters using free public webmail addresses in formal appointment letter footers."
            ),
            (
                "RULE-N-003",
                "Synthetic Notary Registration Seal Claim",
                "DOCUMENT_FORGERY",
                88.0,
                r"(?:registered\s+with\s+the\s+global\s+notarial\s+council|official\s+federal\s+employment\s+seal)",
                1,
                "Cross-reference corporate entity with state Secretary of State corporate registry.",
                "Detects fictitious regulatory or notarial council seals applied to scam employment agreements."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleN(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleN]:
        """Scans input text against all compiled volume N rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
