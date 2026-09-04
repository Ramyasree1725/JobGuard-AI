"""
JobGuard Core Security - Security Rule Catalog Master Volume BA
Contains behavioral detection signatures for simulated corporate compliance notary certificates,
unauthorized international currency exchange fees, and fake executive signing stamps.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleBA:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterBA:
    """Master expanded catalog of behavioral detection rules volume BA."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleBA] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_ba()

    def _seed_rules_ba() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-BA-001",
                "Foreign Currency Exchange Conversion Surcharge Lure",
                "CURRENCY_EXTORTION",
                96.0,
                r"(?:pay|wire)\s+(?:a\s+)?foreign\s+currency\s+exchange\s+(?:conversion|hedging)\s+fee\s+of\s+\$?\d+\s+for\s+salary\s+disbursement",
                1,
                "Refuse payment. Employers absorb all foreign exchange conversion costs during international payroll disbursement.",
                "Detects demands requiring international remote workers to pay upfront currency conversion fees to receive salary."
            ),
            (
                "RULE-BA-002",
                "Synthetic Corporate Seal Embossment Claim",
                "DOCUMENT_FORGERY",
                88.0,
                r"(?:affixed\s+with\s+the\s+official\s+digital\s+embossment\s+of\s+the\s+global\s+board\s+of\s+directors)",
                1,
                "Verify employment letter directly through verified corporate HR switchboard.",
                "Detects fabricated corporate embossment language added to scam PDF offer documents."
            ),
            (
                "RULE-BA-003",
                "Pre-Employment Equipment Re-Stocking Security Fee",
                "ADVANCE_FEE",
                95.0,
                r"(?:refundable\s+)?hardware\s+re-stocking\s+fee\s+of\s+\$?\d+\s+prior\s+to\s+shipping",
                1,
                "Refuse payment. Hardware restocking and provisioning fees are never charged to job candidates.",
                "Detects extortion demands requiring candidates to pay equipment re-stocking or freight assurance fees."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleBA(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleBA]:
        """Scans input text against all compiled volume BA rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
