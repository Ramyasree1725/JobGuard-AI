"""
JobGuard Core Security - Security Rule Catalog Master Volume L
Contains behavioral signatures for detecting fake corporate tax ID claims (EIN/SSN spoofing),
bogus employment guarantee bonds, and unverified direct deposit routing updates.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleL:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterL:
    """Master expanded catalog of behavioral detection rules volume L."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleL] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_l()

    def _seed_rules_l() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-L-001",
                "Bogus Performance Bond Indemnity Demand",
                "FINANCIAL_EXTORTION",
                95.0,
                r"(?:deposit|remit)\s+(?:a\s+)?refundable\s+(?:performance|indemnity|fidelity)\s+bond\s+of\s+\$?\d+",
                1,
                "Refuse payment. Legitimate corporate employers never require employee performance bonds.",
                "Detects demands for advance performance bonds or fidelity guarantee deposits."
            ),
            (
                "RULE-L-002",
                "Equipment Customs Clearance Fee Shifting",
                "SHIPPING_FRAUD",
                96.0,
                r"(?:pay|cover)\s+(?:the\s+)?(?:customs|import|duty|clearance)\s+fee\s+for\s+your\s+(?:laptop|equipment|shipment)",
                1,
                "Do not pay customs fees. Corporate employers handle international courier customs clearance directly.",
                "Detects attempts to extract personal funds under the pretext of international customs clearance for laptops."
            ),
            (
                "RULE-L-003",
                "Stolen Corporate Tax EIN Attribution",
                "IDENTITY_SPOOFING",
                88.0,
                r"(?:our\s+corporate\s+tax\s+id|company\s+ein\s+is)\s*:\s*\d{2}-\d{7}",
                1,
                "Cross-reference stated EIN against SEC EDGAR database to verify legal entity alignment.",
                "Detects scam operators using publicly known corporate Employer Identification Numbers (EINs) on fake offer letters."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleL(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleL]:
        """Scans input text against all compiled volume L rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
