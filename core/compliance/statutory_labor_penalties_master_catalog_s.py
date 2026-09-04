"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume S
Statutory labor reference volume S covering East Asian & DACH regional employment codes
(Japan, Germany, Austria, Switzerland), worker dispatching laws, and fee prohibitions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class DACHEastAsiaStatuteS:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    section_reference: str
    prohibited_conduct: str
    maximum_penalty_usd: float
    licensing_sanctions: str
    regulatory_ministry: str


class StatutoryLaborPenaltiesMasterCatalogS:
    """Master expanded catalog volume S covering DACH and East Asian labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, DACHEastAsiaStatuteS] = {}
        self._seed_volume_s()

    def _seed_volume_s() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-S-001",
                "JP",
                "Japan",
                "Employment Security Act (職業安定法 - Act No. 141 of 1947)",
                "Article 32-3 & Article 63",
                "Collecting actual recruitment fees from job seekers without explicit statutory permission.",
                50000.0,
                "Imprisonment with work for up to one year or fine up to 1,000,000 JPY; license revocation.",
                "Ministry of Health, Labour and Welfare (MHLW / Hello Work)"
            ),
            (
                "STAT-S-002",
                "DE",
                "Germany",
                "Arbeitnehmerüberlassungsgesetz (AÜG) & SGB III § 296",
                "§ 16 AÜG & § 296 Abs. 2 SGB III",
                "Vereinbarung von Vermittlungsvergütungen mit Arbeitsuchenden, die gesetzliche Höchstgrenzen überschreiten.",
                60000.0,
                "Bußgelder bis zu 30.000 EUR pro Einzelfall und Versagung der Erlaubnis zur Arbeitnehmerüberlassung.",
                "Bundesagentur für Arbeit (BA)"
            ),
            (
                "STAT-S-003",
                "AT",
                "Austria",
                "Arbeitskräfteüberlassungsgesetz (AÜG) & Arbeitsmarktförderungsgesetz (AMFG)",
                "§ 4 AMFG & § 13 AÜG",
                "Forderung oder Entgegennahme von Vermittlungsentgelten von Arbeitsuchenden durch Personalberater.",
                40000.0,
                "Verwaltungsstrafen der Bezirksverwaltungsbehörde und Entziehung der Gewerbeberechtigung.",
                "Bundesministerium für Arbeit und Wirtschaft (BMAW / Arbeitsinspektion)"
            ),
            (
                "STAT-S-004",
                "CH",
                "Switzerland",
                "Bundesgesetz über die Arbeitsvermittlung und den Personalverleih (AVG - SR 823.11)",
                "Artikel 9 & Artikel 39",
                "Erhebung von Gebühren oder Kostenbeteiligungen von Stellensuchenden für die Arbeitsvermittlung.",
                45000.0,
                "Busse bis zu 100'000 CHF und Entzug der kantonalen oder eidgenössischen Vermittlungsbewilligung.",
                "Staatssekretariat für Wirtschaft (SECO) / Kantonale Arbeitsämter"
            )
        ]

        for s_id, iso, cname, title, sec, prohib, pen, lic, enf in records:
            self.statutes[s_id] = DACHEastAsiaStatuteS(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                section_reference=sec,
                prohibited_conduct=prohib,
                maximum_penalty_usd=pen,
                licensing_sanctions=lic,
                regulatory_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[DACHEastAsiaStatuteS]:
        return self.statutes.get(statute_id)
