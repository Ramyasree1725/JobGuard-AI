"""
JobGuard Core Compliance - Cross-Border Recruitment & Foreign Labor Regulatory Framework
Governs compliance with US H-1B / H-2A / H-2B recruiter fee prohibitions, Canadian Temporary
Foreign Worker Program (TFWP) regulations, and UK Gangmasters and Labour Abuse Authority (GLAA).
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class VisaCategory(Enum):
    US_H1B_SPECIALTY_OCCUPATION = "US_H1B_SPECIALTY_OCCUPATION"
    US_H2B_NON_AGRICULTURAL = "US_H2B_NON_AGRICULTURAL"
    CA_TFWP_TEMPORARY_FOREIGN_WORKER = "CA_TFWP_TEMPORARY_FOREIGN_WORKER"
    UK_SKILLED_WORKER_TIER_2 = "UK_SKILLED_WORKER_TIER_2"
    AU_TSS_SUBCLASS_482 = "AU_TSS_SUBCLASS_482"


@dataclass
class VisaComplianceStatute:
    statute_code: str
    visa_type: VisaCategory
    governing_regulation: str
    fee_prohibition_clause: str
    employer_must_pay_costs: List[str]
    prohibited_candidate_charges: List[str]
    maximum_penalty_description: str


class CrossBorderRecruitmentRegulatoryFramework:
    """Master compliance database for foreign migrant and guest worker recruitment protection."""

    def __init__(self):
        self.statutes: Dict[VisaCategory, VisaComplianceStatute] = {}
        self._initialize_statutes()

    def _initialize_statutes(self) -> None:
        """Register cross-border employment visa compliance statutes."""

        # US H-1B Specialty Occupation
        self.statutes[VisaCategory.US_H1B_SPECIALTY_OCCUPATION] = VisaComplianceStatute(
            statute_code="US-20CFR655-731",
            visa_type=VisaCategory.US_H1B_SPECIALTY_OCCUPATION,
            governing_regulation="20 C.F.R. § 655.731 & 8 U.S.C. § 1182(n)",
            fee_prohibition_clause="Employers are strictly prohibited from requiring H-1B nonimmigrants to pay the ACWIA fee, filing fees, or recoupment penalties.",
            employer_must_pay_costs=[
                "USCIS I-129 petition filing fees",
                "Fraud Prevention and Detection Fee ($500)",
                "ACWIA training fee ($750 - $1,500)",
                "Mandatory prevailing wage as certified on Labor Condition Application (LCA)"
            ],
            prohibited_candidate_charges=[
                "Any attorney fees for petition preparation",
                "Penalty fees for quitting prior to contractual end date",
                "Bench fees or un-paid nonproductive downtime"
            ],
            maximum_penalty_description="Debarment from H-1B program for up to 3 years, back wages, and civil fines up to $50,000 per violation."
        )

        # US H-2B Non-Agricultural Guest Workers
        self.statutes[VisaCategory.US_H2B_NON_AGRICULTURAL] = VisaComplianceStatute(
            statute_code="US-20CFR655-20",
            visa_type=VisaCategory.US_H2B_NON_AGRICULTURAL,
            governing_regulation="20 C.F.R. § 655.20(p)",
            fee_prohibition_clause="Neither the employer nor its agents may seek or receive payment of any kind from a prospective employee for recruitment or job placement.",
            employer_must_pay_costs=[
                "Inbound and outbound international transportation and subsistence",
                "All visa application and processing fees",
                "Work tools and protective equipment at no cost"
            ],
            prohibited_candidate_charges=[
                "Recruitment agency finder fees",
                "Visa appointment booking fees",
                "Security deposits for equipment"
            ],
            maximum_penalty_description="Immediate petition revocation, mandatory refund of all prohibited fees with interest, and federal debarment."
        )

        # Canada TFWP
        self.statutes[VisaCategory.CA_TFWP_TEMPORARY_FOREIGN_WORKER] = VisaComplianceStatute(
            statute_code="CA-IRPR-203",
            visa_type=VisaCategory.CA_TFWP_TEMPORARY_FOREIGN_WORKER,
            governing_regulation="Immigration and Refugee Protection Regulations (IRPR) § 203(1)(e)",
            fee_prohibition_clause="Employers must not directly or indirectly charge or recover from a foreign worker any recruitment-related fees or LMIA application fees.",
            employer_must_pay_costs=[
                "LMIA processing fee ($1,000 CAD)",
                "Airfare transportation to Canada and return",
                "Private health insurance until provincial coverage activates"
            ],
            prohibited_candidate_charges=[
                "Job placement fees",
                "Third-party recruiter commissions",
                "Immigration document handling fees"
            ],
            maximum_penalty_description="Permanent debarment from hiring foreign workers and administrative monetary penalties up to $1,000,000 CAD."
        )

    def audit_foreign_worker_offer(self, visa_type: VisaCategory, candidate_charged_amount: float) -> Tuple[bool, str]:
        """Audits whether any fees assessed to a foreign applicant violate immigration labor statutes."""
        if visa_type not in self.statutes:
            return True, "No specific cross-border statute mapped."

        statute = self.statutes[visa_type]
        if candidate_charged_amount > 0:
            return False, f"CRITICAL IMMIGRATION VIOLATION ({statute.statute_code}): Charging candidate ${candidate_charged_amount:,.2f} is illegal under {statute.governing_regulation}."

        return True, f"Compliant: Zero recruitment fees charged pursuant to {statute.governing_regulation}."
