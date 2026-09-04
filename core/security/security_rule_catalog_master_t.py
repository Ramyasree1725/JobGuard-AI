"""
JobGuard Core Security - Security Rule Catalog Master Volume T
Contains behavioral detection signatures for synthetic job board API scraping tokens,
unauthorized LinkedIn inMail scraping automation, and resume parsing webhook exploits.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleT:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterT:
    """Master expanded catalog of behavioral detection rules volume T."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleT] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_t()

    def _seed_rules_t() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-T-001",
                "Automated Recruiter Bot Session Token Leak",
                "BOTNET_ACTIVITY",
                93.0,
                r"(?:bot_session_id|recruiter_scrape_token)\s*=\s*[\"'][a-zA-Z0-9_\-\.]{32,}[\"']",
                1,
                "Block automated bot scraping sessions and revoke compromised recruiter API session tokens.",
                "Detects hardcoded bot scraper session tokens in malicious browser extensions or automated scrapers."
            ),
            (
                "RULE-T-002",
                "Fake Video Interview Recording Consent Waiver",
                "PRIVACY_VIOLATION",
                86.0,
                r"(?:unrestricted\s+biometric\s+voice\s+and\s+facial\s+data\s+commercial\s+licensing\s+grant)",
                1,
                "Do not sign broad biometric licensing grants on interview screening forms.",
                "Detects predatory clauses granting scam platforms unlimited rights to use candidate voice and video for AI training."
            ),
            (
                "RULE-T-003",
                "Simulated Employee Stock Option Purchase Advance Fee",
                "SECURITIES_FRAUD",
                98.0,
                r"(?:purchase|exercise)\s+(?:discounted|pre-ipo)\s+employee\s+stock\s+options\s+for\s+\$?\d+\s+prior\s+to\s+start\s+date",
                1,
                "Refuse payment. Pre-employment option purchases before commencing employment violate federal securities laws.",
                "Detects fraudulent demands requiring new hires to wire personal funds for advance stock option purchases."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleT(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleT]:
        """Scans input text against all compiled volume T rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
