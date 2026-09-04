"""
JobGuard Core Security - Security Rule Catalog Master Volume K
Contains behavioral signatures for detecting malicious PDF form exploits,
macro-enabled word documents (.docm), and fake video call installer payloads.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleK:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterK:
    """Master expanded catalog of behavioral detection rules volume K."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleK] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_k()

    def _seed_rules_k() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-K-001",
                "Fake Video Interview Codec Installer Lure",
                "MALWARE_DISTRIBUTION",
                99.0,
                r"(?:download|install)\s+(?:the\s+special|required)\s+(?:zoom|teams|meeting)\s+(?:codec|plugin|exe)\s+to\s+join",
                1,
                "Do not download third-party executables to join video calls. Use official browser web client.",
                "Detects fake meeting client installers delivering info-stealer malware (RedLine / Lumma Stealer)."
            ),
            (
                "RULE-K-002",
                "Macro Enabled Contract Document (.docm)",
                "MALWARE_DISTRIBUTION",
                98.0,
                r"(?:enable\s+content|enable\s+macros)\s+to\s+(?:view|sign|unlock)\s+(?:the\s+employment\s+agreement|offer\s+letter)",
                1,
                "Never enable macros on recruitment documents. Legitimate contracts are static PDFs.",
                "Detects malicious VBA macro lures in weaponized Word documents sent as employment contracts."
            ),
            (
                "RULE-K-003",
                "Compressed LNK Shortcut in Assessment Folder",
                "EXECUTION_EXPLOIT",
                99.0,
                r"\.lnk\b.*(?:coding_challenge|interview_test|starter_code)",
                1,
                "Do not double click .lnk shortcut files received in job application bundles.",
                "Detects Windows shortcut (.lnk) files containing PowerShell download cradles."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleK(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleK]:
        """Scans input text against all compiled volume K rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
