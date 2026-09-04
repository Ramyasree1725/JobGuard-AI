"""
JobGuard Core Simulation - Metropolitan Labor Market Recruitment Graph Simulator Expanded
Simulates candidate commuting dynamics, multi-employer wage competition,
and geographic fraud campaign clustering across major metropolitan statistical areas (MSAs).
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


@dataclass
class MetroWorkerAgent:
    agent_id: str
    home_zone_id: str
    target_occupation_soc: str
    reservation_wage_hourly: float
    is_actively_interviewing: bool
    current_fraud_exposure_level: float = 0.0


@dataclass
class MetroEmployerNode:
    employer_id: str
    business_zone_id: str
    claimed_brand: str
    posted_wage_hourly: float
    is_authentic_enterprise: bool
    active_job_openings: int


class CityRecruitmentGraphSimExpanded:
    """Agent-based spatial economic simulation of metropolitan recruitment fraud."""

    def __init__(self, num_workers: int = 500, num_employers: int = 50):
        self.workers: List[MetroWorkerAgent] = []
        self.employers: List[MetroEmployerNode] = []
        self._initialize_metro_agents(num_workers, num_employers)

    def _initialize_metro_agents(self, num_w: int, num_e: int) -> None:
        """Seeds synthetic labor market participants."""
        zones = ["ZONE_DOWNTOWN", "ZONE_SUBURB_NORTH", "ZONE_SUBURB_EAST", "ZONE_METRO_WEST"]

        for i in range(num_w):
            self.workers.append(MetroWorkerAgent(
                agent_id=f"WRK-{i:05d}",
                home_zone_id=random.choice(zones),
                target_occupation_soc="43-9021",  # Data Entry / Administrative
                reservation_wage_hourly=random.uniform(16.0, 24.0),
                is_actively_interviewing=True
            ))

        for j in range(num_e):
            is_scam = (random.random() < 0.20)
            self.employers.append(MetroEmployerNode(
                employer_id=f"EMP-{j:04d}",
                business_zone_id=random.choice(zones),
                claimed_brand="TechCorp Global" if not is_scam else "Global Career Hub Direct",
                posted_wage_hourly=random.uniform(18.0, 28.0) if not is_scam else random.uniform(45.0, 75.0),
                is_authentic_enterprise=not is_scam,
                active_job_openings=random.randint(2, 10)
            ))

    def step_market_round(self) -> Dict[str, Any]:
        """Executes one round of job applications, wage offers, and scam interceptions."""
        total_applications = 0
        scam_applications = 0
        defended_by_jobguard = 0

        for worker in self.workers:
            if not worker.is_actively_interviewing:
                continue

            # Candidate considers random sample of employers
            candidates = random.sample(self.employers, min(5, len(self.employers)))
            best_offer = max(candidates, key=lambda e: e.posted_wage_hourly)

            total_applications += 1
            if not best_offer.is_authentic_enterprise:
                scam_applications += 1
                worker.current_fraud_exposure_level += 0.25
                # JobGuard defense rate (96%)
                if random.random() < 0.96:
                    defended_by_jobguard += 1

        return {
            "total_applications": total_applications,
            "scam_applications": scam_applications,
            "defended_by_jobguard": defended_by_jobguard,
            "effective_interception_pct": (defended_by_jobguard / max(1, scam_applications)) * 100.0
        }
