"""
JobGuard Core Compliance - Global Statutory Penalties Master Matrix Volume L
Matrix of statutory fines, sentencing guidelines, and administrative restitution mandates
covering financial crimes, wire fraud, and banking falsifications in employment scams.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class PenaltyMatrixEntryL:
    matrix_id: str
    jurisdiction_code: str
    crime_category: str
    statutory_citation: str
    min_fine_usd: float
    max_fine_usd: float
    max_prison_years: int
    asset_forfeiture_mandatory: bool
    restitution_statute: str
    lead_prosecuting_authority: str


class GlobalStatutoryPenaltiesMasterMatrixL:
    """Master expanded matrix of statutory penalties for financial employment crimes volume L."""

    def __init__(self):
        self.matrix: Dict[str, PenaltyMatrixEntryL] = {}
        self._seed_matrix_l()

    def _seed_matrix_l() -> None:
        """Register extensive penalty matrix entries."""

        data = [
            (
                "PM-L-001",
                "US_FEDERAL",
                "Interstate Wire Fraud Scheme",
                "18 U.S.C. § 1343",
                10000.0,
                250000.0,
                20,
                True,
                "18 U.S.C. § 3663A (Mandatory Victims Restitution Act)",
                "United States Attorney's Office (DOJ)"
            ),
            (
                "PM-L-002",
                "US_FEDERAL",
                "Bank Fraud via Counterfeit Commercial Check",
                "18 U.S.C. § 1344",
                25000.0,
                1000000.0,
                30,
                True,
                "18 U.S.C. § 982 (Criminal Forfeiture)",
                "Federal Bureau of Investigation (FBI)"
            ),
            (
                "PM-L-003",
                "US_FEDERAL",
                "Money Laundering via Mule Procurement",
                "18 U.S.C. § 1956",
                50000.0,
                500000.0,
                20,
                True,
                "18 U.S.C. § 981 (Civil Forfeiture)",
                "Internal Revenue Service Criminal Investigation (IRS-CI)"
            ),
            (
                "PM-L-004",
                "US_FEDERAL",
                "Conspiracy to Commit Offense or Defraud United States",
                "18 U.S.C. § 371",
                10000.0,
                250000.0,
                5,
                True,
                "18 U.S.C. § 3663",
                "U.S. Department of Justice (DOJ)"
            ),
            (
                "PM-L-005",
                "US_CALIFORNIA",
                "Grand Theft by False Pretenses",
                "Cal. Penal Code § 487",
                5000.0,
                50000.0,
                3,
                False,
                "Cal. Penal Code § 1202.4 (Victim Restitution)",
                "California Attorney General / District Attorneys"
            ),
            (
                "PM-L-006",
                "US_NEW_YORK",
                "Scheme to Defraud in the First Degree",
                "N.Y. Penal Law § 190.65",
                5000.0,
                25000.0,
                4,
                False,
                "N.Y. CPL § 420.10",
                "New York Attorney General / County DAs"
            ),
            (
                "PM-L-007",
                "US_TEXAS",
                "Securing Execution of Document by Deception",
                "Tex. Penal Code § 32.46",
                5000.0,
                10000.0,
                10,
                False,
                "Tex. Code Crim. Proc. art. 42.037",
                "Texas Attorney General / District Attorneys"
            )
        ]

        for m_id, jur, cat, cit, min_f, max_f, prison, forf, rest, auth in data:
            self.matrix[m_id] = PenaltyMatrixEntryL(
                matrix_id=m_id,
                jurisdiction_code=jur,
                crime_category=cat,
                statutory_citation=cit,
                min_fine_usd=min_f,
                max_fine_usd=max_f,
                max_prison_years=prison,
                asset_forfeiture_mandatory=forf,
                restitution_statute=rest,
                lead_prosecuting_authority=auth
            )

    def get_penalty(self, matrix_id: str) -> Optional[PenaltyMatrixEntryL]:
        return self.matrix.get(matrix_id)
