"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AN
Statutory labor reference volume AN covering East African Horn & Red Sea regional labor codes
(Djibouti, Somalia, Eritrea, South Sudan), private placement regulations, and fee bans.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class HornOfAfricaLaborStatuteAN:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_act_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAN:
    """Master expanded catalog volume AN covering Horn of Africa statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, HornOfAfricaLaborStatuteAN] = {}
        self._seed_volume_an()

    def _seed_volume_an() -> None:
        """Register Horn of Africa statutory labor regulations."""

        records = [
            (
                "STAT-AN-001",
                "DJ",
                "Djibouti",
                "Code du travail de la République de Djibouti (Loi n° 133/AN/05/5ème L)",
                "Article 21 & Article 260",
                "Percevoir des droits ou honoraires auprès des demandeurs d'emploi lors des formalités d'embauche ou de placement.",
                25000.0,
                [
                    "Retrait de la licence d'exploitation du bureau privé de placement",
                    "Amendes pénales infligées par le Tribunal de Première Instance de Djibouti",
                    "Remboursement intégral des sommes perçues"
                ],
                "Inspection du Travail et des Lois Sociales (Ministère du Travail chargé de la Formalisation et de la Protection Sociale, Djibouti)"
            ),
            (
                "STAT-AN-002",
                "SO",
                "Somalia",
                "Somali Labour Code (Law No. 65 of 1972) & National Employment Policy",
                "Article 16 & Article 142",
                "Charging fees or commissions to workers for employment placement or recruitment services.",
                20000.0,
                [
                    "Revocation of private employment agency permit by the Ministry",
                    "Summary fines and mandatory restitution to affected jobseekers"
                ],
                "Ministry of Labour and Social Affairs (Federal Government of Somalia)"
            ),
            (
                "STAT-AN-003",
                "ER",
                "Eritrea",
                "Labour Proclamation of Eritrea (Proclamation No. 118/2001)",
                "Article 10 & Article 88",
                "Demanding payments or deductions from jobseekers for employment mediation.",
                15000.0,
                [
                    "Cancellation of agency operating permit",
                    "Restitution orders enforced by the Department of Labour"
                ],
                "Department of Labour (Ministry of Labour and Human Welfare, Eritrea)"
            ),
            (
                "STAT-AN-004",
                "SS",
                "South Sudan",
                "Labour Act, 2017 (Act No. 64 of 2017)",
                "Section 19 & Section 112",
                "Private employment agencies charging fees or demanding remuneration from work-seekers.",
                20000.0,
                [
                    "Revocation of recruitment agency certificate",
                    "Fines and compensation orders enforced by the Commissioner for Labour"
                ],
                "Ministry of Labour, Public Service and Human Resource Development (South Sudan)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = HornOfAfricaLaborStatuteAN(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_act_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[HornOfAfricaLaborStatuteAN]:
        return self.statutes.get(statute_id)
