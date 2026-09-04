"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AE
Statutory labor reference volume AE covering East African Community (EAC) unified labor codes
(Uganda, Tanzania, Rwanda, Ethiopia), overseas recruitment guidelines, and fee prohibitions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EastAfricanLaborStatuteAE:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd_equivalent: float
    administrative_remedies: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAE:
    """Master expanded catalog volume AE covering East African Community statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, EastAfricanLaborStatuteAE] = {}
        self._seed_volume_ae()

    def _seed_volume_ae() -> None:
        """Register East African statutory labor regulations."""

        records = [
            (
                "STAT-AE-001",
                "UG",
                "Uganda",
                "Employment (Recruitment of Ugandan Migrant Workers) Regulations, 2021",
                "Regulation 14 & Regulation 28",
                "Charging unauthorized placement fees or administrative charges to migrant workers exceeding statutory limits.",
                30000.0,
                [
                    "Revocation of recruitment license by the Ministry",
                    "Forfeiture of statutory bank guarantee (UGX 100,000,000)",
                    "Criminal prosecution for human trafficking or illegal recruitment"
                ],
                "Ministry of Gender, Labour and Social Development (Uganda)"
            ),
            (
                "STAT-AE-002",
                "TZ",
                "Tanzania",
                "Employment and Labour Relations Act (Act No. 6 of 2004) & Labour Institutions Act",
                "Section 29 & Section 64",
                "Private employment agencies charging fees or demanding payment from job seekers for job placement.",
                25000.0,
                [
                    "Cancellation of private employment agency registration",
                    "Fines and mandatory refund orders enforced by the Commission for Mediation and Arbitration (CMA)"
                ],
                "Prime Minister's Office (Labour, Youth, Employment and Persons with Disability, Tanzania)"
            ),
            (
                "STAT-AE-003",
                "RW",
                "Rwanda",
                "Law No. 66/2018 of 30/08/2018 Regulating Labour in Rwanda",
                "Article 18 & Article 114",
                "Charging fees to workers for job application, placement, or hiring mediation services.",
                20000.0,
                [
                    "Withdrawal of the agency's operational license by MIFOTRA",
                    "Administrative fines imposed by the Labour Inspectorate"
                ],
                "Ministry of Public Service and Labour (MIFOTRA Rwanda)"
            ),
            (
                "STAT-AE-004",
                "ET",
                "Ethiopia",
                "Overseas Employment Proclamation (No. 923/2016) & Labour Proclamation No. 1156/2019",
                "Article 10 & Article 49",
                "Private employment agencies collecting any recruitment fee or expense directly from overseas jobseekers.",
                35000.0,
                [
                    "Revocation of overseas recruitment agency license",
                    "Forfeiture of USD 100,000 collateral deposit fund",
                    "Criminal imprisonment up to 10 years for illegal foreign placement"
                ],
                "Ministry of Labour and Skills (Ethiopia)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = EastAfricanLaborStatuteAE(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[EastAfricanLaborStatuteAE]:
        return self.statutes.get(statute_id)
