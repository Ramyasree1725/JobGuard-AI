"""
JobGuard Core Security - Security Rule Catalog Master Volume G
Contains comprehensive signatures for detecting fake ATS portals, OAuth consent phishing,
subdomain impersonation, and fraudulent candidate screening forms.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleG:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterG:
    """Master expanded catalog of behavioral detection rules volume G."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleG] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_g()

    def _seed_rules_g(self) -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-G-001",
                "Lookalike ATS Subdomain Spoofing",
                "DOMAIN_SPOOFING",
                90.0,
                r"https?://(?:boards-greenhouse|jobs-lever|workday-apply)-[a-z0-9]+\.(?:com|org|net|info)",
                1,
                "Block domain and navigate exclusively to verified employer careers page.",
                "Detects synthetic lookalike ATS domains designed to deceive candidates into submitting resumes."
            ),
            (
                "RULE-G-002",
                "Third-Party Form Processor Webhook Lure",
                "FORM_PHISHING",
                75.0,
                r"<form\s+action=[\"']https?://(?:formspree\.io|formkeep\.com|typeform\.com/to)/[a-zA-Z0-9]+",
                1,
                "Verify form origin. Enterprise employers host applications directly on dedicated ATS infrastructure.",
                "Detects application questionnaires submitting candidate dossiers to unverified third-party form webhooks."
            ),
            (
                "RULE-G-003",
                "OAuth Consent Phishing for Cloud Storage",
                "CREDENTIAL_PHISHING",
                95.0,
                r"(?:grant|authorize)\s+(?:access|permission)\s+to\s+your\s+(?:google\s+drive|onedrive|dropbox)\s+for\s+interview",
                1,
                "Do not grant third-party OAuth permissions to interview applications.",
                "Detects malicious OAuth consent apps requesting full read/write access to candidate cloud drives."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleG(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleG]:
        """Scans input text against all compiled volume G rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
