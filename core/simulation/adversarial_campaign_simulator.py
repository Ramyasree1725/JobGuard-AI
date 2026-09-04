"""
JobGuard Core Simulation - Adversarial Recruitment Campaign Simulator
Implements multi-agent Monte Carlo simulation of threat actor campaigns,
victim vulnerability distributions, interception economics, and defense ROI.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import math


class CandidateVulnerabilityTier(Enum):
    HIGHLY_EXPERIENCED = "HIGHLY_EXPERIENCED"  # 5% scam susceptibility
    MODERATELY_INFORMED = "MODERATELY_INFORMED"  # 25% scam susceptibility
    FIRST_TIME_JOB_SEEKER = "FIRST_TIME_JOB_SEEKER"  # 65% scam susceptibility
    URGENT_DISTRESSED = "URGENT_DISTRESSED"  # 85% scam susceptibility


class ThreatActorProfile(Enum):
    OPPORTUNISTIC_SOLO = "OPPORTUNISTIC_SOLO"
    ORGANIZED_SYNDICATE = "ORGANIZED_SYNDICATE"
    STATE_SPONSORED_APT = "STATE_SPONSORED_APT"
    AUTOMATED_BOTNET = "AUTOMATED_BOTNET"


@dataclass
class SimulatedCandidate:
    candidate_id: str
    tier: CandidateVulnerabilityTier
    urgency_factor: float  # 0.0 to 1.0
    awareness_score: float  # 0.0 to 1.0
    savings_usd: float
    has_jobguard_protection: bool
    status: str = "SEARCHING"  # SEARCHING, TARGETED, DEFENDED, COMPROMISED
    financial_loss: float = 0.0


@dataclass
class CampaignRunSummary:
    total_candidates_targeted: int
    total_compromised: int
    total_defended_by_jobguard: int
    total_financial_loss_usd: float
    prevented_loss_usd: float
    interception_rate: float
    attacker_roi_ratio: float
    vulnerability_breakdown: Dict[str, int]
    timeline_events: List[Dict[str, Any]]


class AdversarialCampaignSimulator:
    """Monte Carlo engine for evaluating recruitment fraud campaign dynamics."""

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)

    def generate_candidate_population(self, size: int, protection_coverage_pct: float = 0.5) -> List[SimulatedCandidate]:
        """Generates a synthetic labor cohort with varying demographics and awareness."""
        candidates = []
        for i in range(size):
            r = random.random()
            if r < 0.20:
                tier = CandidateVulnerabilityTier.HIGHLY_EXPERIENCED
                urgency = random.uniform(0.1, 0.4)
                awareness = random.uniform(0.75, 0.98)
                savings = random.uniform(5000, 35000)
            elif r < 0.55:
                tier = CandidateVulnerabilityTier.MODERATELY_INFORMED
                urgency = random.uniform(0.3, 0.7)
                awareness = random.uniform(0.45, 0.75)
                savings = random.uniform(2000, 15000)
            elif r < 0.85:
                tier = CandidateVulnerabilityTier.FIRST_TIME_JOB_SEEKER
                urgency = random.uniform(0.5, 0.85)
                awareness = random.uniform(0.15, 0.45)
                savings = random.uniform(500, 5000)
            else:
                tier = CandidateVulnerabilityTier.URGENT_DISTRESSED
                urgency = random.uniform(0.8, 1.0)
                awareness = random.uniform(0.05, 0.25)
                savings = random.uniform(100, 2000)

            is_protected = random.random() < protection_coverage_pct

            candidates.append(SimulatedCandidate(
                candidate_id=f"CAND_{i:06d}",
                tier=tier,
                urgency_factor=urgency,
                awareness_score=awareness,
                savings_usd=savings,
                has_jobguard_protection=is_protected
            ))
        return candidates

    def run_campaign_simulation(
        self,
        population_size: int = 1000,
        attacker_type: ThreatActorProfile = ThreatActorProfile.ORGANIZED_SYNDICATE,
        protection_coverage_pct: float = 0.5,
        campaign_duration_days: int = 30,
        avg_target_demand_usd: float = 2500.0,
        jobguard_detection_accuracy: float = 0.965
    ) -> CampaignRunSummary:
        """Executes a multi-day stochastic discrete event simulation of an adversarial fraud campaign."""
        candidates = self.generate_candidate_population(population_size, protection_coverage_pct)
        
        # Setup attacker parameters
        if attacker_type == ThreatActorProfile.OPPORTUNISTIC_SOLO:
            daily_reach = 25
            sophistication = 0.35
            campaign_cost_usd = 200.0
        elif attacker_type == ThreatActorProfile.ORGANIZED_SYNDICATE:
            daily_reach = 150
            sophistication = 0.78
            campaign_cost_usd = 2500.0
        elif attacker_type == ThreatActorProfile.STATE_SPONSORED_APT:
            daily_reach = 400
            sophistication = 0.95
            campaign_cost_usd = 15000.0
        else:  # AUTOMATED_BOTNET
            daily_reach = 800
            sophistication = 0.50
            campaign_cost_usd = 800.0

        total_targeted = 0
        total_compromised = 0
        total_defended = 0
        total_financial_loss = 0.0
        prevented_loss = 0.0
        vulnerability_counts: Dict[str, int] = {t.value: 0 for t in CandidateVulnerabilityTier}
        timeline: List[Dict[str, Any]] = []

        targeted_pool = list(candidates)
        random.shuffle(targeted_pool)

        day = 1
        index = 0

        while day <= campaign_duration_days and index < len(targeted_pool):
            daily_targets = min(daily_reach, len(targeted_pool) - index)
            daily_loss = 0.0
            daily_prevented = 0.0
            daily_compromises = 0

            for _ in range(daily_targets):
                candidate = targeted_pool[index]
                index += 1
                total_targeted += 1
                candidate.status = "TARGETED"

                # Probability calculation
                susceptibility_map = {
                    CandidateVulnerabilityTier.HIGHLY_EXPERIENCED: 0.05,
                    CandidateVulnerabilityTier.MODERATELY_INFORMED: 0.25,
                    CandidateVulnerabilityTier.FIRST_TIME_JOB_SEEKER: 0.65,
                    CandidateVulnerabilityTier.URGENT_DISTRESSED: 0.85
                }
                base_p = susceptibility_map[candidate.tier]
                
                # Modulated by urgency, awareness, and attacker sophistication
                effective_p = base_p * (1.0 + 0.3 * candidate.urgency_factor - 0.5 * candidate.awareness_score) * sophistication
                effective_p = max(0.01, min(0.99, effective_p))

                # Check defense intervention
                if candidate.has_jobguard_protection:
                    if random.random() < jobguard_detection_accuracy:
                        # Defended
                        candidate.status = "DEFENDED"
                        total_defended += 1
                        loss_amount = min(candidate.savings_usd, avg_target_demand_usd * random.uniform(0.8, 1.2))
                        prevented_loss += loss_amount
                        daily_prevented += loss_amount
                        continue

                # Victim evaluation
                if random.random() < effective_p:
                    candidate.status = "COMPROMISED"
                    loss_amount = min(candidate.savings_usd, avg_target_demand_usd * random.uniform(0.8, 1.2))
                    candidate.financial_loss = loss_amount
                    total_compromised += 1
                    daily_compromises += 1
                    total_financial_loss += loss_amount
                    daily_loss += loss_amount
                    vulnerability_counts[candidate.tier.value] += 1
                else:
                    candidate.status = "DEFENDED"

            timeline.append({
                "day": day,
                "daily_targets": daily_targets,
                "daily_compromises": daily_compromises,
                "daily_loss_usd": daily_loss,
                "daily_prevented_usd": daily_prevented
            })

            day += 1

        interception_rate = (total_defended / max(1, total_targeted)) * 100.0
        attacker_roi = (total_financial_loss - campaign_cost_usd) / max(1.0, campaign_cost_usd)

        return CampaignRunSummary(
            total_candidates_targeted=total_targeted,
            total_compromised=total_compromised,
            total_defended_by_jobguard=total_defended,
            total_financial_loss_usd=total_financial_loss,
            prevented_loss_usd=prevented_loss,
            interception_rate=interception_rate,
            attacker_roi_ratio=attacker_roi,
            vulnerability_breakdown=vulnerability_counts,
            timeline_events=timeline
        )
