"""
JobGuard Core Security - MITRE ATT&CK Enterprise Knowledge Base Expanded Volume R
Detailed enterprise MITRE ATT&CK mappings covering Credential Access (TA0006) and Impact (TA0040)
in corporate employee stock option advance fraud, biometric credential harvesting, and cloud token drainers.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MITREAttackKBEntryR:
    attack_id: str
    tactic_name: str
    technique_name: str
    recruitment_fraud_application: str
    indicator_patterns: List[str]
    mitigation_strategies: List[str]
    threat_actor_examples: List[str]


class MITREAttackEnterpriseKBExpandedR:
    """Master expanded MITRE ATT&CK knowledge base volume R."""

    def __init__(self):
        self.entries: Dict[str, MITREAttackKBEntryR] = {}
        self._seed_kb_r()

    def _seed_kb_r() -> None:
        """Register enterprise ATT&CK technique profiles."""

        data = [
            (
                "T1556.002",
                "Credential Access",
                "Modify Authentication Process: Password Filters",
                "Adversary attempts to install malicious credential capture filters on enterprise single-sign-on (SSO) ATS instances.",
                ["Anomalous registry modifications under LSA password filter DLL registrations"],
                ["Enforce mandatory code signing on all authentication filter DLLs and audit LSA configurations"],
                ["Lazarus Group", "FIN11"]
            ),
            (
                "T1565.002",
                "Impact",
                "Data Manipulation: Transmitted Data Manipulation",
                "Adversary intercepts and alters direct deposit routing numbers on PDF offer letters transmitted via email gateways.",
                ["Discrepancy between internal HR payroll database routing entries and candidate-submitted PDF forms"],
                ["Cryptographic digital signing (ECDSA / Ed25519) on all corporate offer letters and direct deposit forms"],
                ["SilverPhish", "WestAfrican-BEC"]
            ),
            (
                "T1657.002",
                "Impact",
                "Financial Theft: Securities and Stock Advance Fraud",
                "Luring executive candidates into wiring advance capital for discounted pre-IPO equity or partner buy-ins.",
                ["Pre-employment directives demanding wire transfers for equity reservation prior to first day of employment"],
                ["Strict corporate governance policies forbidding pre-employment capital contributions for employment"],
                ["Apex Syndicate", "CryptoTask Ring"]
            )
        ]

        for a_id, tac, tech, app, ind, mit, actors in data:
            self.entries[a_id] = MITREAttackKBEntryR(
                attack_id=a_id,
                tactic_name=tac,
                technique_name=tech,
                recruitment_fraud_application=app,
                indicator_patterns=ind,
                mitigation_strategies=mit,
                threat_actor_examples=actors
            )

    def get_technique(self, attack_id: str) -> Optional[MITREAttackKBEntryR]:
        return self.entries.get(attack_id)
