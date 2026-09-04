"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume H
Detailed statutory reference volume H covering Nordic, Benelux, and East Asian employment codes,
foreign recruiter licensing mandates, and statutory criminal penalties for recruitment fraud.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class GlobalStatuteDetailH:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_name: str
    governing_article: str
    prohibited_recruitment_practice: str
    criminal_penalty_summary: str
    civil_fine_cap_eur_or_usd: float
    enforcement_agency: str


class StatutoryLaborPenaltiesMasterCatalogH:
    """Master expanded catalog of international statutory labor protections and criminal penalties."""

    def __init__(self):
        self.catalog_records: Dict[str, GlobalStatuteDetailH] = {}
        self._seed_volume_h()

    def _seed_volume_h() -> None:
        """Register extensive global statutory definitions."""

        entries = [
            (
                "STAT-H-001",
                "NL",
                "Netherlands",
                "Wet allocatie arbeidskrachten door intermediairs (Waadi)",
                "Article 9a",
                "Charging any fee, direct or indirect, to workers for job mediation services.",
                "Administrative fines and potential criminal prosecution under Economic Offences Act.",
                45000.0,
                "Nederlandse Arbeidsinspectie (Netherlands Labour Authority)"
            ),
            (
                "STAT-H-002",
                "BE",
                "Belgium",
                "Decreet betreffende de private arbeidsbemiddeling",
                "Article 12",
                "Demanding remuneration or expenses from work-seekers for placement or intake.",
                "Imprisonment from 8 days to 1 year and permanent business closure.",
                50000.0,
                "Inspectie Werk en Sociale Economie (Flemish Labour Inspection)"
            ),
            (
                "STAT-H-003",
                "SE",
                "Sweden",
                "Lag (2012:854) om uthyrning av arbetstagare",
                "Section 14",
                "Imposing fees on jobseekers or temporary agency workers for employment acquisition.",
                "Damages and compensation pursuant to Swedish Employment Protection Act (LAS).",
                35000.0,
                "Arbetsmiljöverket (Swedish Work Environment Authority)"
            ),
            (
                "STAT-H-004",
                "NO",
                "Norway",
                "Arbeidsmiljøloven (Working Environment Act)",
                "Chapter 14, Section 14-12",
                "Charging fees to employees for hiring out or recruitment placement.",
                "Fines and imprisonment up to 3 years for aggravated violations.",
                60000.0,
                "Arbeidstilsynet (Norwegian Labour Inspection Authority)"
            ),
            (
                "STAT-H-005",
                "DK",
                "Denmark",
                "Lov om arbejdsformidling og arbejdsløshedsforsikring",
                "Section 24",
                "Collecting payment from job seekers for job placement services.",
                "Fines and suspension of recruitment intermediary certification.",
                40000.0,
                "Styrelsen for Arbejdsmarked og Rekruttering (STAR)"
            ),
            (
                "STAT-H-006",
                "KR",
                "South Korea",
                "Employment Security Act (Act No. 17326)",
                "Article 19 & Article 46",
                "Collecting fees from job seekers exceeding statutory limits or operating unlicensed job placement.",
                "Imprisonment for up to 5 years or fine up to 50 million KRW (~$40,000 USD).",
                40000.0,
                "Ministry of Employment and Labor (MOEL)"
            ),
            (
                "STAT-H-007",
                "TW",
                "Taiwan",
                "Employment Service Act (勞動部就業服務法)",
                "Article 40",
                "Demanding or accepting fees other than prescribed statutory charges from job applicants.",
                "Fine up to 20 times the demanded fee and suspension of operations.",
                50000.0,
                "Ministry of Labor (MOL Taiwan) Workforce Development Agency"
            ),
            (
                "STAT-H-008",
                "HK",
                "Hong Kong SAR",
                "Employment Agency Regulations (Cap. 57A)",
                "Section 10 & Part XII",
                "Charging job applicants commission exceeding 10% of their first month salary.",
                "Fine up to HKD 350,000 (~$45,000 USD) and 3 years imprisonment.",
                45000.0,
                "Labour Department (Employment Agencies Administration)"
            )
        ]

        for s_id, iso, cname, sname, art, pract, crim, cap, enf in entries:
            self.catalog_records[s_id] = GlobalStatuteDetailH(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_name=sname,
                governing_article=art,
                prohibited_recruitment_practice=pract,
                criminal_penalty_summary=crim,
                civil_fine_cap_eur_or_usd=cap,
                enforcement_agency=enf
            )

    def get_statute(self, statute_id: str) -> Optional[GlobalStatuteDetailH]:
        return self.catalog_records.get(statute_id)
