"""
JobGuard Core Recommendation - Multi-Criteria Career Matching & Salary Benchmarking
Evaluates candidate skill vectors against genuine employer requisitions,
calculates compensation market deviations, and computes fair market wage distributions.
"""

import math
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class JobRequisition:
    job_id: str
    title: str
    company: str
    required_skills: List[str]
    min_years_experience: int
    salary_range_usd: Tuple[float, float]
    verified_employer: bool = True


@dataclass
class CandidateProfile:
    candidate_id: str
    skills: List[str]
    years_experience: int
    desired_salary_usd: float
    preferred_locations: List[str]


class EnterpriseMatchingEngine:
    """Matches verified candidates to vetted corporate career requisitions."""

    # Standard industry benchmarks (Title -> (P25, P50, P75, P90) in USD)
    SALARY_BENCHMARKS_USD: Dict[str, Tuple[float, float, float, float]] = {
        "software engineer": (85000.0, 115000.0, 145000.0, 180000.0),
        "senior software engineer": (125000.0, 155000.0, 190000.0, 230000.0),
        "data scientist": (90000.0, 120000.0, 150000.0, 185000.0),
        "product manager": (95000.0, 130000.0, 165000.0, 200000.0),
        "data entry assistant": (32000.0, 42000.0, 52000.0, 60000.0),
        "customer support specialist": (35000.0, 45000.0, 55000.0, 65000.0)
    }

    def __init__(self):
        self.requisitions: Dict[str, JobRequisition] = {}

    def add_requisition(self, req: JobRequisition) -> None:
        self.requisitions[req.job_id] = req

    def evaluate_salary_realism(self, job_title: str, offered_salary_usd: float) -> Tuple[bool, float, str]:
        """Examines offered salary against national percentiles to flag predatory over-promising."""
        clean_title = job_title.strip().lower()
        matched_benchmark = None

        for title_key, benchmark in self.SALARY_BENCHMARKS_USD.items():
            if title_key in clean_title:
                matched_benchmark = benchmark
                break

        if not matched_benchmark:
            return True, 0.0, "Standard market rate (no distortion detected)"

        p25, p50, p75, p90 = matched_benchmark

        # Check for absurdly high salary for low-skill role (classic scam bait)
        if "data entry" in clean_title or "typing" in clean_title or "assistant" in clean_title:
            if offered_salary_usd > p90 * 1.8:
                distortion_ratio = offered_salary_usd / p50
                return False, 85.0, f"Critical salary distortion ({distortion_ratio:.1f}x higher than national median ${p50:,.0f}). Unrealistic compensation bait."

        if offered_salary_usd < p25 * 0.4:
            return False, 40.0, f"Sub-minimum compensation significantly below standard 25th percentile (${p25:,.0f})."

        return True, 0.0, "Compensation aligns with verified corporate market ranges."

    def match_candidate(self, candidate: CandidateProfile) -> List[Tuple[JobRequisition, float]]:
        """Rank requisitions for candidate using skill Jaccard overlap and experience fit."""
        matches = []
        cand_skills = set(s.lower() for s in candidate.skills)

        for req in self.requisitions.values():
            if not req.verified_employer:
                continue

            req_skills = set(s.lower() for s in req.required_skills)
            overlap = len(cand_skills.intersection(req_skills))
            skill_score = overlap / max(1, len(req_skills))

            exp_fit = 1.0 if candidate.years_experience >= req.min_years_experience else (candidate.years_experience / max(1, req.min_years_experience))

            final_score = 0.7 * skill_score + 0.3 * exp_fit
            matches.append((req, round(final_score, 4)))

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
