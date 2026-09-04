"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AI
Statutory labor reference volume AI covering Central European & Non-EU European jurisdictions
(Liechtenstein, Monaco, Andorra, San Marino, Iceland), private recruitment standards, and worker protections.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MicrostateLaborStatuteAI:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_law_title: str
    article_reference: str
    prohibited_conduct_summary: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAI:
    """Master expanded catalog volume AI covering European Microstates and Nordic regional labor codes."""

    def __init__(self):
        self.statutes: Dict[str, MicrostateLaborStatuteAI] = {}
        self._seed_volume_ai()

    def _seed_volume_ai() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AI-001",
                "IS",
                "Iceland",
                "Act on Temporary Work Agencies (No. 139/2005) & Working Environment Act",
                "Article 5 & Article 18",
                "Charging fees or demanding financial compensation from workers for hiring out or employment placement.",
                35000.0,
                [
                    "Suspension or revocation of the agency operating permit",
                    "Administrative fines imposed by the Directorate of Labour (Vinnumálastofnun)",
                    "Mandatory refund of all fees with statutory interest"
                ],
                "Vinnumálastofnun (Directorate of Labour Iceland)"
            ),
            (
                "STAT-AI-002",
                "LI",
                "Liechtenstein",
                "Arbeitsvermittlungsgesetz (AVG - LGBl. 2000 Nr. 104)",
                "Artikel 11 & Artikel 38",
                "Erhebung von Vermittlungsgebühren oder Kostenbeteiligungen von Arbeitsuchenden für die Vermittlung.",
                40000.0,
                [
                    "Entzug der Bewilligung zur Arbeitsvermittlung durch das Amt für Volkswirtschaft",
                    "Bussen bis zu 50'000 CHF und Strafanzeige beim Landgericht"
                ],
                "Amt für Volkswirtschaft (AVW Liechtenstein)"
            ),
            (
                "STAT-AI-003",
                "MC",
                "Monaco",
                "Loi n° 629 du 17 juillet 1957 tendant à régir les conditions d'engagement et de licenciement",
                "Article 7 & Article 22",
                "Perception d'honoraires ou de frais auprès des demandeurs d'emploi pour leur placement.",
                30000.0,
                [
                    "Fermeture administrative de l'agence privée de placement",
                    "Sanctions pénales prononcées par le Tribunal de Première Instance de Monaco"
                ],
                "Direction du Travail (Principauté de Monaco)"
            ),
            (
                "STAT-AI-004",
                "AD",
                "Andorra",
                "Llei 31/2018, del 6 de desembre, de relacions laborals",
                "Article 19 & Article 145",
                "Cobrar tarifes o comissions als treballadors per la prestació de serveis d'intermediació laboral.",
                25000.0,
                [
                    "Cancel·lació de l'autorització d'obertura del servei de col·locació",
                    "Sancions econòmiques greus imposades per la Inspecció de Treball"
                ],
                "Inspecció de Treball (Govern d'Andorra)"
            ),
            (
                "STAT-AI-005",
                "SM",
                "San Marino",
                "Legge 29 settembre 2005 n. 131 (Riforma del Mercato del Lavoro)",
                "Articolo 8 & Articolo 44",
                "Richiesta di compensi o trattenute a carico dei lavoratori per l'accesso al lavoro.",
                25000.0,
                [
                    "Revoca dell'autorizzazione all'esercizio dell'attività di intermediazione",
                    "Sanzioni amministrative pecuniarie inflitte dalla Direzione Generale dell'Ufficio del Lavoro"
                ],
                "Ufficio del Lavoro (Repubblica di San Marino)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = MicrostateLaborStatuteAI(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_title=title,
                article_reference=art,
                prohibited_conduct_summary=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[MicrostateLaborStatuteAI]:
        return self.statutes.get(statute_id)
