"""
JobGuard Core Security - MITRE ATT&CK Enterprise Knowledge Base Expanded Volume K
Detailed enterprise MITRE ATT&CK mappings covering Lateral Movement (TA0008) and Collection (TA0009)
in enterprise recruitment account takeover, inMail hijacking, and corporate credential theft.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MITREAttackKBEntryK:
    attack_id: str
    tactic_name: str
    technique_name: str
    recruitment_fraud_application: str
    indicator_patterns: List[str]
    mitigation_strategies: List[str]
    threat_actor_examples: List[str]


class MITREAttackEnterpriseKBExpandedK:
    """Master expanded MITRE ATT&CK knowledge base volume K."""

    def __init__(self):
        self.entries: Dict[str, MITREAttackKBEntryK] = {}
        self._seed_kb_k()

    def _seed_kb_k() -> None:
        """Register enterprise ATT&CK technique profiles."""

        data = [
            (
                "T1534",
                "Lateral Movement",
                "Internal Spearphishing",
                "Adversaries compromise legitimate HR recruiter email accounts to send phishing offers to external candidates with high domain reputation.",
                ["Legitimate corporate sender domain but anomalous reply-to address", "Sudden bulk outbound recruitment campaign"],
                ["Enforce mandatory FIDO2 hardware keys for HR personnel", "Automated outbound mail volume anomaly detection"],
                ["SilverPhish", "APT29"]
            ),
            (
                "T1114.002",
                "Collection",
                "Email Collection: Remote Email Collection",
                "Adversary accesses compromised recruiter mailboxes via IMAP/Graph API to steal candidate resumes and historical offer letters.",
                ["Anomalous OAuth consent permissions granted to third-party mail applications"],
                ["Audit Azure AD / Google Workspace application consent permissions", "Block unapproved mail sync apps"],
                ["Lazarus Group", "FIN11"]
            ),
            (
                "T1566.003",
                "Initial Access",
                "Phishing: Spearphishing via Service",
                "Utilizing legitimate recruitment platforms (LinkedIn, Indeed, ZipRecruiter) to deliver direct malicious links in candidate inboxes.",
                ["Direct message containing link to URL shortener or unverified external landing page"],
                ["Real-time browser extension link sandboxing and domain reputation scanning"],
                ["Syndicate-Alpha", "CryptoTask Ring"]
            )
        ]

        for a_id, tac, tech, app, ind, mit, actors in data:
            self.entries[a_id] = MITREAttackKBEntryK(
                attack_id=a_id,
                tactic_name=tac,
                technique_name=tech,
                recruitment_fraud_application=app,
                indicator_patterns=ind,
                mitigation_strategies=mit,
                threat_actor_examples=actors
            )

    def get_technique(self, attack_id: str) -> Optional[MITREAttackKBEntryK]:
        return self.entries.get(attack_id)
