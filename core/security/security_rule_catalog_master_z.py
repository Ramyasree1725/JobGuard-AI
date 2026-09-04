"""
JobGuard Core Security - Security Rule Catalog Master Volume Z
Contains behavioral detection signatures for synthetic remote desktop (RDP / TeamViewer / AnyDesk)
session takeover lures, unauthorized keystroke loggers, and simulated VPN access tokens.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleZ:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterZ:
    """Master expanded catalog of behavioral detection rules volume Z."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleZ] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_z()

    def _seed_rules_z() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-Z-001",
                "Remote Desktop Session Takeover Lure for Evaluation",
                "REMOTE_ACCESS_TAKEOVER",
                99.0,
                r"(?:download|install)\s+(?:anydesk|teamviewer|ultraviewer|screenconnect)\s+and\s+provide\s+your\s+(?:id|code)\s+for\s+the\s+interview",
                1,
                "CRITICAL: Do not install remote desktop software for interviews. Scammers use RDP to compromise your PC and online banking.",
                "Detects directives instructing candidates to install remote desktop control software during hiring."
            ),
            (
                "RULE-Z-002",
                "Simulated Enterprise VPN Access Token Fee",
                "VPN_EXTORTION",
                96.0,
                r"(?:purchase|activate)\s+your\s+corporate\s+vpn\s+(?:token|license|gateway)\s+for\s+\$?\d+\s+prior\s+to\s+onboarding",
                1,
                "Refuse payment. Corporate VPN access and zero-trust tokens are provided 100% free by enterprise IT departments.",
                "Detects demands requiring new hires to purchase VPN gateway access licenses."
            ),
            (
                "RULE-Z-003",
                "Automated Keystroke Recording Consent Waiver",
                "PRIVACY_EXPLOIT",
                92.0,
                r"(?:candidate\s+consents\s+to\s+unrestricted\s+continuous\s+keystroke\s+logging\s+and\s+screen\s+capture\s+on\s+personal\s+device)",
                1,
                "Do not consent. Comprehensive keystroke logging on personal devices exposes banking and personal passwords.",
                "Detects predatory employment terms authorizing unrestricted keylogging on candidate personal laptops."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleZ(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleZ]:
        """Scans input text against all compiled volume Z rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
