"""
JobGuard Core Network - DNS Telemetry & Fast-Flux DGA Classifier
Analyzes DNS resolution characteristics, Shannon character entropy for Domain Generation
Algorithms (DGA), fast-flux TTL rotations, and suspicious DNSSEC configurations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math
import collections
import re


@dataclass
class DNSRecordSet:
    domain_name: str
    a_records: List[str]
    mx_records: List[Tuple[int, str]]  # (priority, host)
    ns_records: List[str]
    txt_records: List[str]
    soa_ttl: int
    has_dnssec: bool


@dataclass
class DNSThreatReport:
    domain_name: str
    shannon_entropy: float
    is_likely_dga: bool
    is_fast_flux: bool
    has_valid_mx: bool
    threat_score: float
    detected_indicators: List[str]
    recommendation: str


class DNSTelemetryEngine:
    """Classifies algorithmic domain generation, fast-flux evasion, and DNS routing anomalies."""

    SUSPICIOUS_TLDS: Set[str] = {
        "top", "xyz", "club", "online", "work", "loan", "click", "site", "vip", "cfd", "sbs", "rest"
    }

    def __init__(self):
        self.fast_flux_history: Dict[str, List[Set[str]]] = collections.defaultdict(list)

    def calculate_shannon_entropy(self, s: str) -> float:
        """Computes Shannon information entropy (bits per character) of a domain label."""
        if not s:
            return 0.0
        # Consider only the primary domain name label without TLD
        label = s.split(".")[0].lower()
        counts = collections.Counter(label)
        entropy = 0.0
        length = len(label)
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy

    def analyze_dns_telemetry(self, dns_data: DNSRecordSet) -> DNSThreatReport:
        """Evaluates DNS resolution data against threat detection heuristics."""
        domain = dns_data.domain_name.lower().strip()
        parts = domain.split(".")
        main_label = parts[0]
        tld = parts[-1] if len(parts) > 1 else ""

        indicators: List[str] = []
        base_threat = 0.0

        # 1. Shannon Entropy Analysis (DGA Detection)
        entropy = self.calculate_shannon_entropy(main_label)
        is_dga = False
        
        # English domain names typically have entropy between 2.2 and 3.5. DGA domains > 3.8
        if entropy > 3.8 and len(main_label) > 10:
            is_dga = True
            base_threat += 45.0
            indicators.append(f"High character entropy ({entropy:.2f} bits) indicates Domain Generation Algorithm (DGA).")

        # 2. Suspicious / High-Abuse TLD
        if tld in self.SUSPICIOUS_TLDS:
            base_threat += 25.0
            indicators.append(f"Domain utilizes high-abuse Top Level Domain (.{tld}) commonly seen in disposable scam campaigns.")

        # 3. Fast-Flux Check (Extremely low TTL with rotating multiple A records)
        is_fast_flux = False
        if dns_data.soa_ttl < 300 and len(dns_data.a_records) >= 3:
            is_fast_flux = True
            base_threat += 35.0
            indicators.append(f"Fast-Flux DNS signature detected: TTL is {dns_data.soa_ttl}s with {len(dns_data.a_records)} rotating IP addresses.")

        # 4. Absence of valid Mail Exchanger (MX) records
        has_mx = len(dns_data.mx_records) > 0
        if not has_mx:
            base_threat += 20.0
            indicators.append("Domain has zero MX records; cannot legally receive inbound recruitment communications.")

        # 5. Consecutive consonant clusters / numeric ratio
        digits = sum(1 for c in main_label if c.isdigit())
        if len(main_label) > 0 and (digits / len(main_label)) > 0.4:
            base_threat += 20.0
            indicators.append(f"Excessive numeric digit density ({digits}/{len(main_label)}) in domain label.")

        # Recommendation
        if base_threat >= 60.0:
            rec = "CRITICAL: Block all traffic to this domain. Signature consistent with active cybercrime / scam infrastructure."
        elif base_threat >= 25.0:
            rec = "WARNING: Domain exhibits atypical DNS configuration. Require manual administrator verification."
        else:
            rec = "DNS records reflect legitimate, stable hosting configuration."

        return DNSThreatReport(
            domain_name=domain,
            shannon_entropy=entropy,
            is_likely_dga=is_dga,
            is_fast_flux=is_fast_flux,
            has_valid_mx=has_mx,
            threat_score=min(100.0, max(0.0, base_threat)),
            detected_indicators=indicators if indicators else ["Standard DNS configuration."],
            recommendation=rec
        )
