"""
JobGuard Core Knowledge - Enterprise Recruitment Threat Intelligence Database Large
Provides extensive catalog of known cybercriminal campaign clusters, malicious ATS clone architectures,
lookalike domain generation algorithms, and verified corporate threat intelligence feeds.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ThreatInfrastructureType(Enum):
    PHISHING_PORTAL = "PHISHING_PORTAL"
    FAKE_ATS_SYSTEM = "FAKE_ATS_SYSTEM"
    TELEGRAM_BOTNET = "TELEGRAM_BOTNET"
    CHECK_KICKBACK_VENDOR = "CHECK_KICKBACK_VENDOR"
    CRYPTO_DRAINER_WALLET = "CRYPTO_DRAINER_WALLET"
    MALICIOUS_NPM_PACKAGE = "MALICIOUS_NPM_PACKAGE"


@dataclass
class ThreatActorProfileExpanded:
    actor_id: str
    actor_alias: str
    origin_country: str
    active_since_year: int
    infrastructure_types: List[ThreatInfrastructureType]
    targeted_industry_verticals: List[str]
    estimated_victim_count: int
    financial_impact_estimate_usd: float
    signature_tactics: List[str]
    known_associated_domains: List[str]
    is_active: bool = True


class EnterpriseRecruitmentThreatIntelligenceDatabaseLarge:
    """Master expanded repository of advanced persistent recruitment threat actors."""

    def __init__(self):
        self.actors: Dict[str, ThreatActorProfileExpanded] = {}
        self._initialize_large_threat_database()

    def _initialize_large_threat_database(self) -> None:
        """Register comprehensive threat actor intelligence profiles."""

        actors_list = [
            ThreatActorProfileExpanded(
                actor_id="ACT-001",
                actor_alias="SilverPhish Recruitment Syndicate",
                origin_country="NG",
                active_since_year=2022,
                infrastructure_types=[ThreatInfrastructureType.PHISHING_PORTAL, ThreatInfrastructureType.CHECK_KICKBACK_VENDOR],
                targeted_industry_verticals=["Technology", "Healthcare", "Financial Services", "Retail"],
                estimated_victim_count=4500,
                financial_impact_estimate_usd=12500000.0,
                signature_tactics=[
                    "Mailing counterfeit cashier checks for home office equipment",
                    "Directing victims to fake IT vendor shell portals",
                    "Conducting initial screening via spoofed LinkedIn recruiter profiles"
                ],
                known_associated_domains=[
                    "google-remote-careers.com", "microsoft-talent-portal.org", "apple-advisors-remote.net",
                    "certified-it-workstation-vendors.com", "global-office-supplies-direct.org"
                ]
            ),
            ThreatActorProfileExpanded(
                actor_id="ACT-002",
                actor_alias="CryptoTask Matrix Group",
                origin_country="KH",
                active_since_year=2023,
                infrastructure_types=[ThreatInfrastructureType.CRYPTO_DRAINER_WALLET, ThreatInfrastructureType.TELEGRAM_BOTNET],
                targeted_industry_verticals=["Digital Marketing", "E-Commerce", "Hospitality"],
                estimated_victim_count=12000,
                financial_impact_estimate_usd=38000000.0,
                signature_tactics=[
                    "Advertising $300-$800/day for liking videos or rating hotel reservations",
                    "Demanding cryptocurrency (USDT) deposits to reset negative balances",
                    "Operating tiered VIP commission schemes with automated Telegram channel bots"
                ],
                known_associated_domains=[
                    "opt-media-vip.top", "smart-rating-vip.club", "hotel-booking-optimizer.vip",
                    "data-annotation-earn.site", "app-review-boost.online"
                ]
            ),
            ThreatActorProfileExpanded(
                actor_id="ACT-003",
                actor_alias="Lazarus Recruitment Lure Unit",
                origin_country="KP",
                active_since_year=2020,
                infrastructure_types=[ThreatInfrastructureType.MALICIOUS_NPM_PACKAGE, ThreatInfrastructureType.FAKE_ATS_SYSTEM],
                targeted_industry_verticals=["Cryptocurrency Exchanges", "Defi Protocols", "Aerospace & Defense"],
                estimated_victim_count=350,
                financial_impact_estimate_usd=85000000.0,
                signature_tactics=[
                    "Posing as top tier executive recruiters on LinkedIn",
                    "Delivering malicious coding assessments via Git repositories with pre-install script trojans",
                    "Exfiltrating developer cryptocurrency private keys and SSH credentials"
                ],
                known_associated_domains=[
                    "blockchain-careers-talent.com", "crypto-recruiting-network.io", "defi-tech-interviews.net"
                ]
            ),
            ThreatActorProfileExpanded(
                actor_id="ACT-004",
                actor_alias="Apex Advance-Fee Consortium",
                origin_country="GH",
                active_since_year=2021,
                infrastructure_types=[ThreatInfrastructureType.PHISHING_PORTAL],
                targeted_industry_verticals=["Oil & Gas", "Maritime Logistics", "Construction"],
                estimated_victim_count=2800,
                financial_impact_estimate_usd=6200000.0,
                signature_tactics=[
                    "Issuing fake high-paying overseas employment appointment letters",
                    "Demanding advance visa processing, medical clearance, and immigration fees",
                    "Using forged embassy stamps and notary seals"
                ],
                known_associated_domains=[
                    "offshore-energy-recruitment.org", "maritime-global-careers.net", "gulf-construction-hr.com"
                ]
            )
        ]

        for actor in actors_list:
            self.actors[actor.actor_id] = actor

    def get_actor_by_domain(self, domain: str) -> Optional[ThreatActorProfileExpanded]:
        """Finds if a domain is associated with known advanced threat actor groups."""
        dom_clean = domain.lower().strip()
        for actor in self.actors.values():
            if any(dom_clean == d.lower() or dom_clean.endswith("." + d.lower()) for d in actor.known_associated_domains):
                return actor
        return None
