"""
JobGuard Core Security - Security Rule Catalog Master Volume O
Contains behavioral signatures for detecting simulated escrow holding agreements,
fake crypto task rating dashboards, and automated referral commission cascades.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleO:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterO:
    """Master expanded catalog of behavioral detection rules volume O."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleO] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_o()

    def _seed_rules_o() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-O-001",
                "Simulated Escrow Holding Pretext",
                "ESCROW_FRAUD",
                94.0,
                r"(?:funds|allowance)\s+(?:are\s+held|secured)\s+in\s+(?:our\s+third-party|online)\s+escrow\s+account\s+pending\s+your\s+deposit",
                1,
                "Do not deposit personal funds to release escrow. Legitimate employers disburse wages directly.",
                "Detects claims that candidate funds or allowances are locked in escrow requiring an advance deposit to unlock."
            ),
            (
                "RULE-O-002",
                "Automated Referral Pyramid Commission Lure",
                "PYRAMID_SCHEME",
                91.0,
                r"(?:earn|receive)\s+\d+%\s+commission\s+(?:from|on)\s+every\s+(?:friend|user|sub-agent)\s+you\s+refer\s+to\s+the\s+platform",
                1,
                "Refuse participation. Multi-level referral commission models for job tasks are illegal pyramid schemes.",
                "Detects multi-tier referral pyramid incentives integrated into crypto task rating scams."
            ),
            (
                "RULE-O-003",
                "Task Reset Penalty Surcharge",
                "TASK_FRAUD",
                98.0,
                r"(?:account\s+frozen|task\s+incomplete).*(?:deposit|recharge)\s+\$?\d+.*(?:to\s+reset|to\s+unfreeze|to\s+withdraw)",
                1,
                "Immediate critical alert. Cease sending funds. The platform will continue to demand larger amounts.",
                "Detects predatory algorithms locking user balances and demanding exponential deposits to withdraw earnings."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleO(
                rule_id=r_id,
                rule_name=name,
                category=cat,
                risk_score_impact=impact,
                regex_pattern=pat,
                min_word_match_threshold=min_w,
                remediation_action=rem,
                technical_description=desc
            )
            self.rules[r_id] = rule
            self._compiled[r_id] = re.compile(pat, re.IGNORECASE)

    def scan_text(self, text: str) -> List[MasterSecurityRuleO]:
        """Scans input text against all compiled volume O rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
