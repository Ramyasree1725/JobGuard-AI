"""
JobGuard Core Knowledge - Corporate Entity Registry & Domain Verification Protocols
Maintains authoritative organizational profiles, verified primary root domains,
official career portal endpoints, and impersonation defense configurations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import urllib.parse
import re


@dataclass
class CorporateEntity:
    entity_id: str
    company_name: str
    canonical_root_domain: str
    known_aliases: List[str]
    official_careers_url: str
    verified_recruitment_email_domains: List[str]
    associated_ats: str
    headquarters_country: str
    industry_sector: str
    is_frequently_impersonated: bool
    security_advisory_url: Optional[str] = None
    known_fraudulent_lookalike_domains: List[str] = field(default_factory=list)


@dataclass
class DomainVerificationAudit:
    query_domain: str
    claimed_company: str
    matched_entity: Optional[CorporateEntity]
    is_exact_match: bool
    is_legitimate_subdomain: bool
    is_known_impersonation_domain: bool
    similarity_score: float
    risk_level: str  # 'VERIFIED_SAFE', 'SUSPICIOUS_UNREGISTERED', 'CRITICAL_IMPERSONATION'
    verdict_message: str


class CorporateEntityRegistry:
    """Authoritative registry for verifying legitimate enterprise corporate domains and career channels."""

    def __init__(self):
        self.entities: Dict[str, CorporateEntity] = {}
        self.domain_to_entity_map: Dict[str, CorporateEntity] = {}
        self.lookalike_threat_map: Dict[str, str] = {}  # bad domain -> entity_id
        self._initialize_corporate_catalog()

    def _initialize_corporate_catalog(self) -> None:
        """Register verified global enterprise entities and known lookalike threats."""

        # Google / Alphabet
        google = CorporateEntity(
            entity_id="ENT_GOOGLE",
            company_name="Google LLC",
            canonical_root_domain="google.com",
            known_aliases=["Google", "Alphabet", "Google Inc", "YouTube"],
            official_careers_url="https://www.google.com/about/careers/applications/jobs/results",
            verified_recruitment_email_domains=["google.com", "alphabet.com"],
            associated_ats="Internal ATS",
            headquarters_country="USA",
            industry_sector="Technology",
            is_frequently_impersonated=True,
            security_advisory_url="https://support.google.com/faqs/answer/6328224",
            known_fraudulent_lookalike_domains=[
                "google-careers-portal.com", "google-hiring-desk.net", "googlejobs-online.org",
                "google-talent-remote.com", "alphabet-recruiters.info"
            ]
        )
        self._register_entity(google)

        # Microsoft Corporation
        microsoft = CorporateEntity(
            entity_id="ENT_MICROSOFT",
            company_name="Microsoft Corporation",
            canonical_root_domain="microsoft.com",
            known_aliases=["Microsoft", "MSFT", "LinkedIn", "GitHub"],
            official_careers_url="https://careers.microsoft.com/professionals/us/en",
            verified_recruitment_email_domains=["microsoft.com", "linkedin.com", "github.com"],
            associated_ats="Internal / Dynamics 365",
            headquarters_country="USA",
            industry_sector="Technology",
            is_frequently_impersonated=True,
            security_advisory_url="https://www.microsoft.com/en-us/security",
            known_fraudulent_lookalike_domains=[
                "microsoft-careers-remote.com", "microsoft-recruiting-center.org",
                "msft-hiring-portal.net", "microsoft-teams-interviews.online"
            ]
        )
        self._register_entity(microsoft)

        # Amazon
        amazon = CorporateEntity(
            entity_id="ENT_AMAZON",
            company_name="Amazon.com, Inc.",
            canonical_root_domain="amazon.com",
            known_aliases=["Amazon", "AWS", "Amazon Web Services"],
            official_careers_url="https://www.amazon.jobs/en",
            verified_recruitment_email_domains=["amazon.com", "amazon.jobs"],
            associated_ats="Internal ATS (Amazon.jobs)",
            headquarters_country="USA",
            industry_sector="E-Commerce & Cloud Computing",
            is_frequently_impersonated=True,
            security_advisory_url="https://www.amazon.com/gp/help/customer/display.html?nodeId=G4YFYCCNUSENA23B",
            known_fraudulent_lookalike_domains=[
                "amazon-remote-jobs-apply.com", "aws-hiring-assessment.org",
                "amazon-task-review.net", "amazon-customer-support-hiring.info"
            ]
        )
        self._register_entity(amazon)

        # Apple Inc.
        apple = CorporateEntity(
            entity_id="ENT_APPLE",
            company_name="Apple Inc.",
            canonical_root_domain="apple.com",
            known_aliases=["Apple", "Apple Computers"],
            official_careers_url="https://jobs.apple.com/en-us/search",
            verified_recruitment_email_domains=["apple.com", "email.apple.com"],
            associated_ats="Internal ATS",
            headquarters_country="USA",
            industry_sector="Consumer Electronics & Software",
            is_frequently_impersonated=True,
            security_advisory_url="https://support.apple.com/en-us/HT204759",
            known_fraudulent_lookalike_domains=[
                "apple-careers-remote.org", "apple-job-verification.net", "apple-advisor-apply.info"
            ]
        )
        self._register_entity(apple)

        # Johnson & Johnson
        jnj = CorporateEntity(
            entity_id="ENT_JNJ",
            company_name="Johnson & Johnson",
            canonical_root_domain="jnj.com",
            known_aliases=["J&J", "Johnson and Johnson", "Janssen"],
            official_careers_url="https://www.careers.jnj.com/",
            verified_recruitment_email_domains=["jnj.com", "its.jnj.com"],
            associated_ats="Workday",
            headquarters_country="USA",
            industry_sector="Healthcare & Pharmaceuticals",
            is_frequently_impersonated=True,
            security_advisory_url="https://www.careers.jnj.com/recruitment-fraud-alert",
            known_fraudulent_lookalike_domains=[
                "jnj-careers-hiring.com", "johnson-johnson-remote.net", "jnj-medical-interviews.org"
            ]
        )
        self._register_entity(jnj)

        # Deloitte
        deloitte = CorporateEntity(
            entity_id="ENT_DELOITTE",
            company_name="Deloitte Touche Tohmatsu Limited",
            canonical_root_domain="deloitte.com",
            known_aliases=["Deloitte", "Deloitte Consulting"],
            official_careers_url="https://www.deloitte.com/global/en/careers.html",
            verified_recruitment_email_domains=["deloitte.com", "deloitteresources.com"],
            associated_ats="Taleo / SAP SuccessFactors",
            headquarters_country="United Kingdom",
            industry_sector="Professional Services & Audit",
            is_frequently_impersonated=True,
            security_advisory_url="https://www.deloitte.com/us/en/pages/about-deloitte/articles/fraudulent-job-offers.html",
            known_fraudulent_lookalike_domains=[
                "deloitte-consulting-careers.org", "deloitte-recruiting-us.com", "deloitte-hr-desk.net"
            ]
        )
        self._register_entity(deloitte)

    def _register_entity(self, entity: CorporateEntity) -> None:
        self.entities[entity.entity_id] = entity
        self.domain_to_entity_map[entity.canonical_root_domain.lower()] = entity
        for domain in entity.verified_recruitment_email_domains:
            self.domain_to_entity_map[domain.lower()] = entity
        for bad_domain in entity.known_fraudulent_lookalike_domains:
            self.lookalike_threat_map[bad_domain.lower()] = entity.entity_id

    def verify_recruiter_domain(self, domain_or_email: str, claimed_company_name: str) -> DomainVerificationAudit:
        """Verifies if an email domain matches the official corporate infrastructure of the claimed company."""
        domain = domain_or_email.lower().strip()
        if "@" in domain:
            domain = domain.split("@")[-1]

        # 1. Check known fraud lookalike catalog
        if domain in self.lookalike_threat_map:
            ent_id = self.lookalike_threat_map[domain]
            entity = self.entities.get(ent_id)
            comp_name = entity.company_name if entity else claimed_company_name
            return DomainVerificationAudit(
                query_domain=domain,
                claimed_company=claimed_company_name,
                matched_entity=entity,
                is_exact_match=False,
                is_legitimate_subdomain=False,
                is_known_impersonation_domain=True,
                similarity_score=0.95,
                risk_level="CRITICAL_IMPERSONATION",
                verdict_message=f"CRITICAL: Domain '{domain}' is a confirmed fraudulent lookalike targeting {comp_name}."
            )

        # 2. Find entity by claimed company name
        matched_entity: Optional[CorporateEntity] = None
        for entity in self.entities.values():
            if (claimed_company_name.lower() in entity.company_name.lower() or
                    any(alias.lower() in claimed_company_name.lower() for alias in entity.known_aliases)):
                matched_entity = entity
                break

        if not matched_entity:
            # Check domain direct match
            if domain in self.domain_to_entity_map:
                matched_entity = self.domain_to_entity_map[domain]

        if matched_entity:
            # Check exact or verified subdomain match
            root = matched_entity.canonical_root_domain.lower()
            if domain == root or domain in matched_entity.verified_recruitment_email_domains:
                return DomainVerificationAudit(
                    query_domain=domain,
                    claimed_company=claimed_company_name,
                    matched_entity=matched_entity,
                    is_exact_match=True,
                    is_legitimate_subdomain=False,
                    is_known_impersonation_domain=False,
                    similarity_score=1.0,
                    risk_level="VERIFIED_SAFE",
                    verdict_message=f"VERIFIED: Domain '{domain}' matches official corporate domain for {matched_entity.company_name}."
                )
            
            if domain.endswith("." + root):
                return DomainVerificationAudit(
                    query_domain=domain,
                    claimed_company=claimed_company_name,
                    matched_entity=matched_entity,
                    is_exact_match=False,
                    is_legitimate_subdomain=True,
                    is_known_impersonation_domain=False,
                    similarity_score=0.9,
                    risk_level="VERIFIED_SAFE",
                    verdict_message=f"VERIFIED: '{domain}' is an authentic subdomain of {matched_entity.company_name}."
                )

            # If company matches but domain differs completely
            return DomainVerificationAudit(
                query_domain=domain,
                claimed_company=claimed_company_name,
                matched_entity=matched_entity,
                is_exact_match=False,
                is_legitimate_subdomain=False,
                is_known_impersonation_domain=False,
                similarity_score=self._calculate_levenshtein_similarity(domain, root),
                risk_level="CRITICAL_IMPERSONATION",
                verdict_message=(f"IMPERSONATION ALERT: Recruiter claims {matched_entity.company_name} but sent from '{domain}'. "
                                f"Official domain is '{matched_entity.canonical_root_domain}'.")
            )

        # Uncataloged company/domain
        return DomainVerificationAudit(
            query_domain=domain,
            claimed_company=claimed_company_name,
            matched_entity=None,
            is_exact_match=False,
            is_legitimate_subdomain=False,
            is_known_impersonation_domain=False,
            similarity_score=0.0,
            risk_level="SUSPICIOUS_UNREGISTERED",
            verdict_message=f"UNREGISTERED: '{domain}' is not in authoritative Fortune 500 catalog. Exercise due diligence."
        )

    def _calculate_levenshtein_similarity(self, s1: str, s2: str) -> float:
        """Computes normalized Levenshtein similarity between two strings."""
        if not s1 or not s2:
            return 0.0
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
        distance = dp[m][n]
        max_len = max(m, n)
        return 1.0 - (distance / max_len) if max_len > 0 else 1.0
