"""
JobGuard Core Security - Security Rule Catalog Master Volume U
Contains behavioral detection signatures for simulated tax compliance audits,
unauthorized digital signature validation requests, and candidate hardware tracking tokens.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleU:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterU:
    """Master expanded catalog of behavioral detection rules volume U."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleU] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_u()

    def _seed_rules_u() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-U-001",
                "Simulated IRS / State Tax Audit Fee Lure",
                "TAX_EXTORTION",
                97.0,
                r"(?:irs|state\s+tax\s+franchise\s+board)\s+requires\s+(?:a\s+)?pre-employment\s+tax\s+compliance\s+clearance\s+fee\s+of\s+\$?\d+",
                1,
                "Refuse payment. The IRS and state tax boards never require job candidates to pay pre-employment tax clearance fees.",
                "Detects extortion demands claiming government tax authorities require pre-employment tax compliance fees."
            ),
            (
                "RULE-U-002",
                "Hardware Serial Number Verification Deposit",
                "ADVANCE_FEE",
                94.0,
                r"(?:register|authenticate)\s+your\s+personal\s+laptop\s+serial\s+number\s+for\s+\$?\d+\s+security\s+deposit",
                1,
                "Refuse payment. Enterprise employers configure MDM (Mobile Device Management) at zero cost to employees.",
                "Detects demands requiring candidates to pay a security deposit to register their personal hardware serial numbers."
            ),
            (
                "RULE-U-003",
                "Unverified Digital E-Signature Service Redirection",
                "PHISHING_LINK",
                91.0,
                r"https?://(?:docusign-verification|hellosign-careers|adobesign-portal)-[a-z0-9]+\.[a-z]{2,}/sign",
                1,
                "Do not enter passwords or sign documents. Access e-signature requests only from official vendor notification emails.",
                "Detects typosquatted e-signature portals engineered to harvest candidate email logins and signatures."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleU(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleU]:
        """Scans input text against all compiled volume U rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
