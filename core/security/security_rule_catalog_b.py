"""
JobGuard Core Security - Security Threat Rule Catalog Part B
Contains threat detection rules, forensic patterns, MITRE ATT&CK techniques, and statutory citations.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re
from core.security.security_rule_catalog_a import ThreatRuleRecord


THREAT_RULES_B: List[ThreatRuleRecord] = [
    ThreatRuleRecord(
        rule_id="SEC-RULE-B-0001",
        category="IDENTITY_FRAUD",
        name="Cloned Company Certificate Authority Stamp",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(certified digital seal|authorized registrar stamp|official notary seal)\s*(?:#|no|:)?\s*[A-Z0-9-]+\b",
        mitre="T1583.001",
        statute="USA-18USC-1028",
        description="Pasting counterfeit notarization stamps on fraudulent job appointment letters.",
        remediation="Cross-reference certificate thumbprint with company PKI root."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-B-0002",
        category="IDENTITY_FRAUD",
        name="Fabricated Corporate Tax Registration Number",
        severity="HIGH",
        weight=30.0,
        regex=r"\b(tin|ein|gstin|vat)\s*(?:#|no|:)?\s*[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b",
        mitre="T1589.001",
        statute="IND-GST-ACT-2017",
        description="Displaying forged tax registration codes to fabricate legitimacy on appointment letters.",
        remediation="Verify tax ID against official government revenue portals."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-B-0003",
        category="WIRE_FRAUD",
        name="Crypto Escrow Onboarding Account Directive",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(send (?:usdt|btc|eth|crypto) to (?:wallet|escrow address)|(?:trc20|erc20) deposit address)\b",
        mitre="T1499.001",
        statute="USA-18USC-1343",
        description="Directing job applicant to fund a crypto escrow wallet for work allocation.",
        remediation="Immediate red flag. Corporate employers do not utilize cryptocurrency wallets for payroll."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-B-0004",
        category="WIRE_FRAUD",
        name="Pre-Interview Skill Assessment Fee Demand",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(assessment fee|coding test fee|online examination charges)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
        mitre="T1499.001",
        statute="IND-IT-66D",
        description="Charging candidate fees to access basic online hiring coding assessments.",
        remediation="Do not pay. Genuine hiring tests on HackerRank/LeetCode are fully sponsored by employers."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-B-0005",
        category="COERCION",
        name="Legal Action Threat for Candidate Withdrawal",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(legal action will be taken|breach of contract penalty|police complaint will be filed)\s+if\s+you\s+(?:leave|quit|withdraw|refuse)\b",
        mitre="T1566",
        statute="IND-BNS-351",
        description="Intimidating candidate with fabricated legal lawsuits upon attempting to withdraw application.",
        remediation="Ignore threats. At-will employment rights protect candidate withdrawal."
    )
]


class ThreatRuleCatalogManagerB:
    """Manager class for querying threat rules in Part B."""

    def __init__(self):
        self.rules = {r.rule_id: r for r in THREAT_RULES_B}
        self.compiled = [(re.compile(r.regex, re.IGNORECASE), r) for r in THREAT_RULES_B]

    def scan_content(self, text: str) -> List[Tuple[ThreatRuleRecord, str]]:
        matches = []
        for pat, r in self.compiled:
            m = pat.search(text)
            if m:
                matches.append((r, m.group(0)))
        return matches
