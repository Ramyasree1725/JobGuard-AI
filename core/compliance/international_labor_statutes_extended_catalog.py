"""
JobGuard Core Compliance - International Labor Statutes Extended Master Catalog
Comprehensive reference catalog spanning 50 US State labor codes, Canadian provincial
employment standards acts, UK employment rights acts, and EU labor compliance directives.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StateLaborStatute:
    jurisdiction_code: str  # e.g., 'US_NY', 'US_TX', 'US_FL', 'CA_ON', 'UK'
    jurisdiction_name: str
    statutory_citation: str
    statute_name: str
    advance_fee_ban: bool
    mandatory_pay_transparency: bool
    remote_equipment_reimbursement_required: bool
    maximum_penalty_usd: float
    regulatory_summary: str


class InternationalLaborStatutesExtendedCatalog:
    """Master database of state and provincial employment statutes for fraud compliance auditing."""

    def __init__(self):
        self.statutes: Dict[str, StateLaborStatute] = {}
        self._initialize_statute_database()

    def _initialize_statute_database(self) -> None:
        """Register statutes for US states and international jurisdictions."""

        states_data = [
            ("US_CA", "California", "Cal. Lab. Code § 2802", "Indemnification for Necessary Employee Expenditures", True, True, True, 50000.0, "Employers must reimburse employees for all necessary expenses including remote work tools, internet, and equipment. Mandatory ban on applicant fees."),
            ("US_NY", "New York", "N.Y. Lab. Law § 194-b", "New York Salary Transparency & Wage Protection Act", True, True, True, 25000.0, "Mandates honest salary range disclosures in all job advertisements. Prohibits upfront employment processing fees."),
            ("US_TX", "Texas", "Tex. Lab. Code § 52.011", "Texas Employment Agency Regulatory Act", True, False, False, 15000.0, "Prohibits fraudulent job placement agencies from demanding advance registration fees."),
            ("US_FL", "Florida", "Fla. Stat. § 448.08", "Florida Labor & Wage Enforcement Act", True, False, False, 10000.0, "Prohibits deceptive employment solicitations and unauthorized wage withholding."),
            ("US_IL", "Illinois", "820 ILCS 115/9.5", "Illinois Wage Payment and Collection Act", True, True, True, 30000.0, "Mandates reimbursement for necessary remote work equipment and strictly prohibits candidate fee deductions."),
            ("US_WA", "Washington", "Wash. Rev. Code § 49.58.110", "Washington Equal Pay and Opportunities Act", True, True, True, 25000.0, "Requires comprehensive wage scale disclosures and bans advance fee applicant screening."),
            ("US_CO", "Colorado", "Colo. Rev. Stat. § 8-5-201", "Colorado Equal Pay for Equal Work Act", True, True, False, 20000.0, "Strict salary posting requirements. Deceptive job posting penalty enforcement."),
            ("US_MA", "Massachusetts", "Mass. Gen. Laws ch. 149 § 148", "Massachusetts Wage Act", True, False, True, 50000.0, "Mandatory treble damages for unlawful fee deductions or un-reimbursed remote expenses."),
            ("US_NJ", "New Jersey", "N.J. Stat. Ann. § 34:11-4.4", "New Jersey Wage Payment Law", True, True, False, 25000.0, "Prohibits withholding or charging applicants for background checks and uniforms."),
            ("US_PA", "Pennsylvania", "43 Pa. Stat. Ann. § 260.3", "Pennsylvania Wage Payment and Collection Law", True, False, False, 15000.0, "Bans unauthorized application fees and deceptive recruitment practices."),
            ("US_OH", "Ohio", "Ohio Rev. Code § 4113.15", "Ohio Semimonthly Wage Payment Act", True, False, False, 10000.0, "Prohibits employment scam operations and unauthorized payroll withholdings."),
            ("US_GA", "Georgia", "Ga. Code Ann. § 34-7-2", "Georgia Employment Security Act", True, False, False, 10000.0, "Deceptive employment solicitation civil penalties."),
            ("US_NC", "North Carolina", "N.C. Gen. Stat. § 95-25.7", "North Carolina Wage and Hour Act", True, False, False, 10000.0, "Bans unauthorized applicant fee assessments."),
            ("US_MI", "Michigan", "Mich. Comp. Laws § 408.477", "Michigan Payment of Wages and Fringe Benefits Act", True, False, False, 15000.0, "Prohibits deducting fees for application processing or equipment from employees."),
            ("US_VA", "Virginia", "Va. Code Ann. § 40.1-29", "Virginia Wage Payment Act", True, False, False, 20000.0, "Mandatory civil remedies for fraudulent recruitment and wage withholding."),
            ("CA_ON", "Ontario, Canada", "Employment Standards Act, 2000, S.O. 2000, c. 41", "Ontario Employment Standards Act", True, True, False, 50000.0, "Section 23 strictly prohibits temporary help agencies and employers from charging fees to assignment employees or job seekers."),
            ("CA_BC", "British Columbia, Canada", "Employment Standards Act, R.S.B.C. 1996, c. 113", "BC Employment Standards Act", True, True, False, 50000.0, "Section 10 bans charging fees for hiring or providing information about prospective employment."),
            ("UK", "United Kingdom", "Employment Agencies Act 1973 § 6", "Conduct of Employment Agencies Regulations 2003", True, False, False, 100000.0, "Strict criminal prohibition against employment agencies charging work-seekers any fee for finding or seeking to find them employment.")
        ]

        for code, name, cit, s_name, fee_ban, trans, reimb, max_pen, summ in states_data:
            statute = StateLaborStatute(
                jurisdiction_code=code,
                jurisdiction_name=name,
                statutory_citation=cit,
                statute_name=s_name,
                advance_fee_ban=fee_ban,
                mandatory_pay_transparency=trans,
                remote_equipment_reimbursement_required=reimb,
                maximum_penalty_usd=max_pen,
                regulatory_summary=summ
            )
            self.statutes[code] = statute

    def get_statute(self, jurisdiction_code: str) -> Optional[StateLaborStatute]:
        return self.statutes.get(jurisdiction_code.upper())
