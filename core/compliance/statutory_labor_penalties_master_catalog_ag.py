"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AG
Statutory labor reference volume AG covering Southern African Development Community (SADC)
(Botswana, Namibia, Zambia, Zimbabwe), private employment agency codes, and worker protections.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SADCLaborStatuteAG:
    statute_id: str
    country_iso: str
    country_name: str
    act_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAG:
    """Master expanded catalog volume AG covering SADC statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, SADCLaborStatuteAG] = {}
        self._seed_volume_ag()

    def _seed_volume_ag() -> None:
        """Register SADC statutory labor regulations."""

        records = [
            (
                "STAT-AG-001",
                "BW",
                "Botswana",
                "Employment Act (Cap. 47:01) & Private Employment Agencies Regulations",
                "Section 12 & Section 145",
                "Demanding or receiving any fee, reward or commission from a job applicant for procuring employment.",
                30000.0,
                [
                    "Revocation of agency operating certificate by Commissioner of Labour",
                    "Fines and compensation orders enforced via the Industrial Court of Botswana",
                    "Mandatory refund of all fees paid with statutory interest"
                ],
                "Department of Labour and Social Security (Ministry of Labour and Home Affairs, Botswana)"
            ),
            (
                "STAT-AG-002",
                "NA",
                "Namibia",
                "Labour Act, 2007 (Act No. 11 of 2007) & Employment Services Act 8 of 2011",
                "Section 16 & Section 25",
                "Private employment agencies charging fees to individual work-seekers for placement services.",
                35000.0,
                [
                    "Cancellation of registration with the Employment Services Board",
                    "Prosecution in the Labour Court and mandatory full restitution"
                ],
                "Ministry of Labour, Industrial Relations and Employment Creation (Namibia)"
            ),
            (
                "STAT-AG-003",
                "ZM",
                "Zambia",
                "Employment Code Act, No. 3 of 2019",
                "Section 10 & Section 120",
                "Charging any recruitment fee, registration fee, or medical examination fee directly to a job applicant.",
                25000.0,
                [
                    "Withdrawal of the private employment agency operating permit",
                    "Summary conviction fines and full reimbursement to affected workers"
                ],
                "Ministry of Labour and Social Security (Zambia)"
            ),
            (
                "STAT-AG-004",
                "ZW",
                "Zimbabwe",
                "Labour Act (Chapter 28:01) & Private Employment Agencies Regulations",
                "Section 114 & Section 118",
                "Charging fees to work-seekers for finding employment or operating without registration.",
                20000.0,
                [
                    "Deregistration of the private employment agency",
                    "Prosecution in the Labour Court of Zimbabwe with restitution directives"
                ],
                "Ministry of Public Service, Labour and Social Welfare (Zimbabwe)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = SADCLaborStatuteAG(
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

    def get_statute(self, statute_id: str) -> Optional[SADCLaborStatuteAG]:
        return self.statutes.get(statute_id)
