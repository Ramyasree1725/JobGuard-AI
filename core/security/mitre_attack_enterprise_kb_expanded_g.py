"""
JobGuard Core Security - MITRE ATT&CK Enterprise Knowledge Base Expanded Volume G
Detailed enterprise MITRE ATT&CK mappings covering Reconnaissance (TA0043),
Resource Development (TA0042), and Initial Access (TA0001) in recruitment fraud infrastructure.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MITREAttackKBEntryG:
    attack_id: str
    tactic_name: str
    technique_name: str
    recruitment_fraud_application: str
    indicator_patterns: List[str]
    mitigation_strategies: List[str]
    threat_actor_examples: List[str]


class MITREAttackEnterpriseKBExpandedG:
    """Master expanded MITRE ATT&CK knowledge base volume G."""

    def __init__(self):
        self.entries: Dict[str, MITREAttackKBEntryG] = {}
        self._seed_kb_g()

    def _seed_kb_g(self) -> None:
        """Register enterprise ATT&CK technique profiles."""

        data = [
            (
                "T1589.001",
                "Reconnaissance",
                "Gather Victim Identity Information: Credentials",
                "Adversaries harvest candidate resumes and personal email addresses from public job boards to conduct targeted spearphishing.",
                ["Mass resume scraping webhooks", "Harvesting applicant profiles via fake recruiter accounts"],
                ["Implement rate limiting on public candidate search directories", "Enforce candidate contact masking"],
                ["Lazarus Group", "SilverPhish Syndicate"]
            ),
            (
                "T1583.001",
                "Resource Development",
                "Acquire Infrastructure: Domains",
                "Purchasing typosquatted and lookalike domains (e.g. company-careers-desk.com) via privacy-shielded registrars.",
                ["Domain registrations with newly created WHOIS records (<30 days)", "Disposable registrar usage"],
                ["Continuous brand domain monitoring and proactive defensive domain acquisition", "Automated UDRP takedowns"],
                ["Syndicate-Alpha", "FIN7", "CryptoTask Ring"]
            ),
            (
                "T1585.002",
                "Resource Development",
                "Establish Accounts: Email Accounts",
                "Creating high-volume free public webmail accounts (Gmail, Yahoo, Outlook) using corporate executive display names.",
                ["Emails claiming corporate identity but routing through @gmail.com or @outlook.com"],
                ["Strict DMARC enforcement (p=reject) and public educational advisories regarding official recruitment channels"],
                ["WestAfrican-BEC", "Apex Syndicate"]
            )
        ]

        for a_id, tac, tech, app, ind, mit, actors in data:
            self.entries[a_id] = MITREAttackKBEntryG(
                attack_id=a_id,
                tactic_name=tac,
                technique_name=tech,
                recruitment_fraud_application=app,
                indicator_patterns=ind,
                mitigation_strategies=mit,
                threat_actor_examples=actors
            )

    def get_technique(self, attack_id: str) -> Optional[MITREAttackKBEntryG]:
        return self.entries.get(attack_id)
