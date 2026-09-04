"""
JobGuard Backend Service - Cross-Platform Threat Correlation Engine
Correlates disparate threat signals across LinkedIn messages, Telegram recruiter handles,
WhatsApp onboarding groups, phishing emails, and fake ATS interview forms into unified dossiers.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import hashlib
import time


@dataclass
class ThreatSignal:
    signal_id: str
    channel: str  # 'EMAIL', 'LINKEDIN', 'TELEGRAM', 'WHATSAPP', 'ATS_FORM', 'SMS'
    source_identifier: str  # e.g., email address, handle, URL
    raw_content: str
    extracted_entities: List[str]  # company names, recruiter names, crypto wallets, phone numbers
    timestamp: float
    confidence: float


@dataclass
class CorrelatedCampaignProfile:
    campaign_id: str
    impersonated_brand: str
    primary_channels: List[str]
    associated_handles: List[str]
    associated_emails: List[str]
    associated_domains: List[str]
    total_signals_correlated: int
    threat_severity: str
    campaign_lifecycle_status: str  # 'ACTIVE_OUTBREAK', 'MITIGATED', 'DORMANT'
    timeline_summary: str


class CrossPlatformThreatCorrelator:
    """Aggregates and joins multi-channel threat indicators into coherent attack campaign graphs."""

    def __init__(self):
        self.signal_pool: List[ThreatSignal] = []
        self.campaigns: Dict[str, CorrelatedCampaignProfile] = {}

    def ingest_signal(self, signal: ThreatSignal) -> None:
        """Ingests a multi-channel threat signal."""
        self.signal_pool.append(signal)

    def correlate_signals(self) -> List[CorrelatedCampaignProfile]:
        """Correlates all ingested signals into campaign profiles by shared entities."""
        # Index by brand / company
        brand_groups = collections.defaultdict(list) if 'collections' in globals() else {}
        for s in self.signal_pool:
            for ent in s.extracted_entities:
                if ent.isupper() or len(ent) > 3:
                    brand_groups.setdefault(ent.lower(), []).append(s)

        correlated_campaigns: List[CorrelatedCampaignProfile] = []

        for brand, signals in brand_groups.items():
            if len(signals) < 1:
                continue

            channels = list(set(s.channel for s in signals))
            handles = list(set(s.source_identifier for s in signals if s.channel in ("TELEGRAM", "WHATSAPP")))
            emails = list(set(s.source_identifier for s in signals if s.channel == "EMAIL"))
            domains = list(set(s.source_identifier for s in signals if s.channel == "ATS_FORM"))

            campaign_id = f"CMP-{hashlib.md5(brand.encode()).hexdigest()[:8].upper()}"
            
            # Severity evaluation
            sev = "CRITICAL" if len(channels) >= 2 or len(signals) >= 3 else "HIGH"

            profile = CorrelatedCampaignProfile(
                campaign_id=campaign_id,
                impersonated_brand=brand.title(),
                primary_channels=channels,
                associated_handles=handles,
                associated_emails=emails,
                associated_domains=domains,
                total_signals_correlated=len(signals),
                threat_severity=sev,
                campaign_lifecycle_status="ACTIVE_OUTBREAK",
                timeline_summary=f"Correlated {len(signals)} multi-vector signals spanning {', '.join(channels)}."
            )
            correlated_campaigns.append(profile)
            self.campaigns[campaign_id] = profile

        return correlated_campaigns
