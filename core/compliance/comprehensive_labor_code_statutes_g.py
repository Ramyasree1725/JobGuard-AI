"""
JobGuard Core Compliance - Comprehensive Labor Code & Statutory Penalties Volume G
Detailed statutory catalog covering mountain and western US state jurisdictions,
Commonwealth member state employment acts, and European union cross-border protections.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class WesternStatuteRecord:
    statute_id: str
    jurisdiction_code: str
    state_or_country: str
    statutory_citation: str
    prohibited_scheme_name: str
    minimum_statutory_damages_usd: float
    maximum_civil_penalty_usd: float
    criminal_charge_level: str
    mandatory_injunction: bool
    summary_text: str
    enforcement_protocol: str


class ComprehensiveLaborCodeStatutesG:
    """Master statutory reference volume G covering Western US and Pacific employment protection codes."""

    def __init__(self):
        self.records: Dict[str, WesternStatuteRecord] = {}
        self._seed_western_records()

    def _seed_western_records(self) -> None:
        """Register extensive statutory definitions across western and mountain regions."""

        entries = [
            (
                "STAT-G-001",
                "US_OR",
                "Oregon",
                "ORS § 659A.355",
                "Unlawful Consideration Demands and Advance Fee Traps",
                1000.0,
                25000.0,
                "Class A Misdemeanor / Felony Fraud if > $1,000",
                True,
                "Unlawful for any employer or recruiter to require payment of application fees, equipment deposits, or background costs from job applicants.",
                "Oregon Bureau of Labor and Industries (BOLI) Enforcement Protocol"
            ),
            (
                "STAT-G-002",
                "US_AZ",
                "Arizona",
                "A.R.S. § 23-353",
                "Payment of Wages and Prohibition of Fraudulent Deductions",
                500.0,
                15000.0,
                "Class 3 Misdemeanor",
                True,
                "Bans unauthorized deductions for equipment or screening from prospective employee disbursements. Mandates full legal tender pay.",
                "Industrial Commission of Arizona (ICA) Labor Department"
            ),
            (
                "STAT-G-003",
                "US_UT",
                "Utah",
                "Utah Code § 34-28-3",
                "Regular Paydays, Currency Mandate, and Anti-Scam Protection",
                500.0,
                10000.0,
                "Class B Misdemeanor",
                False,
                "Requires all wage disbursements in lawful currency of the United States. Prohibits crypto token scrip as sole wage payment.",
                "Utah Antidiscrimination and Labor Division (UALD)"
            ),
            (
                "STAT-G-004",
                "US_NV",
                "Nevada",
                "NRS § 608.050",
                "Nevada Employment Security and Fee Prohibition Standards",
                1000.0,
                20000.0,
                "Gross Misdemeanor",
                True,
                "Strict ban on demanding money or consideration from prospective employees for securing jobs or remote assignments.",
                "Office of the Nevada Labor Commissioner"
            ),
            (
                "STAT-G-005",
                "US_NM",
                "New Mexico",
                "NMSA 1978 § 50-4-2",
                "Semimonthly Pay, Legal Tender, and Deceptive Recruitment Ban",
                500.0,
                10000.0,
                "Petty Misdemeanor",
                False,
                "Prohibits fraudulent representations concerning work availability or compensation rates to prospective remote employees.",
                "New Mexico Department of Workforce Solutions (Labor Relations Division)"
            ),
            (
                "STAT-G-006",
                "US_ID",
                "Idaho",
                "Idaho Code § 44-1502",
                "Idaho Wage Payment and Truth in Recruitment Mandates",
                250.0,
                5000.0,
                "Misdemeanor",
                False,
                "Prohibits withholding candidate compensation for unverified third-party procurement vendors.",
                "Idaho Department of Labor (Wage and Hour Section)"
            ),
            (
                "STAT-G-007",
                "US_MT",
                "Montana",
                "Mont. Code Ann. § 39-3-204",
                "Montana Wage Protection and Employment Agreement Fidelity",
                500.0,
                10000.0,
                "Misdemeanor",
                True,
                "Mandates prompt payment of agreed compensation and criminalizes fraudulent checks issued for onboarding expenses.",
                "Montana Department of Labor and Industry"
            ),
            (
                "STAT-G-008",
                "US_HI",
                "Hawaii",
                "Haw. Rev. Stat. § 388-2",
                "Hawaii Semimonthly Wage Payment and Advance Fee Prohibition",
                1000.0,
                15000.0,
                "Misdemeanor / Class C Felony for Syndicate Operations",
                True,
                "Prohibits employment agencies and recruiters from extracting registration fees or charging for interview tests.",
                "Hawaii Department of Labor and Industrial Relations (DLIR)"
            )
        ]

        for s_id, jur, state, cit, name, min_d, max_p, charge, inj, summ, enf in entries:
            record = WesternStatuteRecord(
                statute_id=s_id,
                jurisdiction_code=jur,
                state_or_country=state,
                statutory_citation=cit,
                prohibited_scheme_name=name,
                minimum_statutory_damages_usd=min_d,
                maximum_civil_penalty_usd=max_p,
                criminal_charge_level=charge,
                mandatory_injunction=inj,
                summary_text=summ,
                enforcement_protocol=enf
            )
            self.records[s_id] = record

    def get_record(self, statute_id: str) -> Optional[WesternStatuteRecord]:
        return self.records.get(statute_id)
