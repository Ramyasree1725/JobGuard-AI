"""
JobGuard Core Security - Comprehensive MITRE ATT&CK & Fraud Heuristics Matrix
Maps cybercrime tactics, techniques, and threat indicators across social engineering,
identity theft, corporate domain spoofing, and advance-fee recruitment scams.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class FraudHeuristicRule:
    rule_id: str
    mitre_attack_id: str
    rule_name: str
    threat_vector: str
    severity_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    confidence_weight: float
    regex_pattern: str
    mitigation_action: str
    explanation: str


class ComprehensiveCVEFraudHeuristicsMatrix:
    """Master rule engine linking cyber security threat frameworks to recruitment fraud."""

    def __init__(self):
        self.rules: Dict[str, FraudHeuristicRule] = {}
        self._initialize_rules()

    def _initialize_rules(self) -> None:
        """Register comprehensive rule definitions."""

        rule_data = [
            ("HR-001", "T1566.002", "Phishing via Deceptive Spearfishing Link", "PHISHING_LINK", "CRITICAL", 0.95, r"https?://(?:[a-zA-Z0-9-]+\.)*(?:google|microsoft|amazon|apple)-[a-zA-Z0-9-]+\.[a-z]{2,}", "Block domain and inspect SSL certificate provenance.", "Attacker creates lookalike domain containing brand name combined with hyphens."),
            ("HR-002", "T1589.001", "Credentials & Identity Dossier Harvesting", "PII_HARVEST", "CRITICAL", 0.98, r"(?:enter|provide|upload)\s+(?:ssn|social\s+security|passport|id\s+card)\s+to\s+(?:apply|proceed)", "Cease submission. Real employers only collect SSN via authenticated payroll portal post-offer.", "Demands government identity documents prior to candidate interview or formal verification."),
            ("HR-003", "T1586.002", "Compromised / Impersonated Recruiter Email", "EMAIL_IMPERSONATION", "HIGH", 0.90, r"from:\s*.*@(gmail|yahoo|hotmail|outlook)\.com.*(?:google|apple|meta|amazon)\s+recruitment", "Flag email as unauthenticated spoofing attempt.", "High-profile corporate recruiters never conduct hiring via public free webmail accounts."),
            ("HR-004", "T1204.002", "Malicious Assessment Code Execution Lure", "MALWARE_LURE", "CRITICAL", 0.99, r"(?:clone|download|install)\s+this\s+(?:github|npm|repo|zip)\s+to\s+complete\s+coding\s+test", "Analyze repository in isolated sandbox before installing dependencies.", "Adversaries trick software engineers into cloning repositories with malicious post-install hooks."),
            ("HR-005", "T1056.003", "Counterfeit Form Webhook Credential Exfiltration", "FORM_EXFILTRATION", "HIGH", 0.92, r"<form\s+action=[\"']https?://(?:docs\.google\.com/forms|formkeep|typeform|t\.me)", "Verify that application forms submit to corporate ATS APIs rather than third-party form webhooks.", "Unverified third-party form processors used to collect sensitive candidate data."),
            ("HR-006", "T1657", "Financial Theft via Counterfeit Check Kickback", "CHECK_KICKBACK", "CRITICAL", 0.99, r"(?:deposit|cash)\s+check.*send.*(?:vendor|supplier|back)", "Refuse check deposit. Candidate is personally liable for all bounced funds.", "Adversary mails counterfeit check and requests portion to be wired to fake equipment vendor."),
            ("HR-007", "T1656", "Impersonation of Executive Hiring Leadership", "EXECUTIVE_IMPERSONATION", "HIGH", 0.88, r"i\s+am\s+(?:the\s+ceo|vice\s+president|head\s+of\s+hr).*urgent\s+task", "Verify executive identity via corporate intranet or directory.", "Attacker assumes identity of senior executive to pressure candidate into hurried compliance.")
        ]

        for r_id, m_id, name, vec, sev, conf, pat, mit, expl in rule_data:
            rule = FraudHeuristicRule(
                rule_id=r_id,
                mitre_attack_id=m_id,
                rule_name=name,
                threat_vector=vec,
                severity_level=sev,
                confidence_weight=conf,
                regex_pattern=pat,
                mitigation_action=mit,
                explanation=expl
            )
            self.rules[r_id] = rule

    def get_rule(self, rule_id: str) -> Optional[FraudHeuristicRule]:
        return self.rules.get(rule_id)
