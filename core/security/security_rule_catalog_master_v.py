"""
JobGuard Core Security - Security Rule Catalog Master Volume V
Contains behavioral detection signatures for synthetic job aggregator scraping loops,
unauthorized candidate resume data broking, and deceptive talent pool subscription charges.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleV:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterV:
    """Master expanded catalog of behavioral detection rules volume V."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleV] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_v()

    def _seed_rules_v() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-V-001",
                "Talent Pool Monthly Recurring Subscription Lure",
                "SUBSCRIPTION_TRAP",
                90.0,
                r"(?:join|subscribe\s+to)\s+our\s+(?:exclusive|vip)\s+talent\s+pool\s+for\s+\$?\d+/(?:month|mo|year)",
                1,
                "Refuse payment. Legitimate corporate talent acquisition never charges subscription fees to job seekers.",
                "Detects subscription billing traps promising exclusive job interview leads for a recurring monthly fee."
            ),
            (
                "RULE-V-002",
                "Automated Recruiter Webhook Header Injection",
                "WEBHOOK_EXPLOIT",
                92.0,
                r"(?:X-Recruiter-Inbound-Token|X-ATS-Bypass-Signature)\s*:\s*[a-zA-Z0-9_\-\.]{32,}",
                1,
                "Drop inbound webhook requests with invalid or forged HMAC signatures.",
                "Detects forged HTTP headers engineered to bypass applicant screening firewalls."
            ),
            (
                "RULE-V-003",
                "Candidate Resume Scraping Consent Trap",
                "DATA_PRIVACY_EXPLOIT",
                88.0,
                r"(?:by\s+applying,\s+you\s+grant\s+unrestricted\s+permission\s+to\s+sell|resell\s+your\s+resume\s+and\s+contact\s+details\s+to\s+third\s+parties)",
                1,
                "Do not submit application. Legitimate employers never sell candidate resumes to commercial data brokers.",
                "Detects predatory terms of service clauses commercializing candidate resume dossiers."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleV(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleV]:
        """Scans input text against all compiled volume V rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
