"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AM
Statutory labor reference volume AM covering Central African & Sahelian labor standards
(Chad, Niger, Mali, Burkina Faso, Central African Republic), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SahelLaborStatuteAM:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_act_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAM:
    """Master expanded catalog volume AM covering Central African and Sahelian statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, SahelLaborStatuteAM] = {}
        self._seed_volume_am()

    def _seed_volume_am() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AM-001",
                "TD",
                "Chad",
                "Code du travail de la République du Tchad (Loi n° 038/PR/96)",
                "Article 28 & Article 294",
                "Percevoir des sommes d'argent, des commissions ou des frais auprès des travailleurs à l'occasion de leur placement.",
                25000.0,
                [
                    "Retrait immédiat de l'autorisation d'ouverture du bureau privé de placement",
                    "Poursuites pénales et restitution intégrale des montants perçus avec intérêts",
                    "Amendes infligées par l'Inspection du Travail et des Lois Sociales"
                ],
                "Direction de l'Inspection du Travail (Ministère de la Fonction Publique et de l'Emploi, Tchad)"
            ),
            (
                "STAT-AM-002",
                "NE",
                "Niger",
                "Code du travail du Niger (Loi n° 2012-45)",
                "Article 34 & Article 348",
                "Exiger des demandeurs d'emploi une rétribution quelconque pour des services de placement ou d'embauche.",
                20000.0,
                [
                    "Annulation de l'agrément ministériel accordé à l'agence de placement",
                    "Sanctions pécuniaires prononcées par le Tribunal du Travail",
                    "Remboursement obligatoire des frais de dossier indûment facturés"
                ],
                "Inspection générale du Travail (Ministère de l'Emploi, du Travail et de la Protection Sociale, Niger)"
            ),
            (
                "STAT-AM-003",
                "ML",
                "Mali",
                "Code du travail de la République du Mali (Loi n° 92-020)",
                "Article L.318 & Article L.329",
                "Perception d'honoraires ou de dépôts de garantie auprès des travailleurs lors de la médiation pour l'emploi.",
                25000.0,
                [
                    "Fermeture administrative définitive de l'organisme privé de placement",
                    "Amendes pénales infligées aux dirigeants et restitution aux victimes"
                ],
                "Direction Nationale du Travail (Ministère du Travail, de la Fonction Publique et du Dialogue Social, Mali)"
            ),
            (
                "STAT-AM-004",
                "BF",
                "Burkina Faso",
                "Code du travail du Burkina Faso (Loi n° 028-2008/AN)",
                "Article 41 & Article 422",
                "Faire payer par les demandeurs d'emploi des frais directs ou indirects pour l'accès à un emploi.",
                20000.0,
                [
                    "Retrait de la licence d'exploitation par le Ministre chargé du Travail",
                    "Saisine des juridictions du travail pour réparation des préjudices subis"
                ],
                "Direction générale du Travail (Ministère de la Fonction Publique, du Travail et de la Protection Sociale, Burkina Faso)"
            ),
            (
                "STAT-AM-005",
                "CF",
                "Central African Republic",
                "Code du travail de la République Centrafricaine (Loi n° 09.004)",
                "Article 22 & Article 308",
                "Exiger une rémunération des travailleurs pour des opérations de placement de main-d'œuvre.",
                20000.0,
                [
                    "Suspension d'activité de l'agence de recrutement",
                    "Condamnation à la restitution des sommes perçues"
                ],
                "Inspection générale du Travail (Ministère du Travail, de l'Emploi, de la Formation Professionnelle et de la Protection Sociale, RCA)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = SahelLaborStatuteAM(
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

    def get_statute(self, statute_id: str) -> Optional[SahelLaborStatuteAM]:
        return self.statutes.get(statute_id)
