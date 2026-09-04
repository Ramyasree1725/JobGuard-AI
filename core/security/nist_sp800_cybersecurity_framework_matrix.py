"""
JobGuard Core Security - NIST SP 800-53 Rev 5 & CSF 2.0 Security Control Matrix
Maps National Institute of Standards and Technology (NIST) privacy and security controls
(AC-2, IA-5, SC-8, SI-4) to recruitment fraud defense and candidate telemetry processing.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class NISTCSFFunction(Enum):
    GOVERN = "GOVERN"
    IDENTIFY = "IDENTIFY"
    PROTECT = "PROTECT"
    DETECT = "DETECT"
    RESPOND = "RESPOND"
    RECOVER = "RECOVER"


@dataclass
class NISTSecurityControlRecord:
    control_id: str
    control_title: str
    csf_function: NISTCSFFunction
    sp800_53_family: str
    recruitment_fraud_relevance: str
    implementation_guidance: str
    automated_verification_status: bool


class NISTSP800CybersecurityFrameworkMatrix:
    """Master mapping matrix for NIST cybersecurity controls applicable to JobGuard AI."""

    def __init__(self):
        self.controls: Dict[str, NISTSecurityControlRecord] = {}
        self._initialize_controls()

    def _initialize_controls(self) -> None:
        """Register NIST security controls."""

        controls_data = [
            (
                "AC-2",
                "Account Management & Candidate Onboarding Credential Isolation",
                NISTCSFFunction.PROTECT,
                "Access Control",
                "Prevents premature provisioning of enterprise accounts to unverified recruiters or external contractors.",
                "Enforce multi-stage zero-trust candidate identity proofing prior to directory account provisioning.",
                True
            ),
            (
                "IA-5",
                "Authenticator Management & Anti-Spoofing Protocols",
                NISTCSFFunction.PROTECT,
                "Identification and Authentication",
                "Protects against lookalike domain spoofing and phishing portal credential harvesting.",
                "Enforce FIDO2 / WebAuthn phishing-resistant hardware MFA on all recruiter and admin portals.",
                True
            ),
            (
                "SI-4",
                "System Monitoring & Threat Intelligence Stream Ingestion",
                NISTCSFFunction.DETECT,
                "System and Information Integrity",
                "Ingests real-time threat feeds to flag malicious ATS clones and suspicious check routing numbers.",
                "Deploy sliding-window telemetry aggregators and real-time Kafka partition routing for IoCs.",
                True
            ),
            (
                "SC-8",
                "Transmission Confidentiality & Cryptographic Audit Trails",
                NISTCSFFunction.PROTECT,
                "System and Communications Protection",
                "Protects candidate resume payloads and generates immutable SHA-256 event audit ledgers.",
                "Enforce TLS 1.3 in transit and AES-256 GCM client-side envelope encryption at rest.",
                True
            ),
            (
                "IR-4",
                "Incident Handling & Automated Takedown Coordination",
                NISTCSFFunction.RESPOND,
                "Incident Response",
                "Coordinates automated abuse reports to domain registrars and hosting providers for active scam portals.",
                "Deploy automated registrar takedown notice generation pipelines with ICANN RAA citations.",
                True
            )
        ]

        for c_id, title, func, fam, rel, guide, auto in controls_data:
            self.controls[c_id] = NISTSecurityControlRecord(
                control_id=c_id,
                control_title=title,
                csf_function=func,
                sp800_53_family=fam,
                recruitment_fraud_relevance=rel,
                implementation_guidance=guide,
                automated_verification_status=auto
            )

    def get_control(self, control_id: str) -> Optional[NISTSecurityControlRecord]:
        return self.controls.get(control_id)
