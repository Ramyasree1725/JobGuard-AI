"""
JobGuard Core Simulation - Agent-Based Recruitment Economy (ABM)
Simulates multi-agent market dynamics: Candidates, Legitimate Employers, Fraud Syndicates,
and Law Enforcement interventions to model ecosystem equilibrium.
"""

import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class CandidateAgent:
    id: str
    risk_tolerance: float  # [0, 1]
    capital: float = 1000.0
    is_employed: bool = False
    scammed_count: int = 0


@dataclass
class SyndicateAgent:
    id: str
    fee_demand: float = 300.0
    deception_quality: float = 0.5  # [0, 1]
    revenue: float = 0.0
    is_busted: bool = False


class RecruitmentMarketSimulator:
    """Multi-agent simulator for studying fraud containment policies."""

    def __init__(self, num_candidates: int = 100, num_syndicates: int = 5, enforcement_budget: float = 50.0):
        self.candidates = [CandidateAgent(id=f"C_{i}", risk_tolerance=random.uniform(0.1, 0.9)) for i in range(num_candidates)]
        self.syndicates = [SyndicateAgent(id=f"S_{j}", deception_quality=random.uniform(0.2, 0.8)) for j in range(num_syndicates)]
        self.enforcement_budget = enforcement_budget
        self.history: List[Dict[str, float]] = []

    def step(self) -> Dict[str, float]:
        """Execute one market trading cycle."""
        active_syndicates = [s for s in self.syndicates if not s.is_busted]
        total_scams_committed = 0

        for cand in self.candidates:
            if not cand.is_employed and active_syndicates:
                # Candidate encounters random job posting
                syndicate = random.choice(active_syndicates)
                
                # Candidate decision: risk_tolerance vs perceived deception
                if cand.risk_tolerance > (1.0 - syndicate.deception_quality):
                    # Candidate falls for scam
                    cand.capital -= syndicate.fee_demand
                    cand.scammed_count += 1
                    syndicate.revenue += syndicate.fee_demand
                    total_scams_committed += 1

        # Enforcement action: probability of busting syndicate scales with revenue and enforcement budget
        for syndicate in active_syndicates:
            bust_prob = min(0.9, (syndicate.revenue * 0.001) + (self.enforcement_budget * 0.005))
            if random.random() < bust_prob:
                syndicate.is_busted = True

        stats = {
            "active_syndicates": len([s for s in self.syndicates if not s.is_busted]),
            "scams_this_step": total_scams_committed,
            "avg_candidate_capital": round(sum(c.capital for c in self.candidates) / len(self.candidates), 2)
        }
        self.history.append(stats)
        return stats
