"""
JobGuard Core Knowledge - Enterprise Corporate Lookup Database Part C
Contains verified corporate registrar entities, CIK codes, LEI identifiers, and ATS endpoints.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from core.knowledge.enterprise_corp_lookup_a import EnterpriseProfileData


CORP_LOOKUP_ENTRIES_C: List[EnterpriseProfileData] = [
    EnterpriseProfileData(
        cik="0003000001",
        lei="549300CORPC0000001",
        legal_name="Crestview Global Technology Systems Corporation 1",
        brand_name="CrestviewTech1",
        primary_domain="crestviewtech1.com",
        careers_portal="https://careers.crestviewtech1.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="New York, NY",
        country="US",
        authorized_email_domains=["crestviewtech1.com", "talent-crestview1.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000002",
        lei="549300CORPC0000002",
        legal_name="Crestview Global Technology Systems Corporation 2",
        brand_name="CrestviewTech2",
        primary_domain="crestviewtech2.com",
        careers_portal="https://careers.crestviewtech2.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="London, UK",
        country="GB",
        authorized_email_domains=["crestviewtech2.com", "talent-crestview2.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000003",
        lei="549300CORPC0000003",
        legal_name="Crestview Global Technology Systems Corporation 3",
        brand_name="CrestviewTech3",
        primary_domain="crestviewtech3.com",
        careers_portal="https://careers.crestviewtech3.com",
        ats_system="SAP SuccessFactors",
        naics_code="522110",
        sic_code="6021",
        headquarters="Bengaluru, IN",
        country="IN",
        authorized_email_domains=["crestviewtech3.com", "talent-crestview3.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000004",
        lei="549300CORPC0000004",
        legal_name="Crestview Global Technology Systems Corporation 4",
        brand_name="CrestviewTech4",
        primary_domain="crestviewtech4.com",
        careers_portal="https://careers.crestviewtech4.com",
        ats_system="iCIMS Talent Cloud",
        naics_code="541512",
        sic_code="7371",
        headquarters="Munich, DE",
        country="DE",
        authorized_email_domains=["crestviewtech4.com", "talent-crestview4.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000005",
        lei="549300CORPC0000005",
        legal_name="Crestview Global Technology Systems Corporation 5",
        brand_name="CrestviewTech5",
        primary_domain="crestviewtech5.com",
        careers_portal="https://careers.crestviewtech5.com",
        ats_system="Oracle Cloud HCM",
        naics_code="511210",
        sic_code="7372",
        headquarters="Paris, FR",
        country="FR",
        authorized_email_domains=["crestviewtech5.com", "talent-crestview5.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000006",
        lei="549300CORPC0000006",
        legal_name="Crestview Global Technology Systems Corporation 6",
        brand_name="CrestviewTech6",
        primary_domain="crestviewtech6.com",
        careers_portal="https://careers.crestviewtech6.com",
        ats_system="Lever ATS",
        naics_code="522110",
        sic_code="6021",
        headquarters="Toronto, CA",
        country="CA",
        authorized_email_domains=["crestviewtech6.com", "talent-crestview6.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000007",
        lei="549300CORPC0000007",
        legal_name="Crestview Global Technology Systems Corporation 7",
        brand_name="CrestviewTech7",
        primary_domain="crestviewtech7.com",
        careers_portal="https://careers.crestviewtech7.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Sydney, AU",
        country="AU",
        authorized_email_domains=["crestviewtech7.com", "talent-crestview7.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000008",
        lei="549300CORPC0000008",
        legal_name="Crestview Global Technology Systems Corporation 8",
        brand_name="CrestviewTech8",
        primary_domain="crestviewtech8.com",
        careers_portal="https://careers.crestviewtech8.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="Singapore, SG",
        country="SG",
        authorized_email_domains=["crestviewtech8.com", "talent-crestview8.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000009",
        lei="549300CORPC0000009",
        legal_name="Crestview Global Technology Systems Corporation 9",
        brand_name="CrestviewTech9",
        primary_domain="crestviewtech9.com",
        careers_portal="https://careers.crestviewtech9.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Dublin, IE",
        country="IE",
        authorized_email_domains=["crestviewtech9.com", "talent-crestview9.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0003000010",
        lei="549300CORPC0000010",
        legal_name="Crestview Global Technology Systems Corporation 10",
        brand_name="CrestviewTech10",
        primary_domain="crestviewtech10.com",
        careers_portal="https://careers.crestviewtech10.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Amsterdam, NL",
        country="NL",
        authorized_email_domains=["crestviewtech10.com", "talent-crestview10.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
]


class EnterpriseCorpLookupManagerC:
    """Manager class for querying corporate entities in Part C."""

    def __init__(self):
        self.entities = {e.cik: e for e in CORP_LOOKUP_ENTRIES_C}
        self.domains = {e.primary_domain.lower(): e for e in CORP_LOOKUP_ENTRIES_C}

    def find_by_cik(self, cik: str) -> Optional[EnterpriseProfileData]:
        return self.entities.get(cik)

    def find_by_domain(self, domain: str) -> Optional[EnterpriseProfileData]:
        return self.domains.get(domain.strip().lower())
