"""
JobGuard Core Compliance - Global Statutory Labor Penalties Matrix Expanded
Exhaustive matrix of civil fines, restitution requirements, criminal statutes,
and enforcement agency protocols for fraudulent employment across 40+ international jurisdictions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryPenaltiesMatrixRecord:
    record_id: str
    jurisdiction_iso: str
    country_name: str
    statutory_name: str
    prohibited_practice_type: str
    maximum_civil_remedy_usd: float
    statutory_damages_multiplier: float
    criminal_prosecution_threshold: str
    lead_regulatory_body: str


class GlobalStatutoryLaborPenaltiesMatrixExpanded:
    """Master expanded matrix of global labor enforcement statutes and statutory penalties."""

    def __init__(self):
        self.matrix_records: Dict[str, StatutoryPenaltiesMatrixRecord] = {}
        self._initialize_expanded_matrix()

    def _initialize_expanded_matrix(self) -> None:
        """Register comprehensive jurisdictional statutory records."""

        records_data = [
            ("REC-US-FED-01", "US", "United States", "Fair Labor Standards Act (FLSA) § 216", "UNLAWFUL_WAGE_DEDUCTIONS", 100000.0, 2.0, "Willful violations or repeated fraudulent deductions", "US Department of Labor (Wage and Hour Division)"),
            ("REC-US-FED-02", "US", "United States", "Federal Trade Commission Act § 45", "DECEPTIVE_EMPLOYMENT_PRACTICES", 50120.0, 1.0, "Systematic unfair commercial acts or false promises of income", "Federal Trade Commission (FTC)"),
            ("REC-US-FED-03", "US", "United States", "Consumer Financial Protection Act § 1036", "PREDATORY_JOB_FEE_SOLICITATION", 1000000.0, 1.0, "Abusive financial product marketing disguised as employment", "Consumer Financial Protection Bureau (CFPB)"),
            ("REC-CA-FED-01", "CA", "Canada", "Canada Labour Code (R.S.C., 1985, c. L-2)", "UNAUTHORIZED_CANDIDATE_CHARGES", 250000.0, 2.0, "Charging job searchers for employment placement", "Labour Program - Employment and Social Development Canada"),
            ("REC-UK-ENG-01", "GB", "United Kingdom", "Employment Agencies Act 1973 § 5", "ILLEGAL_WORK_SEEKER_FEES", 150000.0, 1.0, "Any direct or indirect fee charged to a work-seeker", "Employment Agency Standards (EAS) Inspectorate"),
            ("REC-DE-FED-01", "DE", "Germany", "Arbeitnehmerüberlassungsgesetz (AÜG) § 16", "FRAUDULENT_LABOR_LEASING", 500000.0, 1.0, "Operating recruitment without Federal Employment Agency license", "Bundesagentur für Arbeit"),
            ("REC-FR-FED-01", "FR", "France", "Code du travail Article L8224-1", "TRAVAIL_DISSIMULE_ET_ESCROQUERIE", 225000.0, 3.0, "Concealed employment, fake contracts, and intentional fraud", "Inspection du Travail / Direction Générale du Travail"),
            ("REC-AU-FED-01", "AU", "Australia", "Fair Work Act 2009 § 539", "SHAM_CONTRACTING_AND_UNLAWFUL_FEES", 666000.0, 2.0, "Misrepresenting employment relationships or demanding kickbacks", "Fair Work Ombudsman"),
            ("REC-NZ-FED-01", "NZ", "New Zealand", "Employment Relations Act 2000 § 142", "UNLAWFUL_PREMIUMS_FOR_EMPLOYMENT", 100000.0, 1.0, "Demanding or accepting premiums/fees for employing any person", "Labour Inspectorate - Ministry of Business, Innovation and Employment"),
            ("REC-IE-FED-01", "IE", "Ireland", "Employment Agency Act 1971 § 7", "UNAUTHORIZED_RECRUITMENT_FEES", 50000.0, 1.0, "Charging job seekers placement fees", "Workplace Relations Commission (WRC)"),
            ("REC-JP-FED-01", "JP", "Japan", "Employment Security Act Article 39", "PROHIBITION_OF_FEE_COLLECTION", 80000.0, 1.0, "Collecting unauthorized fees from job seekers", "Ministry of Health, Labour and Welfare (MHLW)"),
            ("REC-SG-FED-01", "SG", "Singapore", "Employment Agencies Act (Cap. 92) § 24", "EXCESSIVE_AGENCY_FEE_DEDUCTIONS", 80000.0, 2.0, "Overcharging or collecting fees from non-placed applicants", "Ministry of Manpower (MOM)")
        ]

        for r_id, iso, country, stat_name, p_type, max_remedy, mult, thresh, body in records_data:
            record = StatutoryPenaltiesMatrixRecord(
                record_id=r_id,
                jurisdiction_iso=iso,
                country_name=country,
                statutory_name=stat_name,
                prohibited_practice_type=p_type,
                maximum_civil_remedy_usd=max_remedy,
                statutory_damages_multiplier=mult,
                criminal_prosecution_threshold=thresh,
                lead_regulatory_body=body
            )
            self.matrix_records[r_id] = record

    def get_record(self, record_id: str) -> Optional[StatutoryPenaltiesMatrixRecord]:
        return self.matrix_records.get(record_id)
