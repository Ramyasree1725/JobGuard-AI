"""
JobGuard Core Compliance - International Regulatory & Security Standards Suite
Implements compliance control catalogs for SOC 2 Type II, ISO/IEC 27001:2022,
NIST Cybersecurity Framework 2.0, and GDPR Candidate Protection Principles.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ComplianceControl:
    framework: str  # "ISO27001", "SOC2", "NIST_CSF", "GDPR"
    control_id: str  # e.g., "A.5.15", "CC6.1", "PR.AC-1", "Art.5"
    domain: str
    title: str
    requirement_description: str
    audit_verification_procedure: str
    is_mandatory: bool = True


class RegulatoryFrameworksRegistry:
    """Master compliance mapping engine for enterprise recruitment security governance."""

    def __init__(self):
        self.controls: Dict[str, ComplianceControl] = {}
        self._framework_index: Dict[str, List[str]] = {}
        self._populate_controls()

    def register(self, ctrl: ComplianceControl) -> None:
        self.controls[ctrl.control_id] = ctrl
        f_clean = ctrl.framework.upper()
        if f_clean not in self._framework_index:
            self._framework_index[f_clean] = []
        self._framework_index[f_clean].append(ctrl.control_id)

    def _populate_controls(self) -> None:
        """Populate international cybersecurity and privacy controls."""
        controls_list = [
            # ISO/IEC 27001:2022 Controls
            ComplianceControl(
                framework="ISO27001",
                control_id="ISO-A.5.15",
                domain="Access Control",
                title="Access Control Policy for Candidate Records",
                requirement_description="Access to candidate resume records and PII must be restricted according to business need-to-know.",
                audit_verification_procedure="Verify role-based access control (RBAC) lists and quarterly access reviews."
            ),
            ComplianceControl(
                framework="ISO27001",
                control_id="ISO-A.8.24",
                domain="Cryptographic Controls",
                title="Use of Cryptography for In-Transit Offer Letters",
                requirement_description="All employment contracts, credentials, and identity documents must be encrypted in transit via TLS 1.3.",
                audit_verification_procedure="Audit SSL/TLS cipher suites and certificate validity."
            ),

            # SOC 2 Trust Services Criteria
            ComplianceControl(
                framework="SOC2",
                control_id="SOC2-CC6.1",
                domain="Logical and Physical Access Controls",
                title="Multi-Factor Authentication on Recruiter Portals",
                requirement_description="The entity implements logical access controls including mandatory MFA for all recruiter access points.",
                audit_verification_procedure="Inspect IdP logs for 100% MFA enforcement on recruiter admin logins."
            ),
            ComplianceControl(
                framework="SOC2",
                control_id="SOC2-CC7.2",
                domain="System Operations & Monitoring",
                title="Real-Time Detection of Malicious Recruitment Domains",
                requirement_description="The system monitors network events to identify and alert on trademark typosquatting or brand spoofing.",
                audit_verification_procedure="Review automated threat intelligence alerts and domain monitoring feeds."
            ),

            # GDPR Candidate Privacy
            ComplianceControl(
                framework="GDPR",
                control_id="GDPR-Art.5(1)(c)",
                domain="Data Minimization",
                title="Candidate Data Minimization Standard",
                requirement_description="Personal data collected must be adequate, relevant, and limited to what is necessary for candidate evaluation.",
                audit_verification_procedure="Verify that banking and national identity numbers are strictly forbidden prior to contract signing."
            ),
            ComplianceControl(
                framework="GDPR",
                control_id="GDPR-Art.17",
                domain="Right to Erasure",
                title="Right to Erasure ('Right to be Forgotten')",
                requirement_description="Candidates have the right to obtain the erasure of their personal recruitment data without undue delay.",
                audit_verification_procedure="Audit automated deletion workflows and retention lifecycle managers."
            )
        ]

        for c in controls_list:
            self.register(c)

    def get_controls_for_framework(self, framework: str) -> List[ComplianceControl]:
        ids = self._framework_index.get(framework.upper(), [])
        return [self.controls[cid] for cid in ids]
