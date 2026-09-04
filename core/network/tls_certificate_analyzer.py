"""
JobGuard Core Network - TLS/SSL Certificate Transparency & Trust Chain Analyzer
Analyzes X.509 certificate metadata, Certificate Authority (CA) legitimacy,
SAN extension abuse, certificate age, and short-lived TLS fraud indicators.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import datetime


class CertificateValidationLevel(Enum):
    EXTENDED_VALIDATION_EV = "EXTENDED_VALIDATION_EV"
    ORGANIZATION_VALIDATION_OV = "ORGANIZATION_VALIDATION_OV"
    DOMAIN_VALIDATION_DV = "DOMAIN_VALIDATION_DV"
    SELF_SIGNED = "SELF_SIGNED"
    UNTRUSTED_ROOT = "UNTRUSTED_ROOT"


@dataclass
class X509CertificateRecord:
    subject_common_name: str
    issuer_organization: str
    issuer_common_name: str
    validation_level: CertificateValidationLevel
    subject_alt_names: List[str]
    valid_from: datetime.datetime
    valid_until: datetime.datetime
    signature_algorithm: str
    serial_number: str
    is_revoked: bool = False
    ct_log_verified: bool = True


@dataclass
class TLSTrustAuditReport:
    domain_queried: str
    certificate: Optional[X509CertificateRecord]
    cert_age_days: int
    is_ephemeral_dv_cert: bool
    is_ev_or_ov_verified: bool
    risk_score: float
    detected_anomalies: List[str]
    trust_verdict: str


class TLSCertificateAnalyzer:
    """Evaluates the cryptographic trust and provenance of website and mail server TLS certificates."""

    HIGH_TRUST_ENTERPRISE_CAS: Set[str] = {
        "DigiCert Inc", "Entrust, Inc.", "Sectigo Limited", "GlobalSign nv-sa",
        "GeoTrust Inc.", "IdenTrust", "Amazon"
    }

    AUTOMATED_FREE_CAS: Set[str] = {
        "Let's Encrypt", "cPanel, Inc.", "ZeroSSL", "Cloudflare, Inc."
    }

    def __init__(self):
        self.cached_records: Dict[str, X509CertificateRecord] = {}

    def audit_certificate(
        self,
        domain: str,
        cert: Optional[X509CertificateRecord] = None,
        claimed_enterprise_name: Optional[str] = None
    ) -> TLSTrustAuditReport:
        """Evaluates TLS certificate authenticity against enterprise security standards."""
        if not cert:
            # Fallback mock evaluation for un-queried domains
            return TLSTrustAuditReport(
                domain_queried=domain,
                certificate=None,
                cert_age_days=0,
                is_ephemeral_dv_cert=False,
                is_ev_or_ov_verified=False,
                risk_score=50.0,
                detected_anomalies=["No valid TLS certificate record presented for audit."],
                trust_verdict="UNKNOWN_TLS_STATUS"
            )

        anomalies: List[str] = []
        base_risk = 0.0
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Calculate certificate age
        cert_age_days = (now - cert.valid_from).days
        validity_span_days = (cert.valid_until - cert.valid_from).days

        # Check 1: Self-signed or untrusted root
        if cert.validation_level in (CertificateValidationLevel.SELF_SIGNED, CertificateValidationLevel.UNTRUSTED_ROOT):
            base_risk += 85.0
            anomalies.append(f"CRITICAL: Certificate is {cert.validation_level.value}, lacking verified root CA trust.")

        # Check 2: Revocation
        if cert.is_revoked:
            base_risk += 95.0
            anomalies.append("CRITICAL: Certificate has been explicitly REVOKED by issuing authority.")

        # Check 3: Short-lived / newly minted domain validation
        is_ephemeral = False
        if cert.issuer_organization in self.AUTOMATED_FREE_CAS:
            is_ephemeral = True
            if cert_age_days < 14:
                base_risk += 40.0
                anomalies.append(f"Newly issued free DV certificate ({cert_age_days} days old from {cert.issuer_organization}). Fraud campaigns frequently use fresh free certificates.")
            elif cert_age_days < 60:
                base_risk += 15.0

        # Check 4: Mismatch between claimed Fortune 500 employer and free DV cert
        if claimed_enterprise_name and is_ephemeral:
            base_risk += 35.0
            anomalies.append(f"Discrepancy: Alleged Fortune 500 entity '{claimed_enterprise_name}' is using free automated DV cert rather than corporate EV/OV infrastructure.")

        # Check 5: SAN Wildcard / Multi-tenant dilution
        if len(cert.subject_alt_names) > 50:
            base_risk += 25.0
            anomalies.append(f"Suspiciously broad SAN certificate with {len(cert.subject_alt_names)} shared alt names, typical of low-cost shared hosting.")

        # Trust verdict
        is_ev_ov = cert.validation_level in (CertificateValidationLevel.EXTENDED_VALIDATION_EV, CertificateValidationLevel.ORGANIZATION_VALIDATION_OV)
        if base_risk >= 70.0:
            verdict = "CRITICAL_TLS_FRAUD_RISK"
        elif base_risk >= 30.0:
            verdict = "MODERATE_CAUTION_REQUIRED"
        else:
            verdict = "TRUSTED_TLS_INFRASTRUCTURE"

        return TLSTrustAuditReport(
            domain_queried=domain,
            certificate=cert,
            cert_age_days=max(0, cert_age_days),
            is_ephemeral_dv_cert=is_ephemeral,
            is_ev_or_ov_verified=is_ev_ov,
            risk_score=min(100.0, max(0.0, base_risk)),
            detected_anomalies=anomalies if anomalies else ["Valid TLS certificate issued by verified CA."],
            trust_verdict=verdict
        )
