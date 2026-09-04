"""
JobGuard Core Compliance - Global Labor Statutes, Statutory Minimums & Criminal Codes
Comprehensive database of jurisdictional employment protections across India, US, UK, EU,
Canada, and Australia, including statutory fee prohibitions and cyber fraud provisions.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryCode:
    statute_id: str
    country: str
    jurisdiction_level: str  # "FEDERAL", "STATE", "DIRECTIVE"
    statute_name: str
    section_reference: str
    prohibition_category: str  # "UPFRONT_FEE_BAN", "TRAINING_COST_MANDATE", "IMPERSONATION_FRAUD", "MINIMUM_WAGE"
    penalty_summary: str
    statutory_text_summary: str
    complaint_filing_portal: str
    enforcement_agency: str


class GlobalLaborStatutesRegistry:
    """Master statutory compliance database for international employment law audits."""

    def __init__(self):
        self.statutes: Dict[str, StatutoryCode] = {}
        self._populate_statutes()

    def register_statute(self, statute: StatutoryCode) -> None:
        self.statutes[statute.statute_id] = statute

    def _populate_statutes(self) -> None:
        """Populate global labor codes and cybercrime statutes."""
        statute_list = [
            # India Statutes
            StatutoryCode(
                statute_id="IN-IT-66D",
                country="IN",
                jurisdiction_level="FEDERAL",
                statute_name="Information Technology Act, 2000",
                section_reference="Section 66D",
                prohibition_category="IMPERSONATION_FRAUD",
                penalty_summary="Imprisonment up to 3 years and fine up to ₹1,00,000",
                statutory_text_summary="Punishes cheating by personation by using computer resources or communication devices.",
                complaint_filing_portal="https://cybercrime.gov.in / National Helpline 1930",
                enforcement_agency="Ministry of Home Affairs - Indian Cyber Crime Coordination Centre (I4C)"
            ),
            StatutoryCode(
                statute_id="IN-IPC-420",
                country="IN",
                jurisdiction_level="FEDERAL",
                statute_name="Indian Penal Code, 1860 / Bharatiya Nyaya Sanhita, 2023",
                section_reference="Section 420 (BNS Section 318)",
                prohibition_category="UPFRONT_FEE_BAN",
                penalty_summary="Imprisonment up to 7 years and fine",
                statutory_text_summary="Cheating and dishonestly inducing delivery of property or alteration of valuable securities.",
                complaint_filing_portal="Local Police Station / State Cyber Cell",
                enforcement_agency="State Police Cyber Crime Division"
            ),
            StatutoryCode(
                statute_id="IN-EMIG-1983",
                country="IN",
                jurisdiction_level="FEDERAL",
                statute_name="Emigration Act, 1983",
                section_reference="Section 10 & 24",
                prohibition_category="UPFRONT_FEE_BAN",
                penalty_summary="Imprisonment up to 2 years and fine",
                statutory_text_summary="Prohibits unregistered recruiting agents from collecting service charges or overseas recruitment fees.",
                complaint_filing_portal="https://emigrate.gov.in",
                enforcement_agency="Protector General of Emigrants, Ministry of External Affairs"
            ),

            # US Federal Statutes
            StatutoryCode(
                statute_id="US-FTC-SEC5",
                country="US",
                jurisdiction_level="FEDERAL",
                statute_name="Federal Trade Commission Act",
                section_reference="15 U.S.C. § 45 (Section 5)",
                prohibition_category="UPFRONT_FEE_BAN",
                penalty_summary="Civil penalties up to $50,120 per violation plus restitution",
                statutory_text_summary="Prohibits unfair or deceptive acts or practices in commerce, including bogus work-from-home earnings claims.",
                complaint_filing_portal="https://reportfraud.ftc.gov",
                enforcement_agency="Federal Trade Commission (FTC)"
            ),
            StatutoryCode(
                statute_id="US-18USC-1343",
                country="US",
                jurisdiction_level="FEDERAL",
                statute_name="United States Criminal Code",
                section_reference="18 U.S.C. § 1343 (Wire Fraud)",
                prohibition_category="IMPERSONATION_FRAUD",
                penalty_summary="Fines up to $1,000,000 and imprisonment up to 20 years (30 years if financial institution affected)",
                statutory_text_summary="Criminalizes schemes to defraud or obtain money by means of false pretenses transmitted via interstate wire.",
                complaint_filing_portal="https://ic3.gov",
                enforcement_agency="Federal Bureau of Investigation (FBI) - Internet Crime Complaint Center"
            ),
            StatutoryCode(
                statute_id="US-FLSA-203",
                country="US",
                jurisdiction_level="FEDERAL",
                statute_name="Fair Labor Standards Act of 1938 (FLSA)",
                section_reference="29 U.S.C. § 203 et seq.",
                prohibition_category="TRAINING_COST_MANDATE",
                penalty_summary="Back wages, liquidated damages equal to unpaid wages, and civil money penalties",
                statutory_text_summary="Mandates employers pay statutory minimum wages for all onboarding hours and prohibited employer kickbacks.",
                complaint_filing_portal="https://dol.gov/agencies/whd",
                enforcement_agency="US Department of Labor - Wage and Hour Division (WHD)"
            ),

            # European Union Directives
            StatutoryCode(
                statute_id="EU-DIR-2019-1152",
                country="EU",
                jurisdiction_level="DIRECTIVE",
                statute_name="EU Directive on Transparent and Predictable Working Conditions",
                section_reference="Directive (EU) 2019/1152, Article 13",
                prohibition_category="TRAINING_COST_MANDATE",
                penalty_summary="Member State statutory fines and mandatory candidate compensation",
                statutory_text_summary="Mandatory training must be provided cost-free to the worker and count as working hours.",
                complaint_filing_portal="National Labor Inspectorate in Member State",
                enforcement_agency="European Labour Authority (ELA)"
            ),
            StatutoryCode(
                statute_id="EU-GDPR-ART82",
                country="EU",
                jurisdiction_level="DIRECTIVE",
                statute_name="General Data Protection Regulation (GDPR)",
                section_reference="Regulation (EU) 2016/679, Article 82 & 83",
                prohibition_category="IMPERSONATION_FRAUD",
                penalty_summary="Administrative fines up to €20 million or 4% of total worldwide annual turnover",
                statutory_text_summary="Severe penalties for unlawful processing and deceptive harvesting of candidate biometric/personal data.",
                complaint_filing_portal="National Data Protection Authority (DPA)",
                enforcement_agency="European Data Protection Board (EDPB)"
            ),

            # United Kingdom Statutes
            StatutoryCode(
                statute_id="UK-EA-1973",
                country="UK",
                jurisdiction_level="FEDERAL",
                statute_name="Employment Agencies Act 1973",
                section_reference="Section 6(1)",
                prohibition_category="UPFRONT_FEE_BAN",
                penalty_summary="Unlimited fine in Crown Court and director disqualification",
                statutory_text_summary="Explicitly forbids employment agencies from charging candidates any fee for finding or seeking employment.",
                complaint_filing_portal="https://gov.uk/eas",
                enforcement_agency="Employment Agency Standards (EAS) Inspectorate"
            ),
            StatutoryCode(
                statute_id="UK-FRAUD-2006",
                country="UK",
                jurisdiction_level="FEDERAL",
                statute_name="Fraud Act 2006",
                section_reference="Section 2 (Fraud by False Representation)",
                prohibition_category="IMPERSONATION_FRAUD",
                penalty_summary="Imprisonment up to 10 years and unlimited fine",
                statutory_text_summary="Criminalizes dishonestly making a false representation with intent to make a financial gain.",
                complaint_filing_portal="https://actionfraud.police.uk",
                enforcement_agency="Action Fraud & National Fraud Intelligence Bureau (NFIB)"
            )
        ]

        for st in statute_list:
            self.register_statute(st)

    def query_statutes_for_violation(self, violation_category: str, country: Optional[str] = None) -> List[StatutoryCode]:
        """Query matching statutory provisions by violation type and jurisdiction."""
        matches = []
        for st in self.statutes.values():
            if st.prohibition_category == violation_category or violation_category == "ALL":
                if country is None or st.country == country or st.country == "EU":
                    matches.append(st)
        return matches
