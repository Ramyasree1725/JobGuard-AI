"""
JobGuard Core Simulation - Diamond-Mortensen-Pissarides (DMP) Equilibrium Labor Market
Simulates stochastic job destruction, Cobb-Douglas matching functions,
Nash wage bargaining, and equilibrium Beveridge curve shifts.
"""

import math
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class JobVacancy:
    vacancy_id: str
    productivity: float
    is_filled: bool = False
    wage: float = 0.0


@dataclass
class Worker:
    worker_id: str
    reservation_wage: float
    is_employed: bool = False
    employed_vacancy_id: Optional[str] = None


class DMPSearchMatchingSimulator:
    """Diamond-Mortensen-Pissarides Search and Matching model simulator."""

    def __init__(
        self,
        num_workers: int = 500,
        num_vacancies: int = 200,
        matching_efficiency_gamma: float = 0.6,
        elasticity_alpha: float = 0.5,
        job_separation_rate_s: float = 0.05,
        worker_bargaining_power_beta: float = 0.5
    ):
        self.workers = [Worker(f"W_{i}", reservation_wage=random.uniform(20.0, 40.0)) for i in range(num_workers)]
        self.vacancies = [JobVacancy(f"V_{j}", productivity=random.uniform(50.0, 100.0)) for j in range(num_vacancies)]
        self.gamma = matching_efficiency_gamma
        self.alpha = elasticity_alpha
        self.s = job_separation_rate_s
        self.beta = worker_bargaining_power_beta
        self.history: List[Dict[str, float]] = []

    def step(self) -> Dict[str, float]:
        """Advance matching cycle by 1 period."""
        # 1. Exogenous job destruction
        for w in self.workers:
            if w.is_employed and random.random() < self.s:
                w.is_employed = False
                # Free vacancy
                for v in self.vacancies:
                    if v.vacancy_id == w.employed_vacancy_id:
                        v.is_filled = False
                        v.wage = 0.0
                w.employed_vacancy_id = None

        unemployed = [w for w in self.workers if not w.is_employed]
        open_vacancies = [v for v in self.vacancies if not v.is_filled]

        u = len(unemployed)
        v_count = len(open_vacancies)

        # 2. Cobb-Douglas matching function: M = gamma * u^alpha * v^(1-alpha)
        if u > 0 and v_count > 0:
            m_total = int(self.gamma * (u ** self.alpha) * (v_count ** (1.0 - self.alpha)))
            num_matches = min(m_total, u, v_count)

            matched_workers = random.sample(unemployed, num_matches)
            matched_vacancies = random.sample(open_vacancies, num_matches)

            # 3. Nash wage bargaining: w = beta * p + (1 - beta) * b
            for w_cand, v_cand in zip(matched_workers, matched_vacancies):
                wage = self.beta * v_cand.productivity + (1.0 - self.beta) * w_cand.reservation_wage
                if wage >= w_cand.reservation_wage and wage <= v_cand.productivity:
                    w_cand.is_employed = True
                    w_cand.employed_vacancy_id = v_cand.vacancy_id
                    v_cand.is_filled = True
                    v_cand.wage = wage

        total_employed = sum(1 for w in self.workers if w.is_employed)
        unemployment_rate = (len(self.workers) - total_employed) / len(self.workers)

        stats = {
            "unemployment_rate": round(unemployment_rate, 4),
            "open_vacancies": len([v for v in self.vacancies if not v.is_filled]),
            "total_employed": total_employed,
            "labor_market_tightness_theta": round(v_count / max(1, u), 3)
        }
        self.history.append(stats)
        return stats
