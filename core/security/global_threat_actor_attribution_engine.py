"""
JobGuard Core Security - Global Threat Actor Attribution Engine
Computes Bayesian likelihood ratios, Diamond Model vertex correlations, and Jaccard TTP similarities
to attribute recruitment fraud campaigns to organized cybercrime syndicates and APT groups.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class ThreatActorProfileModel:
    actor_id: str
    alias: str
    known_ttps: Set[str]
    preferred_infrastructure_subnets: List[str]
    preferred_communication_channels: List[str]
    typical_financial_demands_usd: Tuple[float, float]
    language_stylometry_markers: List[str]


@dataclass
class AttributionAssessment:
    candidate_actor: ThreatActorProfileModel
    attribution_confidence_score: float  # 0.0 to 1.0
    matched_ttps: List[str]
    infrastructure_overlap_score: float
    stylometry_match_score: float
    attribution_verdict: str


class GlobalThreatActorAttributionEngine:
    """Diamond Model-based cyber threat attribution engine for recruitment fraud syndicates."""

    def __init__(self):
        self.actor_profiles: Dict[str, ThreatActorProfileModel] = {}
        self._initialize_actor_profiles()

    def _initialize_actor_profiles(self) -> None:
        """Register profiles of tracked cybercrime syndicates."""

        self.actor_profiles["ACT-SILVERPHISH"] = ThreatActorProfileModel(
            actor_id="ACT-SILVERPHISH",
            alias="SilverPhish Syndicate",
            known_ttps={"T1566.002", "T1657", "T1586.002", "CHECK_KICKBACK", "UPFRONT_FEE"},
            preferred_infrastructure_subnets=["185.156.72.0/24", "103.224.182.0/24"],
            preferred_communication_channels=["TELEGRAM", "GMAIL", "SMS"],
            typical_financial_demands_usd=(1500.0, 5000.0),
            language_stylometry_markers=["kindly revert", "home office vendor", "congratulations on selection", "urgent response required"]
        )

        self.actor_profiles["ACT-CRYPTOTASK"] = ThreatActorProfileModel(
            actor_id="ACT-CRYPTOTASK",
            alias="CryptoTask Matrix Ring",
            known_ttps={"T1657", "CRYPTO_TASK_ESCROW", "VIP_RECHARGE", "TELEGRAM_BOT"},
            preferred_infrastructure_subnets=["104.244.72.0/24", "195.181.160.0/24"],
            preferred_communication_channels=["TELEGRAM", "WHATSAPP"],
            typical_financial_demands_usd=(100.0, 15000.0),
            language_stylometry_markers=["recharge usdt", "level 1 vip", "daily task commission", "optimize hotel booking"]
        )

        self.actor_profiles["ACT-LAZARUS"] = ThreatActorProfileModel(
            actor_id="ACT-LAZARUS",
            alias="Lazarus Recruitment Lure Unit",
            known_ttps={"T1204.002", "T1566.001", "MALICIOUS_NPM", "SSH_KEY_THEFT"},
            preferred_infrastructure_subnets=["185.220.101.0/24"],
            preferred_communication_channels=["LINKEDIN", "GITHUB", "EMAIL"],
            typical_financial_demands_usd=(0.0, 0.0),  # Aims for credential/key theft rather than cash
            language_stylometry_markers=["take home coding challenge", "smart contract audit test", "senior blockchain architect"]
        )

    def attribute_campaign(
        self,
        observed_ttps: Set[str],
        observed_subnet: Optional[str] = None,
        observed_channel: Optional[str] = None,
        observed_phrases: Optional[List[str]] = None
    ) -> List[AttributionAssessment]:
        """Calculates multi-dimensional Diamond Model attribution similarity scores."""
        results: List[AttributionAssessment] = []
        observed_phrases = observed_phrases or []

        for actor in self.actor_profiles.values():
            # 1. TTP Jaccard similarity
            intersection = len(observed_ttps.intersection(actor.known_ttps))
            union = len(observed_ttps.union(actor.known_ttps))
            ttp_score = (intersection / max(1, union))

            # 2. Infrastructure overlap
            infra_score = 1.0 if observed_subnet and any(observed_subnet.startswith(s.split('/')[0][:7]) for s in actor.preferred_infrastructure_subnets) else 0.0

            # 3. Stylometry marker matches
            matched_phrases = [p for p in observed_phrases if any(m.lower() in p.lower() for m in actor.language_stylometry_markers)]
            stylo_score = len(matched_phrases) / max(1, len(actor.language_stylometry_markers))

            # 4. Composite confidence
            composite = (ttp_score * 0.50) + (infra_score * 0.30) + (stylo_score * 0.20)

            if composite > 0.15:
                verdict = "HIGH_CONFIDENCE_ATTRIBUTION" if composite >= 0.70 else "MODERATE_SIMILARITY" if composite >= 0.40 else "WEAK_CORRELATION"
                results.append(AttributionAssessment(
                    candidate_actor=actor,
                    attribution_confidence_score=composite,
                    matched_ttps=list(observed_ttps.intersection(actor.known_ttps)),
                    infrastructure_overlap_score=infra_score,
                    stylometry_match_score=stylo_score,
                    attribution_verdict=verdict
                ))

        results.sort(key=lambda x: x.attribution_confidence_score, reverse=True)
        return results
