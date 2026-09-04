"""
JobGuard Core Security - Security Rule Catalog Master Volume F
Contains behavioral signatures for detecting artificial hiring urgency, chat-only evaluation,
premature identity credential harvesting, and suspicious document signing deadlines.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleF:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterF:
    """Master expanded catalog of behavioral detection rules volume F."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleF] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_f()

    def _seed_rules_f(self) -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-F-001",
                "Hyper-Compressed Exploding Offer Window",
                "SOCIAL_ENGINEERING",
                60.0,
                r"(?:offer|appointment)\s+(?:expires|voided|cancelled)\s+within\s+(?:2|3|4|6|12|24)\s+hours",
                1,
                "Request standard 3-5 business day contract review period. Scammers create urgency to prevent diligence.",
                "Detects artificial psychological time pressure designed to rush candidates into compliance."
            ),
            (
                "RULE-F-002",
                "Telegram Scripted Questionnaire Screening",
                "CHANNEL_DECEPTION",
                70.0,
                r"interview\s+(?:will\s+be\s+conducted|is\s+held)\s+via\s+telegram\s+text\s+chat",
                1,
                "Demand live interactive video interview with verified corporate email address.",
                "Detects exclusive reliance on text-only messaging channels for hiring evaluations."
            ),
            (
                "RULE-F-003",
                "Premature SSN and Tax ID Demand",
                "IDENTITY_HARVESTING",
                90.0,
                r"(?:enter|provide|fill\s+in)\s+your\s+ssn\s+(?:on|in)\s+the\s+initial\s+application\s+form",
                1,
                "Never share Social Security Number before formal verified job offer and authenticated portal login.",
                "Detects premature collection of national identification numbers on public application forms."
            ),
            (
                "RULE-F-004",
                "Unsolicited Offer Without Interview",
                "SOCIAL_ENGINEERING",
                85.0,
                r"(?:you\s+have\s+been\s+selected|hired)\s+based\s+on\s+your\s+resume\s+without\s+(?:any\s+)?interview",
                1,
                "Immediate red flag. Genuine corporate employers conduct multiple rounds of technical/behavioral screening.",
                "Detects instant job offers granted with zero prior verbal or video interview interaction."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleF(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleF]:
        """Scans input text against all compiled volume F rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
