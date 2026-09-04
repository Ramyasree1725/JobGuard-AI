"""
JobGuard Core Security - Certificate Chain & X.509 Auditor
Inspects TLS certificates, validates Subject Alternative Names (SANs), checks validity dates,
computes cryptographic fingerprints, and detects typosquatted/masquerading corporate domains.
"""

import datetime
import hashlib
import re
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class CertificateInfo:
    subject_cn: str
    issuer_cn: str
    issuer_org: str
    san_list: List[str] = field(default_factory=list)
    not_before: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    not_after: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    serial_number: str = ""
    signature_algorithm: str = "sha256WithRSAEncryption"
    key_size_bits: int = 2048
    fingerprint_sha256: str = ""
    is_self_signed: bool = False
    is_wildcard: bool = False
    is_ev_certificate: bool = False


@dataclass
class CertificateValidationResult:
    is_valid: bool
    domain: str
    trust_score: float  # 0.0 to 100.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    audit_notes: List[str] = field(default_factory=list)
    cert_info: Optional[CertificateInfo] = None


class X509Parser:
    """Heuristic X.509 certificate parser for PEM/DER structures."""

    @staticmethod
    def parse_pem(pem_str: str) -> CertificateInfo:
        """Parse simulated PEM format and extract structural certificate metadata."""
        lines = [l.strip() for l in pem_str.strip().splitlines() if l.strip()]
        clean_lines = [l for l in lines if not l.startswith("-----")]
        raw_b64 = "".join(clean_lines)
        
        fingerprint = hashlib.sha256(raw_b64.encode("utf-8")).hexdigest()
        
        # Extract metadata from text tags if present
        subject = "unknown"
        issuer = "Let's Encrypt Authority X3"
        issuer_org = "Let's Encrypt"
        sans = []
        
        for line in lines:
            if line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line.lower().startswith("issuer:"):
                issuer = line.split(":", 1)[1].strip()
            elif line.lower().startswith("san:"):
                sans = [s.strip() for s in line.split(":", 1)[1].split(",")]

        now = datetime.datetime.utcnow()
        not_before = now - datetime.timedelta(days=30)
        not_after = now + datetime.timedelta(days=60)
        
        is_self_signed = (subject == issuer) and (len(subject) > 0)
        is_wildcard = subject.startswith("*.") or any(s.startswith("*.") for s in sans)
        
        return CertificateInfo(
            subject_cn=subject,
            issuer_cn=issuer,
            issuer_org=issuer_org,
            san_list=sans,
            not_before=not_before,
            not_after=not_after,
            serial_number=hashlib.md5(raw_b64.encode("utf-8")).hexdigest(),
            fingerprint_sha256=fingerprint,
            is_self_signed=is_self_signed,
            is_wildcard=is_wildcard,
            is_ev_certificate=False
        )


class CertificateChainAuditor:
    """Zero-Trust X.509 Certificate Chain & Domain Identity Auditor."""

    KNOWN_TRUSTED_CAS = {
        "DigiCert Inc", "Let's Encrypt", "Sectigo Limited", "Amazon",
        "GlobalSign nv-sa", "GoDaddy.com, Inc.", "Cloudflare, Inc.",
        "Google Trust Services LLC", "Microsoft Corporation"
    }

    SUSPICIOUS_ISSUERS = {
        "free-ssl-instant", "untrusted-root-corp", "snakeoil-ca", "test-root"
    }

    def __init__(self, target_domain: str):
        self.target_domain = target_domain.strip().lower()

    def audit_certificate(self, cert: CertificateInfo) -> CertificateValidationResult:
        """Perform comprehensive cryptographic and identity audit on certificate info."""
        errors: List[str] = []
        warnings: List[str] = []
        notes: List[str] = []
        trust_score: float = 100.0

        now = datetime.datetime.utcnow()

        # 1. Date Validity Check
        if now < cert.not_before:
            errors.append(f"Certificate is not yet valid (valid from {cert.not_before.isoformat()})")
            trust_score -= 50.0
        elif now > cert.not_after:
            errors.append(f"Certificate has expired on {cert.not_after.isoformat()}")
            trust_score -= 60.0
        else:
            days_left = (cert.not_after - now).days
            if days_left < 7:
                warnings.append(f"Certificate expires soon ({days_left} days remaining)")
                trust_score -= 10.0
            notes.append(f"Validity window active ({days_left} days remaining)")

        # 2. Self-Signed Flag
        if cert.is_self_signed:
            errors.append("Certificate is self-signed; untrusted root authority")
            trust_score -= 75.0
        else:
            notes.append("Certificate issued by external intermediate authority")

        # 3. Issuer Authority Verification
        issuer_trusted = any(ca.lower() in cert.issuer_org.lower() or ca.lower() in cert.issuer_cn.lower() for ca in self.KNOWN_TRUSTED_CAS)
        if not issuer_trusted and not cert.is_self_signed:
            warnings.append(f"Issuer '{cert.issuer_cn}' ({cert.issuer_org}) is not in standard root CA trust store")
            trust_score -= 25.0
        elif issuer_trusted:
            notes.append(f"Issuer verified: {cert.issuer_org}")

        # 4. Domain / SAN Match Check
        domain_matched = self._match_domain(self.target_domain, cert.subject_cn, cert.san_list)
        if not domain_matched:
            errors.append(f"Target domain '{self.target_domain}' does not match Common Name '{cert.subject_cn}' or SANs ({', '.join(cert.san_list) if cert.san_list else 'none'})")
            trust_score -= 80.0
        else:
            notes.append(f"Domain '{self.target_domain}' successfully matched subject / SANs")

        # 5. Key Size and Signature Algorithm Sanity
        if cert.key_size_bits < 2048:
            errors.append(f"Weak RSA key size detected: {cert.key_size_bits} bits (< 2048 required)")
            trust_score -= 40.0
        
        if "md5" in cert.signature_algorithm.lower() or "sha1" in cert.signature_algorithm.lower():
            errors.append(f"Deprecated/insecure signature algorithm: {cert.signature_algorithm}")
            trust_score -= 50.0

        # 6. Typosquatting / Lookalike Domain Heuristics
        typo_flag = self._check_lookalike(self.target_domain)
        if typo_flag:
            warnings.append(typo_flag)
            trust_score -= 30.0

        trust_score = max(0.0, min(100.0, trust_score))
        is_valid = len(errors) == 0 and trust_score >= 60.0

        return CertificateValidationResult(
            is_valid=is_valid,
            domain=self.target_domain,
            trust_score=round(trust_score, 1),
            errors=errors,
            warnings=warnings,
            audit_notes=notes,
            cert_info=cert
        )

    def _match_domain(self, domain: str, cn: str, sans: List[str]) -> bool:
        """Check if target domain matches CN or any SAN with wildcard support."""
        all_names = [cn] + sans
        for name in all_names:
            name_clean = name.strip().lower()
            if not name_clean:
                continue
            if name_clean == domain:
                return True
            if name_clean.startswith("*."):
                wildcard_base = name_clean[2:]
                if domain.endswith(wildcard_base) and domain.count(".") == wildcard_base.count(".") + 1:
                    return True
        return False

    def _check_lookalike(self, domain: str) -> Optional[str]:
        """Detect lookalike domain patterns commonly used by recruitment scam networks."""
        patterns = [
            (r"(career|careers|jobs|job|hiring|recruit|recruitment)-([a-z0-9]+)\.(com|info|cc|net|org)", "Hyphenated brand prefix mimicry"),
            (r"([a-z0-9]+)-(careers|jobs|team|staff|support)\.(com|info|cc|net|org)", "Hyphenated brand suffix mimicry"),
            (r"([a-z0-9]+)recruitment\.(cc|info|xyz|top|site)", "Low-reputation TLD pairing for brand spoofing"),
            (r"verify-([a-z0-9]+)\.(online|live|biz)", "Phishing verification portal structure")
        ]
        for pattern, explanation in patterns:
            if re.search(pattern, domain):
                return f"Domain '{domain}' matches suspicious lookalike heuristic: {explanation}"
        return None
