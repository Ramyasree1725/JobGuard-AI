"""
JobGuard Core Security - Security Rule Catalog Master Volume M
Contains behavioral signatures for detecting synthetic video interview deepfake cues,
virtual background spoofing, and automated voice synthesizers in hiring evaluations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleM:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterM:
    """Master expanded catalog of behavioral detection rules volume M."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleM] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_m()

    def _seed_rules_m() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-M-001",
                "Voice Call Only No-Camera Evaluation Lure",
                "INTERVIEW_ANOMALY",
                75.0,
                r"(?:video\s+camera\s+is\s+not\s+required|voice\s+call\s+only\s+interview\s+via\s+phone)",
                1,
                "Insist on multi-party video evaluation with official corporate meeting links.",
                "Detects recruiters declining video calls to mask overseas accent or synthetic voice impersonation."
            ),
            (
                "RULE-M-002",
                "Third-Party Crypto Exchange Account Onboarding",
                "FINANCIAL_CRIME",
                99.0,
                r"(?:create|register)\s+(?:an\s+account\s+on|with)\s+(?:binance|coinbase|kraken|bybit)\s+for\s+company\s+disbursements",
                1,
                "Immediate critical alert. Employers use domestic automated clearing house (ACH) bank deposits.",
                "Detects instructions ordering prospective employees to create cryptocurrency exchange accounts for wage disbursement."
            ),
            (
                "RULE-M-003",
                "Personal Bank Account Usage for Company Logistics",
                "MONEY_LAUNDERING",
                99.0,
                r"(?:use|provide)\s+your\s+personal\s+bank\s+account\s+to\s+(?:process|receive)\s+client\s+(?:payments|wires|funds)",
                1,
                "CRITICAL: Unlawful money mule activity. Using personal accounts for company funds constitutes criminal money laundering.",
                "Detects recruitment of financial money mules to receive and transfer illicit funds."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleM(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleM]:
        """Scans input text against all compiled volume M rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
