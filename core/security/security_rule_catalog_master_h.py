"""
JobGuard Core Security - Security Rule Catalog Master Volume H
Contains detection signatures for foreign visa fee solicitations, package mule reshipping recruitment,
and cryptocurrency drainer wallet links in job descriptions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleH:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterH:
    """Master expanded catalog of behavioral detection rules volume H."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleH] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_h()

    def _seed_rules_h() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-H-001",
                "Foreign Visa and Work Permit Advance Fee Demand",
                "IMMIGRATION_FRAUD",
                95.0,
                r"(?:visa|work\s+permit|consular|embassy)\s+(?:processing|clearance|issuance)\s+fee\s+of\s+\$?\d+",
                1,
                "Refuse payment. Under US/UK/CA labor laws, employers and agencies cannot charge workers visa fees.",
                "Detects advance fee demands targeting international candidates under the pretext of visa processing."
            ),
            (
                "RULE-H-002",
                "Package Reshipping Mule Solicitation",
                "MULE_OPERATION",
                98.0,
                r"(?:receive|re-ship|forward)\s+(?:packages|parcels|boxes)\s+(?:from\s+home|to\s+overseas\s+addresses)",
                1,
                "Immediate critical alert. Cease forwarding packages. Contact U.S. Postal Inspection Service.",
                "Detects recruitment of unwitting victims to receive and re-ship goods purchased with stolen credit cards."
            ),
            (
                "RULE-H-003",
                "Cryptocurrency Wallet Direct Deposit Pretext",
                "FINANCIAL_FRAUD",
                90.0,
                r"(?:salary|wages|daily\s+commission)\s+(?:paid|disbursed)\s+exclusively\s+in\s+(?:usdt|bitcoin|crypto|bnb)",
                1,
                "Verify employer legal registration. Legitimate employers pay in sovereign legal tender.",
                "Detects offers conditioning remuneration exclusively on cryptocurrency wallet transfers."
            ),
            (
                "RULE-H-004",
                "Counterfeit Corporate Notary Stamp Lure",
                "DOCUMENT_FORGERY",
                85.0,
                r"(?:certified|notarized)\s+seal\s+by\s+(?:the\s+supreme\s+court|international\s+hiring\s+board|global\s+notary)",
                1,
                "Inspect document with digital seal verification module to expose clip-art stamp templates.",
                "Detects fictitious legal notary claims in overseas job appointment letters."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleH(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleH]:
        """Scans input text against all compiled volume H rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
