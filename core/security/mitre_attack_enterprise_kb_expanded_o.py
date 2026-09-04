"""
JobGuard Core Security - MITRE ATT&CK Enterprise Knowledge Base Expanded Volume O
Detailed enterprise MITRE ATT&CK mappings covering Reconnaissance (TA0043) and Resource Development (TA0042)
in candidate demographic scraping, lookalike domain acquisition, and money mule recruitment infrastructure.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MITREAttackKBEntryO:
    attack_id: str
    tactic_name: str
    technique_name: str
    recruitment_fraud_application: str
    indicator_patterns: List[str]
    mitigation_strategies: List[str]
    threat_actor_examples: List[str]


class MITREAttackEnterpriseKBExpandedO:
    """Master expanded MITRE ATT&CK knowledge base volume O."""

    def __init__(self):
        self.entries: Dict[str, MITREAttackKBEntryO] = {}
        self._seed_kb_o()

    def _seed_kb_o() -> None:
        """Register enterprise ATT&CK technique profiles."""

        data = [
            (
                "T1593.001",
                "Reconnaissance",
                "Search Open Technical Databases: Social Media",
                "Scraping LinkedIn open-to-work candidate profiles to identify recently laid-off engineers vulnerable to job scams.",
                ["High-volume automated profile scraping activity on candidate professional profiles"],
                ["Educate job seekers on privacy settings and avoiding public display of personal contact details on resumes"],
                ["SilverPhish", "Apex Syndicate"]
            ),
            (
                "T1584.004",
                "Resource Development",
                "Compromise Infrastructure: Server",
                "Compromising legitimate WordPress job boards or university career center websites to host malicious application landing pages.",
                ["Unexpected new sub-paths or directories created under legitimate university or agency domains"],
                ["Continuous file integrity monitoring (FIM) and web application firewalls (WAF) on corporate career pages"],
                ["FIN7", "DevScam Syndicate"]
            ),
            (
                "T1587.001",
                "Resource Development",
                "Develop Capabilities: Malware",
                "Creating custom info-stealer binaries disguised as take-home coding challenges or interactive video interview codecs.",
                ["Compilation of new malware payloads with embedded candidate data exfiltration endpoints"],
                ["Automated static AST analysis and dynamic behavioral container sandboxing for all candidate testing bundles"],
                ["Lazarus Group"]
            )
        ]

        for a_id, tac, tech, app, ind, mit, actors in data:
            self.entries[a_id] = MITREAttackKBEntryO(
                attack_id=a_id,
                tactic_name=tac,
                technique_name=tech,
                recruitment_fraud_application=app,
                indicator_patterns=ind,
                mitigation_strategies=mit,
                threat_actor_examples=actors
            )

    def get_technique(self, attack_id: str) -> Optional[MITREAttackKBEntryO]:
        return self.entries.get(attack_id)
