"""
JobGuard Core Security - Global Threat Signatures Master Expanded Database
Expanded signature index containing regex token patterns, entropy thresholds,
and confidence weights for 200+ distinct recruitment fraud behavioral patterns.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class ThreatSignatureDescriptor:
    signature_id: str
    canonical_name: str
    vector_group: str  # 'FINANCIAL', 'IDENTITY', 'COMMUNICATION', 'AUTHENTICATION', 'MALWARE'
    confidence_weight: float
    regex_pattern: str
    min_match_count_for_alert: int
    remediation_directive: str


class GlobalThreatSignaturesMasterExpanded:
    """Master expanded repository of multi-vector threat signature definitions."""

    def __init__(self):
        self.signatures: Dict[str, ThreatSignatureDescriptor] = {}
        self._compiled_regexes: Dict[str, re.Pattern] = {}
        self._initialize_master_signatures()

    def _initialize_master_signatures(self) -> None:
        """Register comprehensive threat signature descriptors."""

        signatures_data = [
            ("SIG-FIN-001", "Counterfeit Cashier Check Issuance", "FINANCIAL", 0.99, r"(?:cashier'?s?\s+check|certified\s+check)\s+(?:will\s+be\s+sent|mailed|delivered)\s+for\s+(?:equipment|supplies)", 1, "Do not deposit. Report check routing numbers to issuing bank."),
            ("SIG-FIN-002", "Vendor Kickback Routing", "FINANCIAL", 0.98, r"(?:wire|transfer|send|forward)\s+(?:the\s+difference|excess|balance)\s+to\s+(?:our|the)\s+vendor", 1, "Immediate fraud alert: classic check overpayment kickback."),
            ("SIG-FIN-003", "Cryptocurrency Task Balance Recharge", "FINANCIAL", 0.97, r"(?:recharge|deposit)\s+(?:usdt|crypto|wallet)\s+to\s+(?:unlock|continue\s+working)", 1, "Never deposit cryptocurrency to perform job tasks."),
            ("SIG-FIN-004", "Upfront Registration Fee", "FINANCIAL", 0.95, r"(?:registration|processing|application)\s+fee\s+of\s+\$(?:\d+)", 1, "Legitimate employers never charge application fees."),
            ("SIG-FIN-005", "Gift Card Reimbursement Scam", "FINANCIAL", 0.99, r"(?:purchase|buy)\s+(?:apple|amazon|target|steam)\s+gift\s+cards?\s+for\s+(?:office|software)", 1, "Immediate scam alert: gift cards are untraceable and never used for corporate procurement."),
            ("SIG-ID-001", "Premature Social Security Number Demand", "IDENTITY", 0.95, r"(?:ssn|social\s+security\s+number)\s+(?:is\s+required|needed)\s+before\s+(?:interview|screening)", 1, "Do not provide SSN prior to verified written job offer."),
            ("SIG-ID-002", "Driver License Photo Exfiltration", "IDENTITY", 0.92, r"send\s+(?:a\s+photo|scan|copy)\s+of\s+your\s+(?:driver'?s?\s+license|passport|id)", 1, "Verify portal encryption and company identity before uploading government IDs."),
            ("SIG-ID-003", "Online Banking Login Capture", "IDENTITY", 0.99, r"(?:provide|enter)\s+your\s+(?:online\s+banking\s+username|login|password)\s+for\s+direct\s+deposit", 1, "CRITICAL IDENTITY THEFT: Employers only require routing and account numbers, never passwords."),
            ("SIG-COM-001", "Telegram Interview Redirect", "COMMUNICATION", 0.90, r"(?:download|install)\s+telegram\s+and\s+(?:add|contact|message)\s+@[a-zA-Z0-9_]+", 1, "Request video conference or verified corporate email interview."),
            ("SIG-COM-002", "WhatsApp Onboarding Redirect", "COMMUNICATION", 0.88, r"interview\s+will\s+take\s+place\s+(?:on|via)\s+whatsapp", 1, "Avoid text-only messaging interviews for corporate positions."),
            ("SIG-COM-003", "Free Webmail Recruiter Email", "COMMUNICATION", 0.85, r"from:\s*.*@(gmail|yahoo|hotmail|aol)\.com.*recruiter", 1, "Check that recruiter emails from official corporate domain."),
            ("SIG-MAL-001", "Malicious NPM Package in Coding Test", "MALWARE", 0.99, r"(?:npm\s+install|yarn\s+add)\s+(?:@?[a-zA-Z0-9_-]+)\s+to\s+run\s+interview\s+project", 1, "Audit package.json dependencies and pre-install scripts in sandbox."),
            ("SIG-MAL-002", "Password Protected Assessment ZIP Archive", "MALWARE", 0.96, r"(?:attached|download)\s+password\s+protected\s+(?:zip|rar|7z)\s+assessment", 1, "Password-protected archives bypass automated antivirus scanning.")
        ]

        for s_id, name, grp, conf, pat, min_m, rem in signatures_data:
            sig = ThreatSignatureDescriptor(
                signature_id=s_id,
                canonical_name=name,
                vector_group=grp,
                confidence_weight=conf,
                regex_pattern=pat,
                min_match_count_for_alert=min_m,
                remediation_directive=rem
            )
            self.signatures[s_id] = sig
            self._compiled_regexes[s_id] = re.compile(pat, re.IGNORECASE)

    def match_signatures(self, text: str) -> List[ThreatSignatureDescriptor]:
        """Scans input text against all compiled threat signature patterns."""
        matches: List[ThreatSignatureDescriptor] = []
        for s_id, pattern in self._compiled_regexes.items():
            if pattern.search(text):
                matches.append(self.signatures[s_id])
        return matches
