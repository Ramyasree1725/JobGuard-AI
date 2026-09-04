"""
JobGuard Core Network - DNS Resolver & Domain Reputation Inspector
Performs simulated DNS record resolution (A, AAAA, MX, TXT, SPF, DMARC),
computes domain age risk multipliers, and audits mail server credibility.
"""

import hashlib
import time
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class DNSRecord:
    record_type: str  # "A", "MX", "TXT", "NS"
    value: str
    ttl: int = 300


@dataclass
class DomainReputationReport:
    domain: str
    is_resolvable: bool
    has_mx_record: bool
    has_spf_record: bool
    has_dmarc_record: bool
    is_disposable_email_domain: bool
    domain_age_days: int
    risk_penalty: float
    notes: List[str] = field(default_factory=list)


class DNSResolver:
    """DNS & Mail Infrastructure Auditor for recruitment authenticity checks."""

    DISPOSABLE_DOMAINS = {
        "tempmail.com", "guerrillamail.com", "10minutemail.com", "throwawaymail.com",
        "mailinator.com", "yopmail.com", "trashmail.com", "sharklasers.com"
    }

    FREE_DOMAINS = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com"
    }

    def __init__(self):
        self._cache: Dict[str, DomainReputationReport] = {}

    def audit_domain(self, domain: str) -> DomainReputationReport:
        """Inspect domain DNS records and compute security reputation score."""
        domain_clean = domain.strip().lower()
        if domain_clean in self._cache:
            return self._cache[domain_clean]

        notes: List[str] = []
        risk = 0.0

        is_disposable = domain_clean in self.DISPOSABLE_DOMAINS
        if is_disposable:
            risk += 50.0
            notes.append("Domain is a known burner / disposable email provider")

        is_free = domain_clean in self.FREE_DOMAINS
        if is_free:
            notes.append("Domain is a public free webmail provider (unverified corporate identity)")

        # Check for suspicious TLDs (.xyz, .top, .cc, .cfd)
        if re.search(r"\.(xyz|top|cc|cfd|work|click|gq|ml|tk)$", domain_clean):
            risk += 25.0
            notes.append("Domain utilizes high-abuse cheap/free top-level domain (TLD)")

        # Simulated MX & SPF checks
        has_mx = True
        has_spf = not is_disposable
        has_dmarc = not is_disposable

        if not has_spf:
            risk += 15.0
            notes.append("Missing or unverified SPF (Sender Policy Framework) record")

        report = DomainReputationReport(
            domain=domain_clean,
            is_resolvable=True,
            has_mx_record=has_mx,
            has_spf_record=has_spf,
            has_dmarc_record=has_dmarc,
            is_disposable_email_domain=is_disposable,
            domain_age_days=180 if not is_disposable else 2,
            risk_penalty=min(100.0, risk),
            notes=notes
        )

        self._cache[domain_clean] = report
        return report
