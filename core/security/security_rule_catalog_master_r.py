"""
JobGuard Core Security - Security Rule Catalog Master Volume R
Contains behavioral detection signatures for simulated embassy interview appointments,
fake consular security deposits, and unauthorized international wire remittance instructions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleR:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterR:
    """Master expanded catalog of behavioral detection rules volume R."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleR] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_r()

    def _seed_rules_r() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-R-001",
                "Simulated Embassy Appointment Booking Fee",
                "IMMIGRATION_FRAUD",
                96.0,
                r"(?:embassy|consulate|visa\s+center)\s+(?:appointment|slot|booking)\s+fee\s+of\s+\$?\d+",
                1,
                "Do not pay private recruiters for embassy appointments. Use official government consular portals.",
                "Detects demands for advance payments to secure embassy interview appointment slots."
            ),
            (
                "RULE-R-002",
                "Personal Foreign Bank Wire Routing for Tax Withholding",
                "FINANCIAL_CRIME",
                97.0,
                r"(?:wire|remit)\s+(?:foreign|international)\s+tax\s+withholding\s+to\s+account\s*:\s*[A-Z0-9]{15,34}",
                1,
                "Refuse international wire payments for tax. Sovereign tax authorities never accept third-party wire deposits.",
                "Detects directives instructing candidates to wire personal funds to overseas bank accounts for tax withholding."
            ),
            (
                "RULE-R-003",
                "Simulated Repatriation Security Deposit Lure",
                "LABOR_EXTORTION",
                94.0,
                r"(?:refundable\s+)?repatriation\s+(?:security\s+deposit|airfare\s+guarantee)\s+of\s+\$?\d+",
                1,
                "Refuse payment. Under international labor standards (ILO C181), employers bear all repatriation expenses.",
                "Detects extortion schemes requiring overseas applicants to pay upfront repatriation deposits."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleR(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleR]:
        """Scans input text against all compiled volume R rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
