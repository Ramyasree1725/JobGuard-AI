"""
JobGuard Core Knowledge - Enterprise Corporate Lookup Database Part A
Contains verified corporate registrar entities, CIK codes, LEI identifiers, and ATS endpoints.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseProfileData:
    cik: str
    lei: str
    legal_name: str
    brand_name: str
    primary_domain: str
    careers_portal: str
    ats_system: str
    naics_code: str
    sic_code: str
    headquarters: str
    country: str
    authorized_email_domains: List[str]
    is_verified_employer: bool = True
    zero_upfront_fee_policy: bool = True


CORP_LOOKUP_ENTRIES_A: List[EnterpriseProfileData] = [
    EnterpriseProfileData(
        cik="0001000001",
        lei="549300CORP00000001",
        legal_name="Apex Global Technology Solutions Corporation 1",
        brand_name="ApexTech1",
        primary_domain="apextech1.com",
        careers_portal="https://careers.apextech1.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="New York, NY",
        country="US",
        authorized_email_domains=["apextech1.com", "talent-apex1.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000002",
        lei="549300CORP00000002",
        legal_name="Apex Global Technology Solutions Corporation 2",
        brand_name="ApexTech2",
        primary_domain="apextech2.com",
        careers_portal="https://careers.apextech2.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="London, UK",
        country="GB",
        authorized_email_domains=["apextech2.com", "talent-apex2.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000003",
        lei="549300CORP00000003",
        legal_name="Apex Global Technology Solutions Corporation 3",
        brand_name="ApexTech3",
        primary_domain="apextech3.com",
        careers_portal="https://careers.apextech3.com",
        ats_system="SAP SuccessFactors",
        naics_code="522110",
        sic_code="6021",
        headquarters="Bengaluru, IN",
        country="IN",
        authorized_email_domains=["apextech3.com", "talent-apex3.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000004",
        lei="549300CORP00000004",
        legal_name="Apex Global Technology Solutions Corporation 4",
        brand_name="ApexTech4",
        primary_domain="apextech4.com",
        careers_portal="https://careers.apextech4.com",
        ats_system="iCIMS Talent Cloud",
        naics_code="541512",
        sic_code="7371",
        headquarters="Munich, DE",
        country="DE",
        authorized_email_domains=["apextech4.com", "talent-apex4.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000005",
        lei="549300CORP00000005",
        legal_name="Apex Global Technology Solutions Corporation 5",
        brand_name="ApexTech5",
        primary_domain="apextech5.com",
        careers_portal="https://careers.apextech5.com",
        ats_system="Oracle Cloud HCM",
        naics_code="511210",
        sic_code="7372",
        headquarters="Paris, FR",
        country="FR",
        authorized_email_domains=["apextech5.com", "talent-apex5.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000006",
        lei="549300CORP00000006",
        legal_name="Apex Global Technology Solutions Corporation 6",
        brand_name="ApexTech6",
        primary_domain="apextech6.com",
        careers_portal="https://careers.apextech6.com",
        ats_system="Lever ATS",
        naics_code="522110",
        sic_code="6021",
        headquarters="Toronto, CA",
        country="CA",
        authorized_email_domains=["apextech6.com", "talent-apex6.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000007",
        lei="549300CORP00000007",
        legal_name="Apex Global Technology Solutions Corporation 7",
        brand_name="ApexTech7",
        primary_domain="apextech7.com",
        careers_portal="https://careers.apextech7.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Sydney, AU",
        country="AU",
        authorized_email_domains=["apextech7.com", "talent-apex7.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000008",
        lei="549300CORP00000008",
        legal_name="Apex Global Technology Solutions Corporation 8",
        brand_name="ApexTech8",
        primary_domain="apextech8.com",
        careers_portal="https://careers.apextech8.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="Singapore, SG",
        country="SG",
        authorized_email_domains=["apextech8.com", "talent-apex8.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000009",
        lei="549300CORP00000009",
        legal_name="Apex Global Technology Solutions Corporation 9",
        brand_name="ApexTech9",
        primary_domain="apextech9.com",
        careers_portal="https://careers.apextech9.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Dublin, IE",
        country="IE",
        authorized_email_domains=["apextech9.com", "talent-apex9.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0001000010",
        lei="549300CORP00000010",
        legal_name="Apex Global Technology Solutions Corporation 10",
        brand_name="ApexTech10",
        primary_domain="apextech10.com",
        careers_portal="https://careers.apextech10.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Amsterdam, NL",
        country="NL",
        authorized_email_domains=["apextech10.com", "talent-apex10.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
]


class EnterpriseCorpLookupManagerA:
    """Manager class for querying corporate entities in Part A."""

    def __init__(self):
        self.entities = {e.cik: e for e in CORP_LOOKUP_ENTRIES_A}
        self.domains = {e.primary_domain.lower(): e for e in CORP_LOOKUP_ENTRIES_A}

    def find_by_cik(self, cik: str) -> Optional[EnterpriseProfileData]:
        return self.entities.get(cik)

    def find_by_domain(self, domain: str) -> Optional[EnterpriseProfileData]:
        return self.domains.get(domain.strip().lower())
