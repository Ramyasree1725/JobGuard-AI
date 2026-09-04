"""
JobGuard Core Simulation - Synthetic Adversarial Fraud Generator
Generates procedurally structured synthetic job postings, recruiter pitch messages,
and offer contracts with controlled red flag injections for benchmark testing.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random


@dataclass
class SyntheticJobProfile:
    job_id: str
    target_role: str
    claimed_employer: str
    compensation_text: str
    description_body: str
    injected_red_flags: List[str]
    is_fraudulent: bool
    ground_truth_threat_level: str  # 'BENIGN', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'


class SyntheticFraudGenerator:
    """Procedural generator for generating realistic and adversarial recruitment postings."""

    COMPANIES = ["Google", "Microsoft", "Amazon", "Apple", "Netflix", "Tesla", "Deloitte", "Meta", "Adobe", "Salesforce"]
    TITLES = ["Data Entry Specialist", "Remote Administrative Assistant", "Customer Support Rep", "Software Engineer", "Marketing Associate"]
    
    BENIGN_TEMPLATES = [
        "We are seeking a qualified {title} to join our distributed team at {company}. Requirements include 2+ years experience with office suites and strong verbal communication. Candidates must apply through our official careers portal at {ats_url}.",
        "Join {company} as an entry-level {title}. This full-time position offers comprehensive healthcare benefits, 401(k) matching, and paid time off. To apply, submit your resume and cover letter via our Workday portal.",
        "Exciting opportunity for a {title} at {company}. The role involves collaborating across cross-functional teams, managing records, and preparing analytical briefs. Interviews consist of a 45-minute technical screen and a panel discussion."
    ]

    SCAM_TEMPLATES = [
        "URGENT: {company} is immediately hiring remote {title}! Pay is {pay}. No prior experience needed. Work 2-3 hours daily from home. Interview is strictly conducted via Telegram (@{telegram_handle}). We will mail you a check for ${check_amount} to purchase your home office equipment from our certified vendor.",
        "Congratulations! You have been selected for the {title} position at {company}. Salary: {pay}. Before your start date, you are required to submit an upfront registration and background processing fee of ${fee_amount} via Zelle or Bitcoin. This will be 100% reimbursed on your first paycheck.",
        "Earn up to {pay} doing simple daily product rating and task optimization for {company}! All you need is a smartphone and Telegram. Initial deposit of 100 USDT required to activate Level 1 VIP commission earnings. Daily payouts guaranteed to your crypto wallet."
    ]

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)

    def generate_batch(self, count: int = 50, scam_ratio: float = 0.5) -> List[SyntheticJobProfile]:
        """Generates a dataset of synthetic job descriptions with labelled ground truth."""
        dataset: List[SyntheticJobProfile] = []

        for i in range(count):
            is_scam = random.random() < scam_ratio
            company = random.choice(self.COMPANIES)
            title = random.choice(self.TITLES)

            if is_scam:
                template = random.choice(self.SCAM_TEMPLATES)
                pay = random.choice(["$45.00/hr", "$65.00/hr", "$350.00/day", "$4,500/week"])
                telegram = f"recruiter_{company.lower()}_{random.randint(100, 999)}"
                check_amt = random.randint(2500, 5000)
                fee_amt = random.randint(150, 450)

                body = template.format(
                    company=company,
                    title=title,
                    pay=pay,
                    telegram_handle=telegram,
                    check_amount=check_amt,
                    fee_amount=fee_amt
                )

                injected_flags = []
                if "telegram" in body.lower():
                    injected_flags.append("CHAT_ONLY_INTERVIEW")
                if "check" in body.lower():
                    injected_flags.append("COUNTERFEIT_CHECK_EQUIPMENT")
                if "fee" in body.lower() or "zelle" in body.lower():
                    injected_flags.append("UPFRONT_REGISTRATION_FEE")
                if "usdt" in body.lower() or "crypto" in body.lower():
                    injected_flags.append("CRYPTO_TASK_RATING_SCHEME")

                dataset.append(SyntheticJobProfile(
                    job_id=f"SYNTH_SCAM_{i:04d}",
                    target_role=title,
                    claimed_employer=company,
                    compensation_text=pay,
                    description_body=body,
                    injected_red_flags=injected_flags,
                    is_fraudulent=True,
                    ground_truth_threat_level="CRITICAL" if len(injected_flags) >= 2 else "HIGH"
                ))
            else:
                template = random.choice(self.BENIGN_TEMPLATES)
                ats_url = f"https://boards.greenhouse.io/{company.lower()}/jobs/{random.randint(100000, 999999)}"
                body = template.format(
                    company=company,
                    title=title,
                    ats_url=ats_url
                )

                dataset.append(SyntheticJobProfile(
                    job_id=f"SYNTH_BENIGN_{i:04d}",
                    target_role=title,
                    claimed_employer=company,
                    compensation_text="$22.00 - $28.00/hr",
                    description_body=body,
                    injected_red_flags=[],
                    is_fraudulent=False,
                    ground_truth_threat_level="BENIGN"
                ))

        return dataset
