"""
JobGuard Core Knowledge - Standard Occupational Classification (SOC) Risk Index
Maps labor market statistics, standard job titles, typical salary distribution bands,
and vulnerability risk coefficients for fraud anomaly analysis.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import statistics


@dataclass
class SalaryBand:
    currency: str
    hourly_p10: float
    hourly_median: float
    hourly_p90: float
    annual_p10: float
    annual_median: float
    annual_p90: float


@dataclass
class OccupationalProfile:
    soc_code: str
    title: str
    major_group: str
    salary_benchmarks: SalaryBand
    remote_work_feasibility: float  # 0.0 to 1.0
    fraud_target_vulnerability: float  # 0.0 (rarely targeted) to 1.0 (heavily targeted)
    common_scam_vectors: List[str]
    standard_hiring_requirements: List[str]
    description: str


@dataclass
class CompensationAnomalyReport:
    claimed_rate: float
    rate_period: str  # 'hourly' or 'annual'
    expected_median: float
    ratio_to_median: float
    percentile_estimate: float
    is_hyper_inflated: bool
    is_sub_minimum: bool
    risk_score: float
    analysis_narrative: str


class OccupationalRiskIndex:
    """Master benchmark catalog of labor codes, market compensation, and fraud vulnerability."""

    def __init__(self):
        self.occupations: Dict[str, OccupationalProfile] = {}
        self.title_lookup: Dict[str, str] = {}  # Normalized title -> soc_code
        self._initialize_soc_database()

    def _initialize_soc_database(self) -> None:
        """Populate standard occupational classification profiles and compensation benchmarks."""

        # 43-9021: Data Entry Keyers (Extremely High Scam Target)
        self._register_occupation(OccupationalProfile(
            soc_code="43-9021",
            title="Data Entry Keyer",
            major_group="Office and Administrative Support Occupations",
            salary_benchmarks=SalaryBand(
                currency="USD",
                hourly_p10=14.50, hourly_median=18.50, hourly_p90=24.50,
                annual_p10=30160.0, annual_median=38480.0, annual_p90=50960.0
            ),
            remote_work_feasibility=0.90,
            fraud_target_vulnerability=0.95,
            common_scam_vectors=[
                "Fake check for office equipment",
                "Hyper-inflated hourly rates ($40-$75/hr for basic typing)",
                "Upfront software training fees",
                "Telegram/WhatsApp direct chat interviews"
            ],
            standard_hiring_requirements=["High school diploma or GED", "Typing speed certification (45+ WPM)"],
            description="Operates data entry devices to verify and enter data into computer systems."
        ))

        # 43-4051: Customer Service Representatives
        self._register_occupation(OccupationalProfile(
            soc_code="43-4051",
            title="Customer Service Representative",
            major_group="Office and Administrative Support Occupations",
            salary_benchmarks=SalaryBand(
                currency="USD",
                hourly_p10=15.00, hourly_median=19.80, hourly_p90=28.50,
                annual_p10=31200.0, annual_median=41184.0, annual_p90=59280.0
            ),
            remote_work_feasibility=0.85,
            fraud_target_vulnerability=0.85,
            common_scam_vectors=[
                "Remote call center equipment advance check scam",
                "Identity theft via direct deposit onboarding forms",
                "Mystery shopper / secret evaluator fake checks"
            ],
            standard_hiring_requirements=["High school diploma", "Communication skills", "Basic computer literacy"],
            description="Interacts with customers to provide information in response to inquiries about products and services."
        ))

        # 43-6014: Secretaries and Administrative Assistants
        self._register_occupation(OccupationalProfile(
            soc_code="43-6014",
            title="Administrative Assistant",
            major_group="Office and Administrative Support Occupations",
            salary_benchmarks=SalaryBand(
                currency="USD",
                hourly_p10=16.50, hourly_median=22.00, hourly_p90=31.50,
                annual_p10=34320.0, annual_median=45760.0, annual_p90=65520.0
            ),
            remote_work_feasibility=0.75,
            fraud_target_vulnerability=0.90,
            common_scam_vectors=[
                "Executive virtual personal assistant package forwarding",
                "Purchasing gift cards with counterfeit corporate credit cards",
                "Receiving and reshipping stolen goods (package mule)"
            ],
            standard_hiring_requirements=["High school diploma", "Calendar management", "Office suite proficiency"],
            description="Performs routine clerical and administrative functions such as drafting correspondence and scheduling appointments."
        ))

        # 15-1252: Software Developers
        self._register_occupation(OccupationalProfile(
            soc_code="15-1252",
            title="Software Developer",
            major_group="Computer and Mathematical Occupations",
            salary_benchmarks=SalaryBand(
                currency="USD",
                hourly_p10=38.00, hourly_median=63.50, hourly_p90=98.00,
                annual_p10=79040.0, annual_median=132270.0, annual_p90=203840.0
            ),
            remote_work_feasibility=0.98,
            fraud_target_vulnerability=0.60,
            common_scam_vectors=[
                "Fake tech startup coding test containing malware",
                "Impersonation of FAANG recruiters on LinkedIn",
                "Unpaid trial project code harvesting",
                "Malicious NPM repository installation during interview"
            ],
            standard_hiring_requirements=["Bachelor's degree or equivalent experience", "Algorithmic coding evaluation", "System design interview"],
            description="Researches, designs, and develops computer software systems and applications."
        ))

        # 13-1161: Market Research Analysts and Marketing Specialists
        self._register_occupation(OccupationalProfile(
            soc_code="13-1161",
            title="Marketing Specialist",
            major_group="Business and Financial Operations Occupations",
            salary_benchmarks=SalaryBand(
                currency="USD",
                hourly_p10=20.00, hourly_median=33.00, hourly_p90=55.00,
                annual_p10=41600.0, annual_median=68640.0, annual_p90=114400.0
            ),
            remote_work_feasibility=0.85,
            fraud_target_vulnerability=0.70,
            common_scam_vectors=[
                "Social media rating task scams",
                "Influencer recruitment affiliate fee scheme",
                "Unpaid marketing campaign pitch theft"
            ],
            standard_hiring_requirements=["Bachelor's degree in marketing/business", "Portfolio review", "Campaign management experience"],
            description="Researches conditions in local, regional, or national areas to determine potential sales of a product or service."
        ))

        # 27-3091: Interpreters and Translators
        self._register_occupation(OccupationalProfile(
            soc_code="27-3091",
            title="Translator",
            major_group="Arts, Design, Entertainment, Sports, and Media Occupations",
            salary_benchmarks=SalaryBand(
                currency="USD",
                hourly_p10=18.00, hourly_median=27.50, hourly_p90=46.00,
                annual_p10=37440.0, annual_median=57200.0, annual_p90=95680.0
            ),
            remote_work_feasibility=0.95,
            fraud_target_vulnerability=0.75,
            common_scam_vectors=[
                "Book translation project with fake check payment",
                "Advance document notarization fee",
                "Unpaid massive sample translation"
            ],
            standard_hiring_requirements=["Fluency in two or more languages", "Translation sample review", "Industry certification"],
            description="Interprets oral or sign language, or translates written text from one language into another."
        ))

    def _register_occupation(self, profile: OccupationalProfile) -> None:
        self.occupations[profile.soc_code] = profile
        normalized_title = profile.title.lower().strip()
        self.title_lookup[normalized_title] = profile.soc_code
        
        # Also map keywords
        words = normalized_title.split()
        for word in words:
            if len(word) > 4:
                self.title_lookup[word] = profile.soc_code

    def lookup_occupation(self, title_query: str) -> Optional[OccupationalProfile]:
        """Matches a job title to the closest SOC profile using normalized fuzzy token matching."""
        query_norm = title_query.lower().strip()
        
        # Exact match
        if query_norm in self.title_lookup:
            return self.occupations.get(self.title_lookup[query_norm])

        # Substring match
        for key, soc_code in self.title_lookup.items():
            if key in query_norm or query_norm in key:
                return self.occupations.get(soc_code)

        return None

    def evaluate_compensation(self, title: str, claimed_rate: float, rate_period: str = "hourly") -> CompensationAnomalyReport:
        """Evaluates whether a claimed salary/rate represents a hyper-inflated red flag anomaly."""
        profile = self.lookup_occupation(title)
        
        if not profile:
            # Fallback baseline
            return CompensationAnomalyReport(
                claimed_rate=claimed_rate,
                rate_period=rate_period,
                expected_median=25.0 if rate_period == "hourly" else 52000.0,
                ratio_to_median=1.0,
                percentile_estimate=50.0,
                is_hyper_inflated=False,
                is_sub_minimum=False,
                risk_score=10.0,
                analysis_narrative="Standard market compensation profile (general baseline)."
            )

        benchmarks = profile.salary_benchmarks
        if rate_period == "hourly":
            expected_median = benchmarks.hourly_median
            p10 = benchmarks.hourly_p10
            p90 = benchmarks.hourly_p90
        else:
            expected_median = benchmarks.annual_median
            p10 = benchmarks.annual_p10
            p90 = benchmarks.annual_p90

        ratio = claimed_rate / max(1.0, expected_median)
        
        # Anomaly scoring logic
        is_hyper_inflated = False
        is_sub_minimum = False
        risk_score = 0.0

        if ratio >= 2.5:
            is_hyper_inflated = True
            risk_score = 85.0
            narrative = (f"CRITICAL SALARY ANOMALY: Claimed rate of ${claimed_rate:,.2f}/{rate_period} is {ratio:.1f}x higher "
                         f"than national median (${expected_median:,.2f}) for {profile.title}. "
                         f"Scammers routinely offer unrealistic rates to bait victims.")
        elif ratio >= 1.8:
            is_hyper_inflated = True
            risk_score = 50.0
            narrative = (f"SUSPICIOUS COMPENSATION: Claimed rate of ${claimed_rate:,.2f}/{rate_period} is significantly above "
                         f"90th percentile (${p90:,.2f}) for entry-level {profile.title}.")
        elif claimed_rate < p10 * 0.6:
            is_sub_minimum = True
            risk_score = 40.0
            narrative = f"SUB-MARKET COMPENSATION: Rate of ${claimed_rate:,.2f}/{rate_period} falls drastically below standard minimum wage."
        else:
            risk_score = 5.0
            narrative = f"COMPENSATION ALIGNED: Rate of ${claimed_rate:,.2f}/{rate_period} is consistent with standard market percentiles."

        # Compute estimated percentile
        if claimed_rate <= p10:
            percentile = max(1.0, (claimed_rate / p10) * 10.0)
        elif claimed_rate <= expected_median:
            percentile = 10.0 + ((claimed_rate - p10) / (expected_median - p10)) * 40.0
        elif claimed_rate <= p90:
            percentile = 50.0 + ((claimed_rate - expected_median) / (p90 - expected_median)) * 40.0
        else:
            percentile = min(99.9, 90.0 + ((claimed_rate - p90) / p90) * 10.0)

        return CompensationAnomalyReport(
            claimed_rate=claimed_rate,
            rate_period=rate_period,
            expected_median=expected_median,
            ratio_to_median=ratio,
            percentile_estimate=percentile,
            is_hyper_inflated=is_hyper_inflated,
            is_sub_minimum=is_sub_minimum,
            risk_score=risk_score,
            analysis_narrative=narrative
        )
