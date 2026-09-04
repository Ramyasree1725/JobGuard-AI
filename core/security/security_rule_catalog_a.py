"""
JobGuard Core Security - Security Threat Rule Catalog Part A
Contains threat detection rules, forensic patterns, MITRE ATT&CK techniques, and statutory citations.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re


@dataclass
class ThreatRuleRecord:
    rule_id: str
    category: str
    name: str
    severity: str
    weight: float
    regex: str
    mitre: str
    statute: str
    description: str
    remediation: str


THREAT_RULES_A: List[ThreatRuleRecord] = [
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0001",
        category="FINANCIAL_DEMAND",
        name="Mandatory Candidate Registration Fee Clause",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(registration fee|entry fee|joining fee|sign-?up fee)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
        mitre="T1499.001",
        statute="IND-IT-66D / USA-FTC-SEC5",
        description="Demanding candidate payment prior to conducting interviews or issuing appointment contracts.",
        remediation="Refuse payment. Legitimate corporate firms never charge job seekers any fee."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0002",
        category="FINANCIAL_DEMAND",
        name="Refundable Laptop Security Deposit Demand",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(refundable (?:security )?deposit|caution deposit|equipment deposit)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
        mitre="T1499.001",
        statute="USA-18USC-1343",
        description="Demanding refundable cash deposit for work-from-home hardware dispatch.",
        remediation="Never pay for corporate laptop shipments. Genuine companies dispatch IT assets at employer expense."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0003",
        category="FAKE_CHECK",
        name="Mobile Check Deposit Instruction for Hardware",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(deposit the (?:check|cheque)|cashier'?s check|e-check)\s+into\s+your\s+(?:personal\s+)?bank\s+account\b",
        mitre="T1566.002",
        statute="USA-18USC-1341",
        description="Instructing applicant to deposit a check and transfer funds to a designated vendor before settlement.",
        remediation="Checks take days to officially clear. Fraudulent checks bounce, leaving candidate liable."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0004",
        category="FAKE_CHECK",
        name="Third-Party Vendor Wire Transfer Clause",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(wire|transfer|send|zelle|venmo)\s+(?:the\s+)?(?:funds|money|balance)\s+to\s+(?:our\s+)?(?:approved|designated)\s+vendor\b",
        mitre="T1566.002",
        statute="USA-18USC-1343",
        description="Requiring funds from an advance check to be wired to a third-party equipment supplier.",
        remediation="Corporate IT departments purchase hardware directly. Do not wire personal funds."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0005",
        category="TASK_RECHARGE",
        name="E-Commerce Product Rating Task Recharge Scheme",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(boost products?|optimize (?:hotel|app|movie) ratings?|complete \d+ tasks per day)\b",
        mitre="T1586",
        statute="IND-BNS-318",
        description="Pyramid task recharge scams requiring daily balance deposits to unlock task commission tiers.",
        remediation="Stop all task participation immediately. Deposited funds are non-recoverable."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0006",
        category="TASK_RECHARGE",
        name="Social Media Video Like Screenshot Incentive",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(like (?:and subscribe|youtube videos|instagram posts)|earn \$\d+ per like|₹\d+ per screenshot)\b",
        mitre="T1586",
        statute="IND-IT-66D",
        description="Baiting users with small payouts for video likes before redirecting to Telegram investment traps.",
        remediation="Block sender and do not join VIP task Telegram channels."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0007",
        category="IMPERSONATION",
        name="Telegram-Only Official Hiring Channel",
        severity="CRITICAL",
        weight=35.0,
        regex=r"\b(contact (?:our\s+)?(?:hr|recruiter)\s+on\s+telegram|telegram (?:username|id|handle)\s*:\s*@[A-Za-z0-9_]+)\b",
        mitre="T1566.003",
        statute="GBR-FRAUD-2006",
        description="Conducting interviews and employment onboarding exclusively over Telegram messaging.",
        remediation="Fortune 500 recruiters use enterprise applicant tracking systems, never Telegram."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0008",
        category="IMPERSONATION",
        name="Free Public Webmail Recruiter Identity",
        severity="HIGH",
        weight=25.0,
        regex=r"\b[A-Za-z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|aol|icloud|protonmail)\.com\b",
        mitre="T1586.002",
        statute="USA-FTC-SEC5",
        description="Recruiter claiming corporate employer affiliation from a free public webmail address.",
        remediation="Demand communication from the verified corporate domain."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0009",
        category="DATA_THEFT",
        name="Premature Banking / Direct Deposit Collection",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(provide (?:your\s+)?(?:bank account number|routing number|online banking credentials))\s+before\s+(?:interview|offer)\b",
        mitre="T1589.001",
        statute="USA-18USC-1028",
        description="Demanding bank account numbers and routing details before extending formal job offers.",
        remediation="Banking details are collected only after contract signing via secure enterprise HR portals."
    ),
    ThreatRuleRecord(
        rule_id="SEC-RULE-A-0010",
        category="COERCION",
        name="24-Hour Offer Forfeiture Ultimatum",
        severity="HIGH",
        weight=25.0,
        regex=r"\b(offer expires in (?:24|12|6|2) hours|must sign and return within \d+ hours or offer will be forfeited)\b",
        mitre="T1566",
        statute="Fair Work Practice Standard",
        description="Artificial extreme time pressure to prevent independent background verification.",
        remediation="Legitimate employers provide 3 to 7 business days for contract review."
    )
]


class ThreatRuleCatalogManagerA:
    """Manager class for querying threat rules in Part A."""

    def __init__(self):
        self.rules = {r.rule_id: r for r in THREAT_RULES_A}
        self.compiled = [(re.compile(r.regex, re.IGNORECASE), r) for r in THREAT_RULES_A]

    def scan_content(self, text: str) -> List[Tuple[ThreatRuleRecord, str]]:
        matches = []
        for pat, r in self.compiled:
            m = pat.search(text)
            if m:
                matches.append((r, m.group(0)))
        return matches
