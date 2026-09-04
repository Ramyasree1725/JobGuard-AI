"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume T
Statutory labor reference volume T covering African regional labor codes
(South Africa, Nigeria, Kenya, Ghana), worker recruitment fee bans, and statutory penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class AfricanLaborStatuteT:
    statute_id: str
    country_iso: str
    country_name: str
    act_title: str
    section_citation: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogT:
    """Master expanded catalog volume T covering African statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, AfricanLaborStatuteT] = {}
        self._seed_volume_t()

    def _seed_volume_t() -> None:
        """Register African statutory labor regulations."""

        records = [
            (
                "STAT-T-001",
                "ZA",
                "South Africa",
                "Employment Services Act 4 of 2014 & Basic Conditions of Employment Act",
                "Section 15 & Section 16",
                "Charging any fee to a work-seeker for providing employment services or job placement.",
                35000.0,
                [
                    "Cancellation of registration of private employment agency",
                    "Mandatory refund of all fees charged to work-seekers with interest",
                    "Referral to Labour Court for compliance order enforcement"
                ],
                "Department of Employment and Labour (Republic of South Africa)"
            ),
            (
                "STAT-T-002",
                "NG",
                "Nigeria",
                "Labour Act (Cap L1, LFN 2004) & Cybercrimes (Prohibition, Prevention) Act 2015",
                "Section 71 & Section 14",
                "Operating private employment agencies without recruiter's licence from the Minister or publishing fraudulent online recruitment adverts.",
                40000.0,
                [
                    "Prosecution by Economic and Financial Crimes Commission (EFCC)",
                    "Imprisonment up to 7 years for cyber recruitment advance fee fraud",
                    "Forfeiture of criminal assets and restitution to victims"
                ],
                "Federal Ministry of Labour and Employment / EFCC"
            ),
            (
                "STAT-T-003",
                "KE",
                "Kenya",
                "Labour Institutions Act (No. 12 of 2007) & Employment Act 2007",
                "Section 56 & Section 60",
                "Charging job placement fees or commissions to employees or job seekers exceeding statutory guidelines.",
                30000.0,
                [
                    "Revocation of National Employment Authority (NEA) accreditation",
                    "Fines and imprisonment for directors of non-compliant agencies"
                ],
                "Ministry of Labour and Social Protection / National Employment Authority (NEA)"
            ),
            (
                "STAT-T-004",
                "GH",
                "Ghana",
                "Labour Act, 2003 (Act 651)",
                "Section 7 & Section 9",
                "Private employment agencies charging fees to job seekers for employment placement.",
                25000.0,
                [
                    "Immediate withdrawal of agency operating permit",
                    "Refund of all sums extracted from job applicants",
                    "Prosecution in the National Labour Commission (NLC)"
                ],
                "Ministry of Employment and Labour Relations / Labour Department Ghana"
            )
        ]

        for s_id, iso, cname, act, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = AfricanLaborStatuteT(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                act_title=act,
                section_citation=sec,
                prohibited_recruitment_practice=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[AfricanLaborStatuteT]:
        return self.statutes.get(statute_id)
