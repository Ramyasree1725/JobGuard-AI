"""
JobGuard Core Knowledge - Recruiter Impersonation Threat Signatures Large
Detailed signature database cataloging deceptive recruiter greeting scripts,
fake interview booking workflows, and fraudulent employment verification certificates.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class RecruiterImpersonationSignature:
    signature_id: str
    signature_name: str
    target_channel: str
    confidence_weight: float
    regex_pattern: str
    mitigation_action: str
    threat_description: str


class RecruiterImpersonationThreatSignaturesLarge:
    """Master expanded repository of recruiter impersonation behavioral signatures."""

    def __init__(self):
        self.signatures: Dict[str, RecruiterImpersonationSignature] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_signatures()

    def _seed_signatures(self) -> None:
        """Register extensive signature patterns."""

        data = [
            (
                "SIG-REC-001",
                "Unsolicited Executive InMail Greeting",
                "LINKEDIN_INMAIL",
                0.88,
                r"(?:i\s+came\s+across\s+your\s+profile\s+on\s+linkedin|reviewed\s+your\s+resume\s+in\s+our\s+database).*(?:immediate\s+opening|exclusive\s+remote\s+role)",
                "Verify recruiter company page alignment and mutual connections before responding.",
                "Standard canned introductory greeting utilized by automated scam scraper bots."
            ),
            (
                "SIG-REC-002",
                "Text-Only Questionnaire Interview Script",
                "TELEGRAM_CHAT",
                0.95,
                r"(?:here\s+are\s+the\s+interview\s+questions|answer\s+the\s+following\s+10\s+questions\s+in\s+text)",
                "Refuse text-only interview. Insist on live video meeting with corporate domain recruiter.",
                "Scripted questionnaire delivered via instant messaging masquerading as formal evaluation."
            ),
            (
                "SIG-REC-003",
                "Immediate Post-Questionnaire Hiring Decision",
                "MESSAGING_APP",
                0.96,
                r"(?:congratulations,\s+you\s+passed\s+the\s+interview|the\s+management\s+has\s+approved\s+your\s+hiring)",
                "Immediate red flag: genuine corporate offers require multiple interview rounds and reference checks.",
                "Instant hiring confirmation issued within minutes of submitting text answers."
            ),
            (
                "SIG-REC-004",
                "Equipment Check Disbursement Instructions",
                "EMAIL_CONTRACT",
                0.99,
                r"(?:we\s+will\s+issue\s+a\s+check\s+for\s+\$?\d+.*to\s+purchase\s+your\s+equipment|home\s+office\s+allowance\s+check)",
                "Do not deposit the check. Genuine employers ship corporate hardware directly.",
                "Mailing counterfeit check for home office supplies with vendor wire instructions."
            ),
            (
                "SIG-REC-005",
                "Deposit Surplus Wire Kickback Directive",
                "EMAIL_INSTRUCTIONS",
                0.99,
                r"(?:deposit\s+the\s+check\s+via\s+mobile\s+app|send\s+the\s+remaining\s+balance\s+to\s+our\s+vendor\s+via\s+zelle)",
                "Contact bank fraud department immediately if already deposited.",
                "Instructing victim to wire personal funds to scam mule before check bounces."
            )
        ]

        for s_id, name, chan, conf, pat, mit, desc in data:
            self.signatures[s_id] = RecruiterImpersonationSignature(
                signature_id=s_id,
                signature_name=name,
                target_channel=chan,
                confidence_weight=conf,
                regex_pattern=pat,
                mitigation_action=mit,
                threat_description=desc
            )
            self._compiled[s_id] = re.compile(pat, re.IGNORECASE)

    def scan_communication(self, text: str) -> List[RecruiterImpersonationSignature]:
        """Scans message text against all compiled recruiter impersonation patterns."""
        matches = []
        for s_id, pattern in self._compiled.items():
            if pattern.search(text):
                matches.append(self.signatures[s_id])
        return matches
