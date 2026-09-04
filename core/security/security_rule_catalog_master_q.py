"""
JobGuard Core Security - Security Rule Catalog Master Volume Q
Contains behavioral signatures for detecting lookalike corporate career subdomains,
unvalidated URL query parameter redirects, and suspicious email header reply-to mismatches.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleQ:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterQ:
    """Master expanded catalog of behavioral detection rules volume Q."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleQ] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_q()

    def _seed_rules_q() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-Q-001",
                "Email Header Reply-To Corporate Domain Mismatch",
                "EMAIL_AUTHENTICATION",
                92.0,
                r"(?:From:\s+.*@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})).*(?:Reply-To:\s+.*@(?!\1)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
                1,
                "Do not reply. Inspect raw email headers to confirm sender domain alignment.",
                "Detects spoofed sender headers where replies are silently redirected to a scammer-controlled mailbox."
            ),
            (
                "RULE-Q-002",
                "ATS Confirmation Open Redirect Parameter",
                "WEB_EXPLOITATION",
                78.0,
                r"https?://(?:[a-zA-Z0-9.-]+\.)?(?:workday|greenhouse|lever)\.com/.*[?&]next=https?://[a-zA-Z0-9.-]+",
                1,
                "Inspect URL parameters before clicking redirect links following job application submission.",
                "Detects unvalidated redirect parameters appended to genuine ATS confirmation URLs."
            ),
            (
                "RULE-Q-003",
                "Hyphenated Lookalike Enterprise Brand Domain",
                "DOMAIN_TYPOSQUATTING",
                91.0,
                r"https?://(?:[a-zA-Z0-9]+-)+(?:careers|jobs|recruitment|talent|hiring)\.[a-z]{2,}",
                1,
                "Navigate directly to the official corporate website and search for the requisition ID.",
                "Detects hyphenated lookalike domains engineered to mimic Fortune 500 career portals."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleQ(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleQ]:
        """Scans input text against all compiled volume Q rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
