"""
JobGuard Core Security - Threat Signatures Large Database
Contains threat signature definitions, regex rules, and remediation steps.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re


@dataclass
class ThreatSigItem:
    sig_id: str
    category: str
    name: str
    severity: str
    weight: float
    regex: str
    mitre: str
    statute: str
    description: str
    remediation: str


def build_threat_large_catalog() -> Dict[str, ThreatSigItem]:
    catalog: Dict[str, ThreatSigItem] = {}
    
    # 1
    catalog["SIG-LG-0001"] = ThreatSigItem(
        sig_id="SIG-LG-0001",
        category="FINANCIAL_DEMAND",
        name="Mandatory Candidate Registration Fee Clause",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(registration fee|entry fee|joining fee|sign-?up fee)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
        mitre="T1499.001",
        statute="IND-IT-66D / USA-FTC-SEC5",
        description="Demanding candidate payment prior to conducting interviews or issuing appointment contracts.",
        remediation="Refuse payment. Legitimate corporate firms never charge job seekers any fee."
    )
    # 2
    catalog["SIG-LG-0002"] = ThreatSigItem(
        sig_id="SIG-LG-0002",
        category="FINANCIAL_DEMAND",
        name="Refundable Laptop Security Deposit Demand",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(refundable (?:security )?deposit|caution deposit|equipment deposit)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
        mitre="T1499.001",
        statute="USA-18USC-1343",
        description="Demanding refundable cash deposit for work-from-home hardware dispatch.",
        remediation="Never pay for corporate laptop shipments. Genuine companies dispatch IT assets at employer expense."
    )
    # 3
    catalog["SIG-LG-0003"] = ThreatSigItem(
        sig_id="SIG-LG-0003",
        category="FAKE_CHECK",
        name="Mobile Check Deposit Instruction for Hardware",
        severity="CRITICAL",
        weight=50.0,
        regex=r"\b(deposit the (?:check|cheque)|cashier'?s check|e-check)\s+into\s+your\s+(?:personal\s+)?bank\s+account\b",
        mitre="T1566.002",
        statute="USA-18USC-1341",
        description="Instructing applicant to deposit a check and transfer funds to a designated vendor before settlement.",
        remediation="Checks take days to officially clear. Fraudulent checks bounce, leaving candidate liable."
    )
    # 4
    catalog["SIG-LG-0004"] = ThreatSigItem(
        sig_id="SIG-LG-0004",
        category="FAKE_CHECK",
        name="Third-Party Vendor Wire Transfer Clause",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(wire|transfer|send|zelle|venmo)\s+(?:the\s+)?(?:funds|money|balance)\s+to\s+(?:our\s+)?(?:approved|designated)\s+vendor\b",
        mitre="T1566.002",
        statute="USA-18USC-1343",
        description="Requiring funds from an advance check to be wired to a third-party equipment supplier.",
        remediation="Corporate IT departments purchase hardware directly. Do not wire personal funds."
    )
    # 5
    catalog["SIG-LG-0005"] = ThreatSigItem(
        sig_id="SIG-LG-0005",
        category="TASK_RECHARGE",
        name="E-Commerce Product Rating Task Recharge Scheme",
        severity="CRITICAL",
        weight=45.0,
        regex=r"\b(boost products?|optimize (?:hotel|app|movie) ratings?|complete \d+ tasks per day)\b",
        mitre="T1586",
        statute="IND-BNS-318",
        description="Pyramid task recharge scams requiring daily balance deposits to unlock task commission tiers.",
        remediation="Stop all task participation immediately. Deposited funds are non-recoverable."
    )
    # 6
    catalog["SIG-LG-0006"] = ThreatSigItem(
        sig_id="SIG-LG-0006",
        category="TASK_RECHARGE",
        name="Social Media Video Like Screenshot Incentive",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(like (?:and subscribe|youtube videos|instagram posts)|earn \$\d+ per like|₹\d+ per screenshot)\b",
        mitre="T1586",
        statute="IND-IT-66D",
        description="Baiting users with small payouts for video likes before redirecting to Telegram investment traps.",
        remediation="Block sender and do not join VIP task Telegram channels."
    )
    # 7
    catalog["SIG-LG-0007"] = ThreatSigItem(
        sig_id="SIG-LG-0007",
        category="IMPERSONATION",
        name="Telegram-Only Official Hiring Channel",
        severity="CRITICAL",
        weight=35.0,
        regex=r"\b(contact (?:our\s+)?(?:hr|recruiter)\s+on\s+telegram|telegram (?:username|id|handle)\s*:\s*@[A-Za-z0-9_]+)\b",
        mitre="T1566.003",
        statute="GBR-FRAUD-2006",
        description="Conducting interviews and employment onboarding exclusively over Telegram messaging.",
        remediation="Fortune 500 recruiters use enterprise applicant tracking systems, never Telegram."
    )
    # 8
    catalog["SIG-LG-0008"] = ThreatSigItem(
        sig_id="SIG-LG-0008",
        category="IMPERSONATION",
        name="Free Public Webmail Recruiter Identity",
        severity="HIGH",
        weight=25.0,
        regex=r"\b[A-Za-z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|aol|icloud|protonmail)\.com\b",
        mitre="T1586.002",
        statute="USA-FTC-SEC5",
        description="Recruiter claiming corporate employer affiliation from a free public webmail address.",
        remediation="Demand communication from the verified corporate domain."
    )
    # 9
    catalog["SIG-LG-0009"] = ThreatSigItem(
        sig_id="SIG-LG-0009",
        category="DATA_THEFT",
        name="Premature Banking / Direct Deposit Collection",
        severity="CRITICAL",
        weight=40.0,
        regex=r"\b(provide (?:your\s+)?(?:bank account number|routing number|online banking credentials))\s+before\s+(?:interview|offer)\b",
        mitre="T1589.001",
        statute="USA-18USC-1028",
        description="Demanding bank account numbers and routing details before extending formal job offers.",
        remediation="Banking details are collected only after contract signing via secure enterprise HR portals."
    )
    # 10
    catalog["SIG-LG-0010"] = ThreatSigItem(
        sig_id="SIG-LG-0010",
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

    return catalog


class ThreatLargeManager:
    def __init__(self):
        self.catalog = build_threat_large_catalog()

    def get_by_id(self, sig_id: str) -> Optional[ThreatSigItem]:
        return self.catalog.get(sig_id)
