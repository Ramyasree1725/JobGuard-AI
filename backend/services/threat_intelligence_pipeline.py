"""
JobGuard Backend Service - Threat Intelligence Ingestion & IOC Normalization Pipeline
Ingests threat indicators from STIX/TAXII feeds, normalizes UPI handles,
and updates the distributed consistent hash ring cache.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from backend.services.threat_intel import ThreatIntelligenceFeed, ThreatIndicator


class ThreatIntelligencePipeline:
    """Batch ingestion and IOC normalization engine."""

    def __init__(self):
        self.feed = ThreatIntelligenceFeed()

    def ingest_indicators(self, raw_indicators: List[Dict[str, Any]]) -> int:
        count = 0
        for item in raw_indicators:
            val = item.get("value", "").strip()
            if not val:
                continue

            ind = ThreatIndicator(
                indicator_id=f"IOC-FEED-{count:04d}",
                indicator_type=item.get("type", "unknown"),
                value=val,
                threat_actor=item.get("actor", "Unattributed Syndicate"),
                confidence_score=float(item.get("confidence", 0.9)),
                tags=item.get("tags", [])
            )
            self.feed.add_indicator(ind)
            count += 1

        return count
