"""
JobGuard Core Security - MITRE ATT&CK Enterprise Knowledge Base Expanded Volume I
Detailed enterprise MITRE ATT&CK mappings covering Execution (TA0002) and Persistence (TA0003)
in developer recruitment supply chain attacks and candidate endpoint compromise.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MITREAttackKBEntryI:
    attack_id: str
    tactic_name: str
    technique_name: str
    recruitment_fraud_application: str
    indicator_patterns: List[str]
    mitigation_strategies: List[str]
    threat_actor_examples: List[str]


class MITREAttackEnterpriseKBExpandedI:
    """Master expanded MITRE ATT&CK knowledge base volume I."""

    def __init__(self):
        self.entries: Dict[str, MITREAttackKBEntryI] = {}
        self._seed_kb_i()

    def _seed_kb_i(self) -> None:
        """Register enterprise ATT&CK technique profiles."""

        data = [
            (
                "T1059.006",
                "Execution",
                "Command and Scripting Interpreter: Python",
                "Adversary instructs candidate to execute Python evaluation scripts containing base64 obfuscated payload downloaders.",
                ["base64.b64decode in assessment setup.py", "subprocess.Popen spawning netcat/reverse shells"],
                ["Static code analysis with AST visitor to block dangerous imports (os.system, subprocess, socket)"],
                ["Lazarus Group", "DevScam Syndicate"]
            ),
            (
                "T1195.001",
                "Initial Access",
                "Supply Chain Compromise: Compromised Software Dependencies",
                "Delivering take-home assessment starter templates containing backdoored PyPI or npm packages.",
                ["requirements.txt containing lookalike package names (e.g. reqeusts instead of requests)"],
                ["Hash verification of all third-party package dependencies against official PyPI/NPM indexes"],
                ["Lazarus Group", "FIN7"]
            ),
            (
                "T1136.001",
                "Persistence",
                "Create Account: Local Account",
                "Malicious assessment test script creates a hidden administrative user account on the candidate's development machine.",
                ["useradd / net user commands executed during test suite run"],
                ["Run coding tests inside non-root Docker containers with read-only root filesystems"],
                ["Lazarus Group"]
            )
        ]

        for a_id, tac, tech, app, ind, mit, actors in data:
            self.entries[a_id] = MITREAttackKBEntryI(
                attack_id=a_id,
                tactic_name=tac,
                technique_name=tech,
                recruitment_fraud_application=app,
                indicator_patterns=ind,
                mitigation_strategies=mit,
                threat_actor_examples=actors
            )

    def get_technique(self, attack_id: str) -> Optional[MITREAttackKBEntryI]:
        return self.entries.get(attack_id)
