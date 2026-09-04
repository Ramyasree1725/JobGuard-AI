"""
JobGuard Core Security - MITRE ATT&CK Enterprise Knowledge Base Expanded Volume Q
Detailed enterprise MITRE ATT&CK mappings covering Execution (TA0002) and Persistence (TA0003)
in developer take-home assessment starter projects, container breakout exploits, and IDE plugin malware.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MITREAttackKBEntryQ:
    attack_id: str
    tactic_name: str
    technique_name: str
    recruitment_fraud_application: str
    indicator_patterns: List[str]
    mitigation_strategies: List[str]
    threat_actor_examples: List[str]


class MITREAttackEnterpriseKBExpandedQ:
    """Master expanded MITRE ATT&CK knowledge base volume Q."""

    def __init__(self):
        self.entries: Dict[str, MITREAttackKBEntryQ] = {}
        self._seed_kb_q()

    def _seed_kb_q() -> None:
        """Register enterprise ATT&CK technique profiles."""

        data = [
            (
                "T1059.004",
                "Execution",
                "Command and Scripting Interpreter: Unix Shell",
                "Delivering take-home assessment Makefiles containing encoded curl/wget shell commands that execute during `make test`.",
                ["Makefile targets executing base64 decode and piping directly into /bin/sh or bash"],
                ["Enforce static Makefile inspection and container sandboxes with network egress disabled during compilation"],
                ["Lazarus Group", "DevScam Syndicate"]
            ),
            (
                "T1546.015",
                "Persistence",
                "Event Triggered Execution: Component Object Model Hijacking",
                "Malicious assessment package writing registry keys to hijack candidate Windows COM objects for permanent backdoor persistence.",
                ["Registry writes targeting HKCU\\Software\\Classes\\CLSID under build scripts"],
                ["Run developer testing tools inside non-persistent virtual machines with automatic state rollback"],
                ["FIN7"]
            ),
            (
                "T1574.006",
                "Privilege Escalation",
                "Hijack Execution Flow: Dynamic Linker Hijacking",
                "Manipulating LD_PRELOAD or DYLD_INSERT_LIBRARIES in Linux/macOS assessment repository environment setup scripts.",
                ["Exporting LD_PRELOAD variables pointing to custom shared object (.so) files"],
                ["Sanitize and override all dynamic linker environment variables in candidate evaluation sandboxes"],
                ["Lazarus Group"]
            )
        ]

        for a_id, tac, tech, app, ind, mit, actors in data:
            self.entries[a_id] = MITREAttackKBEntryQ(
                attack_id=a_id,
                tactic_name=tac,
                technique_name=tech,
                recruitment_fraud_application=app,
                indicator_patterns=ind,
                mitigation_strategies=mit,
                threat_actor_examples=actors
            )

    def get_technique(self, attack_id: str) -> Optional[MITREAttackKBEntryQ]:
        return self.entries.get(attack_id)
