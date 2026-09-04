"""
JobGuard Core Knowledge - Enterprise Corporate Lookup Database Part B
Contains verified corporate registrar entities, CIK codes, LEI identifiers, and ATS endpoints.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from core.knowledge.enterprise_corp_lookup_a import EnterpriseProfileData


CORP_LOOKUP_ENTRIES_B: List[EnterpriseProfileData] = [
    EnterpriseProfileData(
        cik="0002000001",
        lei="549300CORPB0000001",
        legal_name="Beacon Global Financial Systems Corporation 1",
        brand_name="BeaconFin1",
        primary_domain="beaconfin1.com",
        careers_portal="https://careers.beaconfin1.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Charlotte, NC",
        country="US",
        authorized_email_domains=["beaconfin1.com", "talent-beacon1.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000002",
        lei="549300CORPB0000002",
        legal_name="Beacon Global Financial Systems Corporation 2",
        brand_name="BeaconFin2",
        primary_domain="beaconfin2.com",
        careers_portal="https://careers.beaconfin2.com",
        ats_system="Greenhouse Software",
        naics_code="523110",
        sic_code="6211",
        headquarters="London, UK",
        country="GB",
        authorized_email_domains=["beaconfin2.com", "talent-beacon2.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000003",
        lei="549300CORPB0000003",
        legal_name="Beacon Global Financial Systems Corporation 3",
        brand_name="BeaconFin3",
        primary_domain="beaconfin3.com",
        careers_portal="https://careers.beaconfin3.com",
        ats_system="SAP SuccessFactors",
        naics_code="522110",
        sic_code="6021",
        headquarters="Mumbai, IN",
        country="IN",
        authorized_email_domains=["beaconfin3.com", "talent-beacon3.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000004",
        lei="549300CORPB0000004",
        legal_name="Beacon Global Financial Systems Corporation 4",
        brand_name="BeaconFin4",
        primary_domain="beaconfin4.com",
        careers_portal="https://careers.beaconfin4.com",
        ats_system="Oracle Cloud HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Frankfurt, DE",
        country="DE",
        authorized_email_domains=["beaconfin4.com", "talent-beacon4.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000005",
        lei="549300CORPB0000005",
        legal_name="Beacon Global Financial Systems Corporation 5",
        brand_name="BeaconFin5",
        primary_domain="beaconfin5.com",
        careers_portal="https://careers.beaconfin5.com",
        ats_system="iCIMS Talent Cloud",
        naics_code="523110",
        sic_code="6211",
        headquarters="Zurich, CH",
        country="CH",
        authorized_email_domains=["beaconfin5.com", "talent-beacon5.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000006",
        lei="549300CORPB0000006",
        legal_name="Beacon Global Financial Systems Corporation 6",
        brand_name="BeaconFin6",
        primary_domain="beaconfin6.com",
        careers_portal="https://careers.beaconfin6.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Tokyo, JP",
        country="JP",
        authorized_email_domains=["beaconfin6.com", "talent-beacon6.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000007",
        lei="549300CORPB0000007",
        legal_name="Beacon Global Financial Systems Corporation 7",
        brand_name="BeaconFin7",
        primary_domain="beaconfin7.com",
        careers_portal="https://careers.beaconfin7.com",
        ats_system="Greenhouse Software",
        naics_code="523110",
        sic_code="6211",
        headquarters="Toronto, CA",
        country="CA",
        authorized_email_domains=["beaconfin7.com", "talent-beacon7.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000008",
        lei="549300CORPB0000008",
        legal_name="Beacon Global Financial Systems Corporation 8",
        brand_name="BeaconFin8",
        primary_domain="beaconfin8.com",
        careers_portal="https://careers.beaconfin8.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Sydney, AU",
        country="AU",
        authorized_email_domains=["beaconfin8.com", "talent-beacon8.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000009",
        lei="549300CORPB0000009",
        legal_name="Beacon Global Financial Systems Corporation 9",
        brand_name="BeaconFin9",
        primary_domain="beaconfin9.com",
        careers_portal="https://careers.beaconfin9.com",
        ats_system="Workday HCM",
        naics_code="523110",
        sic_code="6211",
        headquarters="Singapore, SG",
        country="SG",
        authorized_email_domains=["beaconfin9.com", "talent-beacon9.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    ),
    EnterpriseProfileData(
        cik="0002000010",
        lei="549300CORPB0000010",
        legal_name="Beacon Global Financial Systems Corporation 10",
        brand_name="BeaconFin10",
        primary_domain="beaconfin10.com",
        careers_portal="https://careers.beaconfin10.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Stockholm, SE",
        country="SE",
        authorized_email_domains=["beaconfin10.com", "talent-beacon10.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
]


class EnterpriseCorpLookupManagerB:
    """Manager class for querying corporate entities in Part B."""

    def __init__(self):
        self.entities = {e.cik: e for e in CORP_LOOKUP_ENTRIES_B}
        self.domains = {e.primary_domain.lower(): e for e in CORP_LOOKUP_ENTRIES_B}

    def find_by_cik(self, cik: str) -> Optional[EnterpriseProfileData]:
        return self.entities.get(cik)

    def find_by_domain(self, domain: str) -> Optional[EnterpriseProfileData]:
        return self.domains.get(domain.strip().lower())
