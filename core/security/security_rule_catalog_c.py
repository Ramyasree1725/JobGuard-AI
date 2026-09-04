"""
JobGuard Core Security - Security Threat Rule Catalog Part C
Contains threat detection rules, forensic patterns, MITRE ATT&CK techniques, and statutory citations.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re
from core.security.security_rule_catalog_a import ThreatRuleRecord


THREAT_RULES_C: List[ThreatRuleRecord] = [
    ThreatRuleRecord(
        rule_id="SEC-RULE-C-0001",
        category="IDENTITY_FRAUD",
        name="Counterfeit Government Seal Embezzlement Pattern",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(ministry of corporate affairs seal|official empanelment stamp|government approved job portal)\b",
        mitre="T1583.001",
        statute="IND-EMBLEMS-ACT-1950",
        description="Falsely claiming official government empanelment on private employment offer letters.",
        remediation="Inspect official government portal registrar."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-C-0002",
        category="WIRE_FRAUD",
        name="Cryptocurrency Payroll Hardware Escrow Directive",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(transfer usdt to escrow|fund hardware security wallet|crypto bond deposit)\b",
        mitre="T1499.001",
        statute="USA-18USC-1343",
        description="Requiring candidates to send cryptocurrency tokens for corporate laptop provisioning.",
        remediation="Corporate IT departments provide all hardware free of charge."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-C-0003",
        category="DATA_THEFT",
        name="Biometric / Face Recognition Video Submission Trap",
        severity="HIGH",
        weight=35.0,
        regex=r"\b(upload unredacted aadhaar|submit passport video verification|send banking otp)\b",
        mitre="T1589.001",
        statute="IND-IT-43A",
        description="Harvesters attempting to collect biometric and sensitive OTP credentials before interview stages.",
        remediation="Never share one-time passwords or unredacted government identification."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-C-0004",
        category="COERCION",
        name="Candidate Breach Penalty Forfeiture Threat",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(legal lawsuit filed in high court|pay \d+ penalty for interview absence|recovery notice issued)\b",
        mitre="T1566",
        statute="IND-BNS-351",
        description="Fabricated legal summons to coerce money from candidates seeking to cancel interviews.",
        remediation="Ignore extortion threats. Candidate interviews carry zero financial liability."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-C-0005",
        category="CHECK_OVERPAYMENT",
        name="Overpayment Check Courier Tracking Directive",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(check will arrive via fedex|deposit check immediately upon delivery|purchase software license from vendor)\b",
        mitre="T1566.002",
        statute="USA-18USC-1341",
        description="Mailing counterfeit check and pressuring immediate software license purchasing before check clearing.",
        remediation="Counterfeit check scheme. Do not deposit or disburse personal funds."
    )
]


class ThreatRuleCatalogManagerC:
    """Manager class for querying threat rules in Part C."""

    def __init__(self):
        self.rules = {r.rule_id: r for r in THREAT_RULES_C}
        self.compiled = [(re.compile(r.regex, re.IGNORECASE), r) for r in THREAT_RULES_C]

    def scan_content(self, text: str) -> List[Tuple[ThreatRuleRecord, str]]:
        matches = []
        for pat, r in self.compiled:
            m = pat.search(text)
            if m:
                matches.append((r, m.group(0)))
        return matches
