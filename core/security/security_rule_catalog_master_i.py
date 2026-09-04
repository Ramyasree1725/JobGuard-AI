"""
JobGuard Core Security - Security Rule Catalog Master Volume I
Contains behavioral signatures for detecting malicious coding test assessments,
credential-harvesting form plugins, and lookalike brand logos.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleI:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterI:
    """Master expanded catalog of behavioral detection rules volume I."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleI] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_i()

    def _seed_rules_i(self) -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-I-001",
                "Malicious NPM Dependency Lure in Take-Home Code",
                "SUPPLY_CHAIN_MALWARE",
                99.0,
                r"(?:run|execute)\s+npm\s+install\s+(?:to\s+start|before\s+running)\s+(?:the\s+assessment|coding\s+test)",
                1,
                "Isolate repository in container sandbox. Audit package.json preinstall scripts.",
                "Detects candidate coding challenges requiring dependency installation from untrusted git remotes."
            ),
            (
                "RULE-I-002",
                "Password Protected Assessment ZIP Archive",
                "EVASION_TECHNIQUE",
                90.0,
                r"(?:extract|unzip)\s+(?:the\s+attached|enclosed)\s+password\s+protected\s+(?:zip|rar|7z)\s+file",
                1,
                "Do not extract or open password-protected archives received from unverified recruiters.",
                "Detects password-encrypted archives designed to bypass automated antivirus email gateway scanners."
            ),
            (
                "RULE-I-003",
                "Direct Deposit Online Banking PIN Prompt",
                "IDENTITY_THEFT",
                99.0,
                r"(?:enter|provide)\s+your\s+(?:atm\s+pin|online\s+banking\s+password|security\s+questions)\s+for\s+payroll",
                1,
                "CRITICAL: Never share online banking passwords or PIN numbers. Employers only require account & routing numbers.",
                "Detects fraudulent payroll forms harvesting candidate online banking authentication secrets."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleI(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleI]:
        """Scans input text against all compiled volume I rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
