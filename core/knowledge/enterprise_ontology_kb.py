"""
JobGuard Core Knowledge - Enterprise Domain Taxonomy & Corporate Knowledge Base
Comprehensive catalog of corporate entity taxonomies, verified employer registrar patterns,
NAICS industry classification codes, and trademark validation rules.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CorporateEntityDefinition:
    cik_number: str
    official_legal_name: str
    primary_domain: str
    verified_careers_url: str
    authorized_ats_providers: List[str]  # e.g., ["workday", "greenhouse", "lever"]
    naics_code: str
    headquarters_country: str
    registered_domains: List[str]
    email_domain_patterns: List[str]
    disallowed_contact_channels: List[str] = field(default_factory=lambda: ["telegram", "whatsapp_cold", "free_webmail"])


class EnterpriseOntologyKB:
    """Enterprise Knowledge Base covering Fortune Global employers and authorized hiring channels."""

    def __init__(self):
        self._entities_by_domain: Dict[str, CorporateEntityDefinition] = {}
        self._entities_by_name: Dict[str, CorporateEntityDefinition] = {}
        self._industry_naics_map: Dict[str, str] = {}
        self._populate_enterprise_catalog()

    def register_corporate_entity(self, entity: CorporateEntityDefinition) -> None:
        self._entities_by_domain[entity.primary_domain.lower()] = entity
        self._entities_by_name[entity.official_legal_name.lower()] = entity
        for d in entity.registered_domains:
            self._entities_by_domain[d.lower()] = entity

    def _populate_enterprise_catalog(self) -> None:
        """Populate corporate knowledge database across major industries."""
        corporations = [
            CorporateEntityDefinition(
                cik_number="0001652044",
                official_legal_name="Alphabet Inc.",
                primary_domain="google.com",
                verified_careers_url="https://careers.google.com",
                authorized_ats_providers=["google_internal_ats"],
                naics_code="518210",  # Computing Infrastructure & Data Processing
                headquarters_country="US",
                registered_domains=["google.com", "alphabet.com", "deepmind.com", "youtube.com", "waymo.com"],
                email_domain_patterns=["@google.com", "@alphabet.com", "@googlemail.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001018724",
                official_legal_name="Amazon.com, Inc.",
                primary_domain="amazon.com",
                verified_careers_url="https://amazon.jobs",
                authorized_ats_providers=["amazon_jobs_internal", "icims"],
                naics_code="454110",  # Electronic Shopping & Mail-Order
                headquarters_country="US",
                registered_domains=["amazon.com", "amazon.jobs", "aws.amazon.com", "audible.com", "twitch.tv"],
                email_domain_patterns=["@amazon.com", "@amazon.jobs", "@aws.amazon.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0000789019",
                official_legal_name="Microsoft Corporation",
                primary_domain="microsoft.com",
                verified_careers_url="https://careers.microsoft.com",
                authorized_ats_providers=["microsoft_careers", "successfactors"],
                naics_code="511210",  # Software Publishers
                headquarters_country="US",
                registered_domains=["microsoft.com", "linkedin.com", "github.com", "xbox.com", "skype.com"],
                email_domain_patterns=["@microsoft.com", "@linkedin.com", "@github.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0000320193",
                official_legal_name="Apple Inc.",
                primary_domain="apple.com",
                verified_careers_url="https://jobs.apple.com",
                authorized_ats_providers=["apple_jobs_internal"],
                naics_code="334111",  # Electronic Computer Manufacturing
                headquarters_country="US",
                registered_domains=["apple.com", "beats.com", "icloud.com"],
                email_domain_patterns=["@apple.com", "@group.apple.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001326801",
                official_legal_name="Meta Platforms, Inc.",
                primary_domain="meta.com",
                verified_careers_url="https://metacareers.com",
                authorized_ats_providers=["meta_internal_ats"],
                naics_code="519130",  # Internet Publishing & Web Search
                headquarters_country="US",
                registered_domains=["meta.com", "metacareers.com", "facebook.com", "instagram.com", "whatsapp.com"],
                email_domain_patterns=["@meta.com", "@fb.com", "@instagram.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001065280",
                official_legal_name="Netflix, Inc.",
                primary_domain="netflix.com",
                verified_careers_url="https://jobs.netflix.com",
                authorized_ats_providers=["greenhouse", "workday"],
                naics_code="512120",  # Motion Picture & Video Distribution
                headquarters_country="US",
                registered_domains=["netflix.com", "jobs.netflix.com"],
                email_domain_patterns=["@netflix.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001108524",
                official_legal_name="Salesforce, Inc.",
                primary_domain="salesforce.com",
                verified_careers_url="https://salesforce.com/company/careers",
                authorized_ats_providers=["workday", "smartrecruiters"],
                naics_code="511210",
                headquarters_country="US",
                registered_domains=["salesforce.com", "slack.com", "tableau.com", "mulesoft.com"],
                email_domain_patterns=["@salesforce.com", "@slack-corp.com", "@tableau.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001048286",
                official_legal_name="FedEx Corporation",
                primary_domain="fedex.com",
                verified_careers_url="https://careers.fedex.com",
                authorized_ats_providers=["workday", "taleo"],
                naics_code="492110",  # Couriers & Express Delivery
                headquarters_country="US",
                registered_domains=["fedex.com", "fedex.jobs", "careers.fedex.com"],
                email_domain_patterns=["@fedex.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0000036000",
                official_legal_name="Infosys Limited",
                primary_domain="infosys.com",
                verified_careers_url="https://career.infosys.com",
                authorized_ats_providers=["successfactors", "infosys_internal"],
                naics_code="541512",  # Computer Systems Design Services
                headquarters_country="IN",
                registered_domains=["infosys.com", "infosysbpm.com", "career.infosys.com"],
                email_domain_patterns=["@infosys.com", "@infosysbpm.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001108525",
                official_legal_name="Tata Consultancy Services Ltd",
                primary_domain="tcs.com",
                verified_careers_url="https://tcs.com/careers",
                authorized_ats_providers=["tcs_ibegin", "tcs_nextstep"],
                naics_code="541512",
                headquarters_country="IN",
                registered_domains=["tcs.com", "tcsion.com", "tataconsultancy.com"],
                email_domain_patterns=["@tcs.com", "@tcsion.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0001467373",
                official_legal_name="Accenture plc",
                primary_domain="accenture.com",
                verified_careers_url="https://accenture.com/careers",
                authorized_ats_providers=["workday", "taleo"],
                naics_code="541611",  # Management Consulting Services
                headquarters_country="IE",
                registered_domains=["accenture.com", "careers.accenture.com"],
                email_domain_patterns=["@accenture.com"]
            ),
            CorporateEntityDefinition(
                cik_number="0000051143",
                official_legal_name="International Business Machines Corp",
                primary_domain="ibm.com",
                verified_careers_url="https://ibm.com/employment",
                authorized_ats_providers=["brassring", "kenexa", "workday"],
                naics_code="541512",
                headquarters_country="US",
                registered_domains=["ibm.com", "redhat.com"],
                email_domain_patterns=["@ibm.com", "@redhat.com", "@us.ibm.com"]
            )
        ]

        for corp in corporations:
            self.register_corporate_entity(corp)

    def lookup_domain(self, domain: str) -> Optional[CorporateEntityDefinition]:
        return self._entities_by_domain.get(domain.strip().lower())

    def verify_recruiter_email(self, alleged_company_name: str, email_address: str) -> Tuple[bool, str]:
        """Verify if recruiter email matches authorized domain patterns for the alleged employer."""
        clean_name = alleged_company_name.strip().lower()
        clean_email = email_address.strip().lower()

        if "@" not in clean_email:
            return False, "Malformed email address structure"

        email_domain = clean_email.split("@")[1]

        # Free webmail check
        if email_domain in {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"}:
            return False, f"Free public webmail provider (@{email_domain}) used for alleged corporate recruiter"

        # Search matching entity
        matched_entity = None
        for name, entity in self._entities_by_name.items():
            if name in clean_name or clean_name in name:
                matched_entity = entity
                break

        if not matched_entity:
            # Look up domain directly
            matched_entity = self._entities_by_domain.get(email_domain)

        if matched_entity:
            # Check domain match
            if any(email_domain == d or email_domain.endswith("." + d) for d in matched_entity.registered_domains):
                return True, f"Verified authorized recruiter domain for {matched_entity.official_legal_name}"
            else:
                return False, f"Domain mismatch: '{email_domain}' is not an authorized domain for {matched_entity.official_legal_name}"

        return True, "Unregistered / mid-market corporate domain (proceed with standard verification)"
