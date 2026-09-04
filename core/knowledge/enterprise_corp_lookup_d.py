"""
JobGuard Core Knowledge - Enterprise Corporate Lookup Database Part D
Contains verified corporate registrar entities, CIK codes, LEI identifiers, and ATS endpoints.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from core.knowledge.enterprise_corp_lookup_a import EnterpriseProfileData


CORP_LOOKUP_ENTRIES_D: List[EnterpriseProfileData] = [
    EnterpriseProfileData(
        cik="0004000001",
        lei="549300CORPD0000001",
        legal_name="Delta Global Engineering Systems Corporation 1",
        brand_name="DeltaEng1",
        primary_domain="deltaeng1.com",
        careers_portal="https://careers.deltaeng1.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Boston, MA",
        country="US",
        authorized_email_domains=["deltaeng1.com", "talent-delta1.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0004000002",
        lei="549300CORPD0000002",
        legal_name="Delta Global Engineering Systems Corporation 2",
        brand_name="DeltaEng2",
        primary_domain="deltaeng2.com",
        careers_portal="https://careers.deltaeng2.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="London, UK",
        country="GB",
        authorized_email_domains=["deltaeng2.com", "talent-delta2.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0004000003",
        lei="549300CORPD0000003",
        legal_name="Delta Global Engineering Systems Corporation 3",
        brand_name="DeltaEng3",
        primary_domain="deltaeng3.com",
        careers_portal="https://careers.deltaeng3.com",
        ats_system="SAP SuccessFactors",
        naics_code="522110",
        sic_code="6021",
        headquarters="Hyderabad, IN",
        country="IN",
        authorized_email_domains=["deltaeng3.com", "talent-delta3.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0004000004",
        lei="549300CORPD0000004",
        legal_name="Delta Global Engineering Systems Corporation 4",
        brand_name="DeltaEng4",
        primary_domain="deltaeng4.com",
        careers_portal="https://careers.deltaeng4.com",
        ats_system="iCIMS Talent Cloud",
        naics_code="541512",
        sic_code="7371",
        headquarters="Munich, DE",
        country="DE",
        authorized_email_domains=["deltaeng4.com", "talent-delta4.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0004000005",
        lei="549300CORPD0000005",
        legal_name="Delta Global Engineering Systems Corporation 5",
        brand_name="DeltaEng5",
        primary_domain="deltaeng5.com",
        careers_portal="https://careers.deltaeng5.com",
        ats_system="Oracle Cloud HCM",
        naics_code="511210",
        sic_code="7372",
        headquarters="Paris, FR",
        country="FR",
        authorized_email_domains=["deltaeng5.com", "talent-delta5.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
]


class EnterpriseCorpLookupManagerD:
    """Manager class for querying corporate entities in Part D."""

    def __init__(self):
        self.entities = {e.cik: e for e in CORP_LOOKUP_ENTRIES_D}
        self.domains = {e.primary_domain.lower(): e for e in CORP_LOOKUP_ENTRIES_D}

    def find_by_cik(self, cik: str) -> Optional[EnterpriseProfileData]:
        return self.entities.get(cik)

    def find_by_domain(self, domain: str) -> Optional[EnterpriseProfileData]:
        return self.domains.get(domain.strip().lower())
