"""
JobGuard Core Knowledge - Enterprise Corporate Entities Large Database
Contains extensive corporate entity definitions and verified careers URLs.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseProfileLarge:
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


def build_enterprise_large_catalog() -> Dict[str, EnterpriseProfileLarge]:
    catalog: Dict[str, EnterpriseProfileLarge] = {}
    
    # 1
    catalog["0003000001"] = EnterpriseProfileLarge(
        cik="0003000001",
        lei="549300LARGE0000001",
        legal_name="Global Enterprise Technology Group 1",
        brand_name="GlobalTech1",
        primary_domain="globaltech1.com",
        careers_portal="https://careers.globaltech1.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="New York, NY",
        country="US",
        authorized_email_domains=["globaltech1.com", "talent-gt1.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 2
    catalog["0003000002"] = EnterpriseProfileLarge(
        cik="0003000002",
        lei="549300LARGE0000002",
        legal_name="Global Enterprise Technology Group 2",
        brand_name="GlobalTech2",
        primary_domain="globaltech2.com",
        careers_portal="https://careers.globaltech2.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="London, UK",
        country="GB",
        authorized_email_domains=["globaltech2.com", "talent-gt2.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 3
    catalog["0003000003"] = EnterpriseProfileLarge(
        cik="0003000003",
        lei="549300LARGE0000003",
        legal_name="Global Enterprise Technology Group 3",
        brand_name="GlobalTech3",
        primary_domain="globaltech3.com",
        careers_portal="https://careers.globaltech3.com",
        ats_system="SAP SuccessFactors",
        naics_code="522110",
        sic_code="6021",
        headquarters="Bengaluru, IN",
        country="IN",
        authorized_email_domains=["globaltech3.com", "talent-gt3.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 4
    catalog["0003000004"] = EnterpriseProfileLarge(
        cik="0003000004",
        lei="549300LARGE0000004",
        legal_name="Global Enterprise Technology Group 4",
        brand_name="GlobalTech4",
        primary_domain="globaltech4.com",
        careers_portal="https://careers.globaltech4.com",
        ats_system="iCIMS Talent Cloud",
        naics_code="541512",
        sic_code="7371",
        headquarters="Munich, DE",
        country="DE",
        authorized_email_domains=["globaltech4.com", "talent-gt4.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 5
    catalog["0003000005"] = EnterpriseProfileLarge(
        cik="0003000005",
        lei="549300LARGE0000005",
        legal_name="Global Enterprise Technology Group 5",
        brand_name="GlobalTech5",
        primary_domain="globaltech5.com",
        careers_portal="https://careers.globaltech5.com",
        ats_system="Oracle Cloud HCM",
        naics_code="511210",
        sic_code="7372",
        headquarters="Paris, FR",
        country="FR",
        authorized_email_domains=["globaltech5.com", "talent-gt5.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 6
    catalog["0003000006"] = EnterpriseProfileLarge(
        cik="0003000006",
        lei="549300LARGE0000006",
        legal_name="Global Enterprise Technology Group 6",
        brand_name="GlobalTech6",
        primary_domain="globaltech6.com",
        careers_portal="https://careers.globaltech6.com",
        ats_system="Lever ATS",
        naics_code="522110",
        sic_code="6021",
        headquarters="Toronto, CA",
        country="CA",
        authorized_email_domains=["globaltech6.com", "talent-gt6.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 7
    catalog["0003000007"] = EnterpriseProfileLarge(
        cik="0003000007",
        lei="549300LARGE0000007",
        legal_name="Global Enterprise Technology Group 7",
        brand_name="GlobalTech7",
        primary_domain="globaltech7.com",
        careers_portal="https://careers.globaltech7.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Sydney, AU",
        country="AU",
        authorized_email_domains=["globaltech7.com", "talent-gt7.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 8
    catalog["0003000008"] = EnterpriseProfileLarge(
        cik="0003000008",
        lei="549300LARGE0000008",
        legal_name="Global Enterprise Technology Group 8",
        brand_name="GlobalTech8",
        primary_domain="globaltech8.com",
        careers_portal="https://careers.globaltech8.com",
        ats_system="Greenhouse Software",
        naics_code="511210",
        sic_code="7372",
        headquarters="Singapore, SG",
        country="SG",
        authorized_email_domains=["globaltech8.com", "talent-gt8.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 9
    catalog["0003000009"] = EnterpriseProfileLarge(
        cik="0003000009",
        lei="549300LARGE0000009",
        legal_name="Global Enterprise Technology Group 9",
        brand_name="GlobalTech9",
        primary_domain="globaltech9.com",
        careers_portal="https://careers.globaltech9.com",
        ats_system="Workday HCM",
        naics_code="522110",
        sic_code="6021",
        headquarters="Dublin, IE",
        country="IE",
        authorized_email_domains=["globaltech9.com", "talent-gt9.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )
    # 10
    catalog["0003000010"] = EnterpriseProfileLarge(
        cik="0003000010",
        lei="549300LARGE0000010",
        legal_name="Global Enterprise Technology Group 10",
        brand_name="GlobalTech10",
        primary_domain="globaltech10.com",
        careers_portal="https://careers.globaltech10.com",
        ats_system="Workday HCM",
        naics_code="541512",
        sic_code="7371",
        headquarters="Amsterdam, NL",
        country="NL",
        authorized_email_domains=["globaltech10.com", "talent-gt10.com"],
        is_verified_employer=True,
        zero_upfront_fee_policy=True
    )

    return catalog


class EnterpriseLargeManager:
    def __init__(self):
        self.catalog = build_enterprise_large_catalog()

    def get_by_cik(self, cik: str) -> Optional[EnterpriseProfileLarge]:
        return self.catalog.get(cik)
