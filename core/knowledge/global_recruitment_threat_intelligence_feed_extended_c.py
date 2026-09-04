"""
JobGuard Core Knowledge - Global Recruitment Threat Intelligence Feed Extended Volume C
Maintains active Indicators of Compromise (IoCs) across maritime, logistics, construction,
and global retail recruiter impersonations, phishing domains, and fake ATS endpoints.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ThreatFeedCategoryC(Enum):
    MARITIME_OFFSHORE_FRAUD = "MARITIME_OFFSHORE_FRAUD"
    LOGISTICS_SUPPLY_CHAIN_LURE = "LOGISTICS_SUPPLY_CHAIN_LURE"
    RETAIL_E_COMMERCE_CLONE = "RETAIL_E_COMMERCE_CLONE"
    CONSTRUCTION_CONTRACT_SCAM = "CONSTRUCTION_CONTRACT_SCAM"


@dataclass
class ThreatIntelRecordC:
    ioc_id: str
    category: ThreatFeedCategoryC
    indicator_value: str
    targeted_corporation: str
    threat_actor_group: str
    confidence_score: float
    first_seen_timestamp: str
    severity_level: str
    mitigation_guidance: str
    detailed_technical_notes: str


class GlobalRecruitmentThreatIntelligenceFeedExtendedC:
    """Master threat intelligence feed volume C for industrial recruitment fraud IoCs."""

    def __init__(self):
        self.feed_database: Dict[str, ThreatIntelRecordC] = {}
        self._seed_threat_feed_c()

    def _seed_threat_feed_c(self) -> None:
        """Populate extensive IoC threat catalog volume C."""

        records_data = [
            (
                "IOC-C-001",
                ThreatFeedCategoryC.MARITIME_OFFSHORE_FRAUD,
                "offshore-drilling-careers-portal.org",
                "Global Offshore Energy",
                "Apex Syndicate",
                0.99,
                "2026-01-16",
                "CRITICAL",
                "Warn maritime job applicants against advance medical and visa fees. Block domain.",
                "Issues forged employment contracts demanding $3,200 for mandatory STCW and maritime visa clearances."
            ),
            (
                "IOC-C-002",
                ThreatFeedCategoryC.LOGISTICS_SUPPLY_CHAIN_LURE,
                "fedex-freight-careers-direct.net",
                "FedEx Corporation",
                "Syndicate-MuleOps",
                0.98,
                "2026-01-21",
                "CRITICAL",
                "Block domain and alert postal inspectors regarding fake remote package inspector listings.",
                "Recruits victims as unwitting reshipping mules for merchandise purchased with stolen credit cards."
            ),
            (
                "IOC-C-003",
                ThreatFeedCategoryC.RETAIL_E_COMMERCE_CLONE,
                "walmart-remote-talent-desk.info",
                "Walmart Inc",
                "Syndicate-RetailPhish",
                0.97,
                "2026-01-26",
                "CRITICAL",
                "Issue takedown request and flag lookalike domain across search engine anti-phishing feeds.",
                "Offers fictitious customer service chat positions with counterfeit equipment check kickback traps."
            ),
            (
                "IOC-C-004",
                ThreatFeedCategoryC.CONSTRUCTION_CONTRACT_SCAM,
                "bechtel-overseas-recruiting.online",
                "Bechtel Corporation",
                "Apex Syndicate",
                0.99,
                "2026-02-03",
                "CRITICAL",
                "Alert international engineering job boards. Blacklist associated nameserver IP range.",
                "Targets engineers with forged overseas appointment letters demanding upfront embassy document processing fees."
            )
        ]

        for ioc_id, cat, val, corp, actor, conf, ts, sev, mit, notes in records_data:
            self.feed_database[val.lower()] = ThreatIntelRecordC(
                ioc_id=ioc_id,
                category=cat,
                indicator_value=val,
                targeted_corporation=corp,
                threat_actor_group=actor,
                confidence_score=float(conf),
                first_seen_timestamp=ts,
                severity_level=sev,
                mitigation_guidance=mit,
                detailed_technical_notes=notes
            )

    def query_threat_feed(self, indicator: str) -> Optional[ThreatIntelRecordC]:
        clean = indicator.lower().strip()
        if "@" in clean and not clean.startswith("@"):
            clean = clean.split("@")[-1]
        return self.feed_database.get(clean)
