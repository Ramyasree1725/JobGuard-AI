"""
JobGuard Core Knowledge - Standard Occupational Classification (SOC) & Role Taxonomies
Contains hierarchical job taxonomy codes, required credential baselines,
typical educational requirements, and salary variance bounds.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class OccupationalRole:
    soc_code: str  # e.g., "15-1252.00"
    title: str
    major_group: str
    typical_min_education: str
    required_skills: List[str]
    annual_median_wage_usd: float
    hourly_median_wage_usd: float
    telework_eligibility: bool = True


class TaxonomyDictionary:
    """Master repository of Standard Occupational Classification (SOC) taxonomies."""

    def __init__(self):
        self.roles: Dict[str, OccupationalRole] = {}
        self._title_index: Dict[str, str] = {}
        self._populate_soc_roles()

    def register(self, role: OccupationalRole) -> None:
        self.roles[role.soc_code] = role
        self._title_index[role.title.lower()] = role.soc_code

    def _populate_soc_roles(self) -> None:
        """Populate representative standard occupational roles."""
        occupations = [
            OccupationalRole(
                soc_code="15-1252.00",
                title="Software Developers",
                major_group="Computer and Mathematical Occupations",
                typical_min_education="Bachelor's Degree",
                required_skills=["Python", "JavaScript", "SQL", "Git", "Data Structures", "System Design"],
                annual_median_wage_usd=127260.0,
                hourly_median_wage_usd=61.18
            ),
            OccupationalRole(
                soc_code="15-1253.00",
                title="Software Quality Assurance Analysts and Testers",
                major_group="Computer and Mathematical Occupations",
                typical_min_education="Bachelor's Degree",
                required_skills=["Selenium", "Pytest", "Jira", "Automated Testing", "API Testing"],
                annual_median_wage_usd=99620.0,
                hourly_median_wage_usd=47.89
            ),
            OccupationalRole(
                soc_code="15-2051.00",
                title="Data Scientists",
                major_group="Computer and Mathematical Occupations",
                typical_min_education="Master's Degree",
                required_skills=["Machine Learning", "Python", "R", "Statistics", "Pandas", "PyTorch"],
                annual_median_wage_usd=103500.0,
                hourly_median_wage_usd=49.76
            ),
            OccupationalRole(
                soc_code="15-1212.00",
                title="Information Security Analysts",
                major_group="Computer and Mathematical Occupations",
                typical_min_education="Bachelor's Degree",
                required_skills=["SIEM", "Network Security", "Incident Response", "Vulnerability Scanning", "Firewalls"],
                annual_median_wage_usd=112000.0,
                hourly_median_wage_usd=53.85
            ),
            OccupationalRole(
                soc_code="43-9021.00",
                title="Data Entry Keyers",
                major_group="Office and Administrative Support Occupations",
                typical_min_education="High School Diploma",
                required_skills=["Typing Speed", "Data Entry", "Microsoft Excel", "Attention to Detail"],
                annual_median_wage_usd=35850.0,
                hourly_median_wage_usd=17.24
            ),
            OccupationalRole(
                soc_code="43-4051.00",
                title="Customer Service Representatives",
                major_group="Office and Administrative Support Occupations",
                typical_min_education="High School Diploma",
                required_skills=["Verbal Communication", "CRM Software", "Conflict Resolution", "Ticketing"],
                annual_median_wage_usd=37780.0,
                hourly_median_wage_usd=18.16
            )
        ]

        for occ in occupations:
            self.register(occ)

    def lookup_title(self, title: str) -> Optional[OccupationalRole]:
        clean = title.strip().lower()
        if clean in self._title_index:
            return self.roles[self._title_index[clean]]
        for t, code in self._title_index.items():
            if t in clean or clean in t:
                return self.roles[code]
        return None
