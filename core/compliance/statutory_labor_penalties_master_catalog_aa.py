"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AA
Statutory labor reference volume AA covering North African and Maghreb employment codes
(Morocco, Egypt, Tunisia, Algeria), private placement agency licensing, and worker rights charters.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MaghrebLaborStatuteAA:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_law_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd_equivalent: float
    administrative_remedies: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAA:
    """Master expanded catalog volume AA covering North African and Maghreb statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, MaghrebLaborStatuteAA] = {}
        self._seed_volume_aa()

    def _seed_volume_aa() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AA-001",
                "MA",
                "Morocco",
                "Code du travail marocain (Loi n° 65-99)",
                "Article 480 & Article 493",
                "Percevoir des sommes d'argent ou des honoraires auprès des demandeurs d'emploi pour des prestations de recrutement ou d'embauche.",
                35000.0,
                [
                    "Retrait immédiat de l'autorisation d'exercer délivrée par le Ministère de l'Emploi",
                    "Amendes pénales de 10.000 à 20.000 DH et restitution obligatoire des sommes indûment perçues",
                    "Fermeture administrative de l'agence privée de recrutement"
                ],
                "Ministère de l'Inclusion Économique, de la Petite Entreprise, de l'Emploi et des Compétences (Maroc)"
            ),
            (
                "STAT-AA-002",
                "EG",
                "Egypt",
                "Egyptian Labour Law No. 12 of 2003 & Law No. 148 of 2019",
                "Article 21 & Article 22",
                "Collecting fees or financial amounts from workers in exchange for their employment inside Egypt or abroad exceeding statutory caps.",
                40000.0,
                [
                    "Revocation of the company's operating license and forfeiture of the statutory bank guarantee (EGP 100,000+)",
                    "Criminal imprisonment for a period not less than one month and fine up to EGP 50,000",
                    "Mandatory full refund of all amounts collected from workers"
                ],
                "Ministry of Manpower and Emigration (Egypt)"
            ),
            (
                "STAT-AA-003",
                "TN",
                "Tunisia",
                "Code du travail tunisien (Loi n° 66-27) & Décret n° 2010-2917",
                "Article 285 & Article 292",
                "Exiger des demandeurs d'emploi des frais d'inscription, des commissions ou des retenues sur salaires.",
                25000.0,
                [
                    "Annulation de l'agrément ministériel accordé au bureau privé d'emploi",
                    "Sanctions pénales prononcées par le tribunal cantonal ou de première instance"
                ],
                "Inspection générale du Travail (Ministère de l'Emploi et de la Formation Professionnelle, Tunisie)"
            ),
            (
                "STAT-AA-004",
                "DZ",
                "Algeria",
                "Loi n° 04-19 relative au placement des travailleurs et au contrôle de l'emploi",
                "Article 15 & Article 32",
                "Percevoir une rémunération ou des frais auprès des demandeurs d'emploi sous quelque forme que ce soit.",
                30000.0,
                [
                    "Retrait définitif de l'agrément de l'organisme privé de placement",
                    "Poursuites judiciaires et amendes infligées par l'Inspection du Travail"
                ],
                "Inspection générale du Travail (Ministère du Travail, de l'Emploi et de la Sécurité Sociale, Algérie)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = MaghrebLaborStatuteAA(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_penalty_usd_equivalent=pen,
                administrative_remedies=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[MaghrebLaborStatuteAA]:
        return self.statutes.get(statute_id)
