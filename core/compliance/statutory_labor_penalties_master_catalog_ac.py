"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AC
Statutory labor reference volume AC covering GCC (Gulf Cooperation Council) unified labor regulations
(Kuwait, Oman, Bahrain), domestic worker protections, and mandatory wage protection systems (WPS).
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class GCCLaborStatuteAC:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_fine_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAC:
    """Master expanded catalog volume AC covering GCC unified statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, GCCLaborStatuteAC] = {}
        self._seed_volume_ac()

    def _seed_volume_ac() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AC-001",
                "KW",
                "Kuwait",
                "Kuwait Private Sector Labour Law (Law No. 6 of 2010)",
                "Article 10 & Article 57",
                "Prohibiting employers and recruitment agencies from charging financial consideration or fees to workers for their employment or residency visas.",
                35000.0,
                [
                    "Cancellation of the recruitment agency license by PAM",
                    "Forfeiture of statutory bank guarantee deposited with Public Authority for Manpower",
                    "Mandatory employer payment of all repatriation and recruitment expenses"
                ],
                "Public Authority for Manpower (PAM Kuwait)"
            ),
            (
                "STAT-AC-002",
                "OM",
                "Oman",
                "Oman Labour Law (Royal Decree No. 53/2023)",
                "Article 20 & Article 138",
                "Charging or collecting recruitment fees, flight expenses, or passport retention charges from expatriate or domestic workers.",
                40000.0,
                [
                    "Suspension or permanent revocation of manpower recruitment license",
                    "Fines up to 5,000 OMR (~$13,000 USD) per affected employee and imprisonment up to one year",
                    "Compulsory electronic wage payment through Central Bank of Oman WPS"
                ],
                "Ministry of Labour (Sultanate of Oman)"
            ),
            (
                "STAT-AC-003",
                "BH",
                "Bahrain",
                "Bahrain Private Sector Labour Law (Law No. 36 of 2012) & LMRA Law No. 19/2006",
                "Article 23 & Article 36",
                "Demanding fees from workers in exchange for employment permits or operating unlicensed manpower recruitment agencies.",
                30000.0,
                [
                    "Immediate closure of recruitment office and revocation of LMRA license",
                    "Court orders for full restitution of all fees extorted from migrant jobseekers",
                    "Criminal penalties for forced labor or illegal visa trade"
                ],
                "Labour Market Regulatory Authority (LMRA Bahrain)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, fine, rems, enf in records:
            self.statutes[s_id] = GCCLaborStatuteAC(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_fine_usd_equivalent=fine,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[GCCLaborStatuteAC]:
        return self.statutes.get(statute_id)
