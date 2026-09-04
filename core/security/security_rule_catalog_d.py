"""
JobGuard Core Security - Security Threat Rule Catalog Part D
Contains threat detection rules, forensic patterns, MITRE ATT&CK techniques, and statutory citations.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re
from core.security.security_rule_catalog_a import ThreatRuleRecord


THREAT_RULES_D: List[ThreatRuleRecord] = [
    ThreatRuleRecord(
        rule_id="SEC-RULE-D-0001",
        category="WIRE_FRAUD",
        name="Offshore Talent Agency Processing Fee Clause",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(visa processing fee|work permit clearance fee|embassy clearance deposit)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
        mitre="T1499.001",
        statute="IND-EMIGRATION-ACT-1983",
        description="Extracting illegal visa and work permit deposits from overseas job seekers.",
        remediation="Authorized employer sponsors cover all visa petition fees directly."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-D-0002",
        category="TASK_RECHARGE",
        name="Crypto Cloud Mining VIP Job Level Tier",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(upgrade to vip level \d+|unlock daily task allocation with \d+ usdt|recharge mining power)\b",
        mitre="T1586",
        statute="USA-18USC-1343",
        description="Ponzi scheme disguised as cloud task computing job requiring continuous capital injection.",
        remediation="Cease all transfers immediately. Report wallet addresses to cyber authorities."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-D-0003",
        category="IMPERSONATION",
        name="Executive Headhunter WhatsApp Group Redirection",
        severity="HIGH",
        weight=30.0,
        regex=r"\b(join our executive recruitment group on whatsapp|whatsapp group invite link: chat\.whatsapp\.com\/[A-Za-z0-9]+)\b",
        mitre="T1566.003",
        statute="GBR-FRAUD-2006",
        description="Mass broadcasting WhatsApp group invites for bogus executive hiring.",
        remediation="Leave group. Legitimate executive search firms conduct personalized communication."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-D-0004",
        category="DATA_THEFT",
        name="Remote Access Screen Sharing Interview Directive",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(install anydesk for technical interview|download teamviewer to begin onboarding|share rustdesk id)\b",
        mitre="T1566.001",
        statute="USA-18USC-1030",
        description="Coercing candidates to install remote desktop access software to compromise local banking credentials.",
        remediation="Never allow remote desktop control during recruitment interviews."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-D-0005",
        category="FINANCIAL_DEMAND",
        name="Medical Examination Reimbursement Trap",
        severity="HIGH",
        weight=35.0,
        regex=r"\b(pay for company approved medical test|medical fitness certificate fee|reimbursable health test charge)\b",
        mitre="T1499.001",
        statute="IND-IT-66D",
        description="Directing job applicants to fraudulent medical clinics demanding upfront testing fees.",
        remediation="Corporate medical assessments are paid directly by the employer."
    )
]


class ThreatRuleCatalogManagerD:
    """Manager class for querying threat rules in Part D."""

    def __init__(self):
        self.rules = {r.rule_id: r for r in THREAT_RULES_D}
        self.compiled = [(re.compile(r.regex, re.IGNORECASE), r) for r in THREAT_RULES_D]

    def scan_content(self, text: str) -> List[Tuple[ThreatRuleRecord, str]]:
        matches = []
        for pat, r in self.compiled:
            m = pat.search(text)
            if m:
                matches.append((r, m.group(0)))
        return matches
