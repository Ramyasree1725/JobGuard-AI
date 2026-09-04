"""
JobGuard Backend Service - Threat Intelligence Feed & IoC Sync
Syncs Indicators of Compromise (IoCs), known scammer UPI IDs, WhatsApp numbers,
and malicious recruitment domains from global threat sharing protocols (STIX/TAXII).
"""

import time
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class ThreatIndicator:
    indicator_id: str
    indicator_type: str  # "phone", "telegram", "upi", "domain", "email"
    value: str
    threat_actor: str
    confidence_score: float
    first_seen: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)


class ThreatIntelligenceFeed:
    """In-memory fast blacklist and IoC matcher."""

    def __init__(self):
        self._indicators: Dict[str, ThreatIndicator] = {}
        self._load_seed_indicators()

    def _load_seed_indicators(self) -> None:
        seed_data = [
            ("phone", "+91 98765 43210", "Digital Nexus Syndicate", 0.98, ["whatsapp_recruiter", "crypto_task"]),
            ("telegram", "@HiringManager_David", "Apex Global Impersonator", 0.99, ["fake_check", "telegram_only"]),
            ("upi", "hr.digitalnexus@paytm", "Task Investment Fraud Ring", 0.95, ["upi_fee_demand"]),
            ("domain", "apex-global-careers.info", "Lookalike Infrastructure", 0.96, ["spoofed_domain", "phishing"]),
            ("email", "apexlogistics.hiring@gmail.com", "Free Webmail Impersonator", 0.92, ["free_email", "fake_recruiter"])
        ]

        for i_type, val, actor, conf, tags in seed_data:
            ind_id = f"IOC-{hash(val) % 100000:05d}"
            self._indicators[val.lower()] = ThreatIndicator(
                indicator_id=ind_id,
                indicator_type=i_type,
                value=val.lower(),
                threat_actor=actor,
                confidence_score=conf,
                tags=tags
            )

    def lookup(self, query: str) -> Optional[ThreatIndicator]:
        query_clean = query.strip().lower()
        # Direct match
        if query_clean in self._indicators:
            return self._indicators[query_clean]
        
        # Substring / partial lookup
        for key, ind in self._indicators.items():
            if query_clean in key or key in query_clean:
                return ind
        return None

    def add_indicator(self, indicator: ThreatIndicator) -> None:
        self._indicators[indicator.value.lower()] = indicator
