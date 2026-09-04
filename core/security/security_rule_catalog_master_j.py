"""
JobGuard Core Security - Security Rule Catalog Master Volume J
Contains behavioral detection signatures for synthetic identity fabrication,
fake corporate tax withholding (W-4 / W-9 / I-9) portals, and unauthorized payroll routing.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleJ:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterJ:
    """Master expanded catalog of behavioral detection rules volume J."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleJ] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_j()

    def _seed_rules_j() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-J-001",
                "Unencrypted Tax Document Upload Endpoint",
                "PII_EXFILTRATION",
                92.0,
                r"<form.*action=[\"']https?://[a-zA-Z0-9.-]+/(?:upload_w4|submit_i9|tax_form)\.php",
                1,
                "Do not upload government tax forms to unauthenticated PHP scripts. Enforce encrypted enterprise portals.",
                "Detects unencrypted HTTP multipart form uploads targeting legacy or malicious PHP endpoints for tax forms."
            ),
            (
                "RULE-J-002",
                "Third-Party Payroll Cloud Storage Link",
                "CREDENTIAL_HARVESTING",
                88.0,
                r"https?://(?:dropbox\.com/request|mega\.nz/folder|drive\.google\.com/drive/folders)/[a-zA-Z0-9_-]+.*(?:tax|payroll|identity)",
                1,
                "Refuse file upload to consumer cloud storage folders. Use authentic corporate HRIS.",
                "Detects recruiter requests to upload passports, SSN cards, or voided checks to public cloud drives."
            ),
            (
                "RULE-J-003",
                "Counterfeit Direct Deposit Change Verification",
                "PAYROLL_FRAUD",
                95.0,
                r"(?:update|change|confirm)\s+your\s+direct\s+deposit\s+bank\s+account\s+via\s+(?:email|sms\s+link)",
                1,
                "Log in directly to your corporate payroll portal. Never update direct deposit via email links.",
                "Detects phishing attempts to redirect candidate or employee payroll disbursements to fraud mule accounts."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleJ(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleJ]:
        """Scans input text against all compiled volume J rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
