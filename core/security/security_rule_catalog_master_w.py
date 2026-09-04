"""
JobGuard Core Security - Security Rule Catalog Master Volume W
Contains behavioral detection signatures for simulated government compliance clearance seals,
fake FINRA / SEC recruiter background certifications, and deceptive regulatory bond claims.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class MasterSecurityRuleW:
    rule_id: str
    rule_name: str
    category: str
    risk_score_impact: float
    regex_pattern: str
    min_word_match_threshold: int
    remediation_action: str
    technical_description: str


class SecurityRuleCatalogMasterW:
    """Master expanded catalog of behavioral detection rules volume W."""

    def __init__(self):
        self.rules: Dict[str, MasterSecurityRuleW] = {}
        self._compiled: Dict[str, re.Pattern] = {}
        self._seed_rules_w()

    def _seed_rules_w() -> None:
        """Register security detection rules."""

        rules_list = [
            (
                "RULE-W-001",
                "Simulated FINRA / SEC Candidate Background Bond Lure",
                "SECURITIES_DECEPTION",
                98.0,
                r"(?:finra|sec)\s+(?:requires|mandates)\s+(?:a\s+)?mandatory\s+candidate\s+(?:compliance|fidelity)\s+bond\s+of\s+\$?\d+",
                1,
                "Immediate critical alert. FINRA and SEC rules prohibit demanding candidate bond deposits for employment.",
                "Detects fraudulent assertions that securities regulators mandate advance employee fidelity bond payments."
            ),
            (
                "RULE-W-002",
                "Fake Corporate Compliance Accreditation Seal Claim",
                "DOCUMENT_FORGERY",
                86.0,
                r"(?:certified|audited)\s+by\s+(?:the\s+global\s+anti-fraud\s+recruitment\s+association|federal\s+hiring\s+board)",
                1,
                "Verify employer registration directly on official state corporation registry.",
                "Detects fabricated regulatory accreditation claims designed to build artificial trust on scam websites."
            ),
            (
                "RULE-W-003",
                "Unregistered Offshore Payroll Intermediary Directive",
                "PAYROLL_FRAUD",
                93.0,
                r"(?:payroll|salary)\s+(?:will\s+be\s+processed|disbursed)\s+through\s+(?:an\s+offshore|unlisted)\s+(?:escrow|disbursement)\s+agent",
                1,
                "Refuse arrangement. Legitimate employers process payroll through registered domestic payroll providers (e.g. ADP, Paychex, Gusto).",
                "Detects diversion of wage processing through shadowy offshore entities."
            )
        ]

        for r_id, name, cat, impact, pat, min_w, rem, desc in rules_list:
            rule = MasterSecurityRuleW(
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

    def scan_text(self, text: str) -> List[MasterSecurityRuleW]:
        """Scans input text against all compiled volume W rules."""
        matched = []
        for r_id, compiled_pat in self._compiled.items():
            if compiled_pat.search(text):
                matched.append(self.rules[r_id])
        return matched
