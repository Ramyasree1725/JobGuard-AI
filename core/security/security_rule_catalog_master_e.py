"""
JobGuard Core Security - Security Rule Catalog Master Volume E
Contains high-precision regex signatures, token distance heuristics,
and risk weights for detecting advance fee scams, onboarding deposit demands, and gift card fraud.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleE:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterE:
    """Master expanded catalog of behavioral detection rules volume E."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleE] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_e()

    def _seed_rules_e(self) -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-E-001",
                "Advance Equipment Deposit Mandate",
                "FINANCIAL_FRAUD",
                85.0,
                r"(?:refundable|mandatory|onboarding)\s+(?:equipment|laptop|hardware)\s+deposit\s+(?:of\s+)?\$?\d+",
                1,
                "Refuse payment. Legitimate employers provide laptops at zero expense.",
                "Detects clauses conditioning equipment dispatch on candidate upfront deposits."
            ),
            (
                "RULE-E-002",
                "Background Screening Fee Extraction",
                "FINANCIAL_FRAUD",
                75.0,
                r"(?:candidate|applicant)\s+must\s+(?:pay|cover|remit)\s+(?:for\s+)?(?:the\s+)?(?:background|criminal)\s+(?:check|screening|clearance)",
                1,
                "Notify candidate that employer is legally responsible for background check expenses.",
                "Detects unlawful fee shifting for pre-employment background screening."
            ),
            (
                "RULE-E-003",
                "Gift Card Procurement Lure",
                "FINANCIAL_FRAUD",
                95.0,
                r"(?:purchase|buy)\s+(?:apple|target|amazon|steam|google\s+play)\s+gift\s*cards?\s+(?:to|for)\s+(?:procure|software|licensing|verification)",
                1,
                "Immediate critical alert. Gift cards are untraceable and never used for enterprise IT.",
                "Detects retail gift card purchasing demands for alleged software or hardware provisioning."
            ),
            (
                "RULE-E-004",
                "Peer-to-Peer App Payment Directives",
                "FINANCIAL_FRAUD",
                90.0,
                r"(?:send|wire|transfer)\s+(?:via|through)\s+(?:zelle|cashapp|venmo|apple\s+cash)\s+to\s+@[a-zA-Z0-9_-]+",
                1,
                "Do not send P2P app transfers. Instant consumer rails provide zero dispute protection for job fees.",
                "Detects instructions directing candidate to use consumer P2P apps for employment fees."
            ),
            (
                "RULE-E-005",
                "Cryptocurrency Wallet Onboarding Address",
                "FINANCIAL_FRAUD",
                98.0,
                r"(?:send|deposit)\s+(?:usdt|btc|eth|crypto)\s+to\s+(?:wallet|address)\s*:\s*(?:0x[a-fA-F0-9]{40}|T[A-Za-z1-9]{33})",
                1,
                "Cease all communication. Legitimate employment never requires cryptocurrency transfers.",
                "Detects explicit cryptocurrency wallet addresses provided for task recharge or onboarding."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleE(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleE]:
        """Scans input text against all compiled volume E rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
