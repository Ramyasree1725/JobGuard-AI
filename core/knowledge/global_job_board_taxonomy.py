"""
JobGuard Core Knowledge - Global Job Board & ATS Taxonomy
Provides comprehensive structural mappings, authentic ATS platform signatures,
webhook ingestion protocols, and legitimate career endpoint routing schemas.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import urllib.parse


class JobPlatformCategory(Enum):
    ENTERPRISE_ATS = "ENTERPRISE_ATS"
    AGGREGATOR = "AGGREGATOR"
    PROFESSIONAL_NETWORK = "PROFESSIONAL_NETWORK"
    NICHE_TECH = "NICHE_TECH"
    FREELANCE_MARKETPLACE = "FREELANCE_MARKETPLACE"
    CLASSIFIED_BOARD = "CLASSIFIED_BOARD"
    UNVERIFIED_SOURCE = "UNVERIFIED_SOURCE"


class VerificationStatus(Enum):
    OFFICIAL_VERIFIED = "OFFICIAL_VERIFIED"
    COMMUNITY_MONITORED = "COMMUNITY_MONITORED"
    HIGH_FRAUD_INCIDENCE = "HIGH_FRAUD_INCIDENCE"
    BLOCKED = "BLOCKED"


@dataclass
class JobBoardProfile:
    platform_name: str
    category: JobPlatformCategory
    primary_domain: str
    supported_ats_subdomains: List[str]
    verification_status: VerificationStatus
    requires_auth_for_application: bool
    anti_fraud_measures: List[str]
    api_endpoint_patterns: List[str]
    risk_multiplier: float  # 0.1 (extremely safe) to 2.5 (high scam incidence)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EndpointAnalysisResult:
    original_url: str
    canonical_domain: str
    identified_platform: Optional[JobBoardProfile]
    is_authentic_ats: bool
    is_legitimate_routing: bool
    risk_score: float
    recommendations: List[str]
    extracted_job_id: Optional[str] = None


class GlobalJobBoardTaxonomy:
    """Enterprise taxonomy and URL validation engine for global job boards and ATS platforms."""

    def __init__(self):
        self.platforms: Dict[str, JobBoardProfile] = {}
        self.ats_signature_map: Dict[str, JobBoardProfile] = {}
        self._initialize_taxonomy()

    def _initialize_taxonomy(self) -> None:
        """Register the authoritative taxonomy of global job platforms and ATS suites."""
        
        # Enterprise ATS Systems
        greenhouse = JobBoardProfile(
            platform_name="Greenhouse",
            category=JobPlatformCategory.ENTERPRISE_ATS,
            primary_domain="greenhouse.io",
            supported_ats_subdomains=["boards.greenhouse.io", "job-boards.greenhouse.io", "api.greenhouse.io"],
            verification_status=VerificationStatus.OFFICIAL_VERIFIED,
            requires_auth_for_application=False,
            anti_fraud_measures=["Domain verification", "Custom DKIM/SPF integration", "SSO integration"],
            api_endpoint_patterns=[r"^https?://boards\.greenhouse\.io/[a-zA-Z0-9_\-]+/jobs/\d+"],
            risk_multiplier=0.15,
            metadata={"ats_type": "hosted_enterprise", "standard_auth": "oauth2"}
        )
        self.platforms["greenhouse"] = greenhouse
        for sub in greenhouse.supported_ats_subdomains:
            self.ats_signature_map[sub] = greenhouse

        lever = JobBoardProfile(
            platform_name="Lever",
            category=JobPlatformCategory.ENTERPRISE_ATS,
            primary_domain="lever.co",
            supported_ats_subdomains=["jobs.lever.co", "api.lever.co"],
            verification_status=VerificationStatus.OFFICIAL_VERIFIED,
            requires_auth_for_application=False,
            anti_fraud_measures=["CSRF tokens", "Automated spam filtering", "Domain key signing"],
            api_endpoint_patterns=[r"^https?://jobs\.lever\.co/[a-zA-Z0-9_\-]+/[a-f0-9\-]+"],
            risk_multiplier=0.15,
            metadata={"ats_type": "hosted_enterprise", "standard_auth": "oauth2"}
        )
        self.platforms["lever"] = lever
        for sub in lever.supported_ats_subdomains:
            self.ats_signature_map[sub] = lever

        workday = JobBoardProfile(
            platform_name="Workday",
            category=JobPlatformCategory.ENTERPRISE_ATS,
            primary_domain="myworkdayjobs.com",
            supported_ats_subdomains=["*.myworkdayjobs.com", "wd3.myworkday.com", "wd5.myworkday.com"],
            verification_status=VerificationStatus.OFFICIAL_VERIFIED,
            requires_auth_for_application=True,
            anti_fraud_measures=["Enterprise SAML/SSO", "Dedicated tenant isolation", "Multi-factor authentication"],
            api_endpoint_patterns=[r"^https?://[a-zA-Z0-9_\-]+\.myworkdayjobs\.com/.*"],
            risk_multiplier=0.10,
            metadata={"ats_type": "tenant_isolated_enterprise"}
        )
        self.platforms["workday"] = workday
        self.ats_signature_map["myworkdayjobs.com"] = workday

        smartrecruiters = JobBoardProfile(
            platform_name="SmartRecruiters",
            category=JobPlatformCategory.ENTERPRISE_ATS,
            primary_domain="smartrecruiters.com",
            supported_ats_subdomains=["jobs.smartrecruiters.com", "api.smartrecruiters.com"],
            verification_status=VerificationStatus.OFFICIAL_VERIFIED,
            requires_auth_for_application=False,
            anti_fraud_measures=["Recruiter verification badge", "Company profile attestation"],
            api_endpoint_patterns=[r"^https?://jobs\.smartrecruiters\.com/[a-zA-Z0-9_\-]+/.*"],
            risk_multiplier=0.20
        )
        self.platforms["smartrecruiters"] = smartrecruiters
        for sub in smartrecruiters.supported_ats_subdomains:
            self.ats_signature_map[sub] = smartrecruiters

        ashby = JobBoardProfile(
            platform_name="Ashby",
            category=JobPlatformCategory.ENTERPRISE_ATS,
            primary_domain="ashbyhq.com",
            supported_ats_subdomains=["jobs.ashbyhq.com"],
            verification_status=VerificationStatus.OFFICIAL_VERIFIED,
            requires_auth_for_application=False,
            anti_fraud_measures=["API key rate limits", "Cryptographic origin proof"],
            api_endpoint_patterns=[r"^https?://jobs\.ashbyhq\.com/[a-zA-Z0-9_\-]+/.*"],
            risk_multiplier=0.15
        )
        self.platforms["ashby"] = ashby
        self.ats_signature_map["jobs.ashbyhq.com"] = ashby

        # Major Job Aggregators & Professional Networks
        linkedin = JobBoardProfile(
            platform_name="LinkedIn",
            category=JobPlatformCategory.PROFESSIONAL_NETWORK,
            primary_domain="linkedin.com",
            supported_ats_subdomains=["www.linkedin.com/jobs"],
            verification_status=VerificationStatus.COMMUNITY_MONITORED,
            requires_auth_for_application=True,
            anti_fraud_measures=["Company page verification", "Recruiter inMail limits", "Verified employer badge"],
            api_endpoint_patterns=[r"^https?://(www\.)?linkedin\.com/jobs/view/\d+"],
            risk_multiplier=0.45
        )
        self.platforms["linkedin"] = linkedin

        indeed = JobBoardProfile(
            platform_name="Indeed",
            category=JobPlatformCategory.AGGREGATOR,
            primary_domain="indeed.com",
            supported_ats_subdomains=["www.indeed.com"],
            verification_status=VerificationStatus.COMMUNITY_MONITORED,
            requires_auth_for_application=False,
            anti_fraud_measures=["Automated job post heuristic review", "Company claim protocol"],
            api_endpoint_patterns=[r"^https?://(www\.)?indeed\.com/viewjob.*"],
            risk_multiplier=0.55
        )
        self.platforms["indeed"] = indeed

        # High Fraud Incidence Sources (Free classifieds, unmoderated boards)
        craigslist = JobBoardProfile(
            platform_name="Craigslist",
            category=JobPlatformCategory.CLASSIFIED_BOARD,
            primary_domain="craigslist.org",
            supported_ats_subdomains=["*.craigslist.org"],
            verification_status=VerificationStatus.HIGH_FRAUD_INCIDENCE,
            requires_auth_for_application=False,
            anti_fraud_measures=["Basic phone verification", "Post flagging"],
            api_endpoint_patterns=[r"^https?://[a-zA-Z0-9_\-]+\.craigslist\.org/.*"],
            risk_multiplier=2.20,
            metadata={"advisory": "High prevalence of fake check and upfront fee scams."}
        )
        self.platforms["craigslist"] = craigslist

        telegram_jobs = JobBoardProfile(
            platform_name="Telegram Channels",
            category=JobPlatformCategory.UNVERIFIED_SOURCE,
            primary_domain="t.me",
            supported_ats_subdomains=["t.me", "telegram.me"],
            verification_status=VerificationStatus.HIGH_FRAUD_INCIDENCE,
            requires_auth_for_application=False,
            anti_fraud_measures=[],
            api_endpoint_patterns=[r"^https?://t\.me/.*"],
            risk_multiplier=2.80,
            metadata={"advisory": "Extremely high risk. Real companies rarely recruit solely through Telegram channels."}
        )
        self.platforms["telegram"] = telegram_jobs

    def evaluate_url(self, url: str) -> EndpointAnalysisResult:
        """Parses and cross-references a job application URL against known ATS signatures."""
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc.lower()

        # Strip standard port if present
        if ":" in netloc:
            netloc = netloc.split(":")[0]

        matched_platform: Optional[JobBoardProfile] = None
        is_authentic_ats = False

        # Direct domain match or wildcard match
        for domain, profile in self.ats_signature_map.items():
            if domain.startswith("*."):
                suffix = domain[2:]
                if netloc.endswith(suffix):
                    matched_platform = profile
                    is_authentic_ats = (profile.category == JobPlatformCategory.ENTERPRISE_ATS)
                    break
            elif netloc == domain or netloc.endswith("." + domain):
                matched_platform = profile
                is_authentic_ats = (profile.category == JobPlatformCategory.ENTERPRISE_ATS)
                break

        if not matched_platform:
            # Check general platforms
            for key, profile in self.platforms.items():
                if profile.primary_domain in netloc:
                    matched_platform = profile
                    is_authentic_ats = (profile.category == JobPlatformCategory.ENTERPRISE_ATS)
                    break

        recommendations: List[str] = []
        if matched_platform:
            risk_score = 15.0 * matched_platform.risk_multiplier
            if matched_platform.verification_status == VerificationStatus.HIGH_FRAUD_INCIDENCE:
                risk_score = 85.0
                recommendations.append(f"Caution: Platform '{matched_platform.platform_name}' has a high incidence of unvetted job listings.")
            elif matched_platform.verification_status == VerificationStatus.OFFICIAL_VERIFIED:
                recommendations.append(f"Authentic applicant tracking endpoint verified on {matched_platform.platform_name}.")
            else:
                recommendations.append(f"Standard public aggregator ({matched_platform.platform_name}). Verify recruiter identity independently.")
        else:
            # Unknown / custom domain
            risk_score = 45.0
            recommendations.append("Custom or uncataloged domain. Verify SSL certificate and official company website before submitting personal data.")

        # Extract potential job ID
        extracted_id = self._extract_job_id(url, matched_platform)

        return EndpointAnalysisResult(
            original_url=url,
            canonical_domain=netloc,
            identified_platform=matched_platform,
            is_authentic_ats=is_authentic_ats,
            is_legitimate_routing=True if matched_platform else False,
            risk_score=min(100.0, max(0.0, risk_score)),
            recommendations=recommendations,
            extracted_job_id=extracted_id
        )

    def _extract_job_id(self, url: str, platform: Optional[JobBoardProfile]) -> Optional[str]:
        """Extracts job listing identifier using platform-specific regex patterns."""
        if not platform:
            return None
        for pattern in platform.api_endpoint_patterns:
            match = re.search(pattern, url)
            if match:
                parts = url.rstrip("/").split("/")
                return parts[-1] if parts else None
        return None

    def get_supported_ats_list(self) -> List[str]:
        """Returns all enterprise ATS platforms recognized by the system."""
        return [
            name for name, profile in self.platforms.items()
            if profile.category == JobPlatformCategory.ENTERPRISE_ATS
        ]
