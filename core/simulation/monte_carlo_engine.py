"""
JobGuard Core Simulation - Monte Carlo Risk Probability Engine
Runs simulated stochastic career trajectories, scam loss probabilities,
and financial fraud exposure distributions across thousands of candidate scenarios.
"""

import math
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class MonteCarloSimulationResult:
    iterations_run: int
    mean_financial_loss: float
    p95_value_at_risk: float
    scam_probability_pct: float
    loss_distribution_histogram: Dict[str, int]


class MonteCarloRiskEngine:
    """Monte Carlo simulator for candidate scam risk profiling."""

    def __init__(self, iterations: int = 10000):
        self.iterations = max(100, iterations)

    def simulate_exposure(
        self,
        base_scam_score: float,
        offered_monthly_salary: float,
        upfront_fee_asked: float = 0.0
    ) -> MonteCarloSimulationResult:
        """Simulate financial risk across thousands of stochastic market iterations."""
        losses: List[float] = []
        scam_hits = 0

        prob_scam = min(0.99, max(0.01, base_scam_score / 100.0))

        for _ in range(self.iterations):
            # Stochastic Bernoulli trial for fraud encounter
            is_scam = random.random() < prob_scam
            if is_scam:
                scam_hits += 1
                # Loss includes upfront fee + lost opportunity wage + fake check bounce penalties
                direct_loss = upfront_fee_asked
                indirect_loss = random.uniform(200.0, 1500.0) if upfront_fee_asked > 0 else random.uniform(500.0, 4500.0)
                losses.append(direct_loss + indirect_loss)
            else:
                losses.append(0.0)

        losses.sort()
        mean_loss = sum(losses) / len(losses)
        p95_index = int(0.95 * len(losses))
        p95_var = losses[p95_index]

        # Histogram bins
        histogram = {
            "0 (Zero Loss)": sum(1 for l in losses if l == 0),
            "1 - 1,000": sum(1 for l in losses if 0 < l <= 1000),
            "1,001 - 3,000": sum(1 for l in losses if 1000 < l <= 3000),
            "3,000+": sum(1 for l in losses if l > 3000)
        }

        return MonteCarloSimulationResult(
            iterations_run=self.iterations,
            mean_financial_loss=round(mean_loss, 2),
            p95_value_at_risk=round(p95_var, 2),
            scam_probability_pct=round((scam_hits / self.iterations) * 100.0, 2),
            loss_distribution_histogram=histogram
        )
