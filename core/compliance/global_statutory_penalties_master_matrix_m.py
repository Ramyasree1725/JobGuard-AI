"""
JobGuard Core Compliance - Global Statutory Penalties Master Matrix Volume M
Matrix of international criminal sanctions, corporate fines, and debarment remedies
for cybercrime, unauthorized recruitment agency operations, and human trafficking traps.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class PenaltyMatrixEntryM:
    matrix_id: str
    country_iso: str
    crime_classification: str
    governing_statute_code: str
    corporate_fine_cap_usd: float
    individual_prison_max_years: int
    corporate_debarment_mandatory: bool
    regulatory_remedies: List[str]


class GlobalStatutoryPenaltiesMasterMatrixM:
    """Master expanded matrix of international penal codes for recruitment fraud volume M."""

    def __init__(self):
        self.matrix: Dict[str, PenaltyMatrixEntryM] = {}
        self._seed_matrix_m()

    def _seed_matrix_m() -> None:
        """Register extensive international penal records."""

        records = [
            (
                "PM-M-001",
                "GB",
                "Fraud by False Representation & Unlawful Agency Operation",
                "UK Fraud Act 2006 § 2 & Employment Agencies Act 1973 § 6",
                500000.0,
                10,
                True,
                [
                    "Unlimited corporate fines upon conviction on indictment",
                    "Prohibition order banning individuals from operating recruitment agencies for up to 10 years",
                    "Compensation orders under Proceeds of Crime Act 2002 (POCA)"
                ]
            ),
            (
                "PM-M-002",
                "AU",
                "Misleading Employment Conduct & Unlawful Fee Extraction",
                "Competition and Consumer Act 2010 (ACL § 31) & Criminal Code Act 1995 § 134",
                10000000.0,  # AUD 10M+
                10,
                True,
                [
                    "Civil penalties of greater of $10M or 3x benefit obtained",
                    "Disqualification from managing corporations under Corporations Act 2001",
                    "Public warning notices and mandatory corrective advertising"
                ]
            ),
            (
                "PM-M-003",
                "CA",
                "Deceptive Telemarketing & Employment Fraud Inducement",
                "Competition Act (R.S.C., 1985, c. C-34) § 52.1 & Criminal Code § 380",
                2500000.0,
                14,
                True,
                [
                    "Administrative monetary penalties and mandatory customer refunds",
                    "Court orders restraining operations of telemarketing / web call centers",
                    "Injunctions freezing Canadian bank accounts and assets"
                ]
            ),
            (
                "PM-M-004",
                "DE",
                "Gewerbsmäßiger Betrug (Commercial Fraud) & Unlicensed Placement",
                "Strafgesetzbuch (StGB) § 263 & AÜG § 16",
                1500000.0,
                10,
                True,
                [
                    "Confiscation of all gross criminal proceeds pursuant to StGB § 73",
                    "Revocation of corporate commercial trade license (Gewerbeuntersagung)",
                    "Compulsory compensation of victim out-of-pocket losses"
                ]
            ),
            (
                "PM-M-005",
                "SG",
                "Cheating by Personation & Unlicensed Employment Agency Offenses",
                "Penal Code 1871 § 419 / § 420 & Employment Agencies Act § 24",
                300000.0,
                10,
                True,
                [
                    "Forfeiture of security deposit furnished to Ministry of Manpower",
                    "Permanent debarment from employing foreign workers or operating agencies",
                    "Mandatory full restitution of all fees collected from applicants"
                ]
            )
        ]

        for m_id, iso, crime, code, fine, prison, debar, rems in records:
            self.matrix[m_id] = PenaltyMatrixEntryM(
                matrix_id=m_id,
                country_iso=iso,
                crime_classification=crime,
                governing_statute_code=code,
                corporate_fine_cap_usd=fine,
                individual_prison_max_years=prison,
                corporate_debarment_mandatory=debar,
                regulatory_remedies=rems
            )

    def get_entry(self, matrix_id: str) -> Optional[PenaltyMatrixEntryM]:
        return self.matrix.get(matrix_id)
