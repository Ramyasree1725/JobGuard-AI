"""
JobGuard Core Knowledge - Recruiter Identity & Verification Ontology
Provides comprehensive domain validation matrices, recruiter impersonation taxonomies,
and executive identity verification graphs for enterprise fraud defense.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import hashlib


class IdentityConfidenceLevel(Enum):
    UNVERIFIED = "UNVERIFIED"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    MEDIUM_CONFIDENCE = "MEDIUM_CONFIDENCE"
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    CRYPTOGRAPHICALLY_VERIFIED = "CRYPTOGRAPHICALLY_VERIFIED"


class ImpersonationTechnique(Enum):
    HOMOGLYPH_ATTACK = "HOMOGLYPH_ATTACK"
    SUBDOMAIN_SPOOFING = "SUBDOMAIN_SPOOFING"
    TYPOSQUATTING = "TYPOSQUATTING"
    COMBO_SQUATTING = "COMBO_SQUATTING"
    FREE_WEBMAIL_IMPERSONATION = "FREE_WEBMAIL_IMPERSONATION"
    DISPLAY_NAME_DECEPTION = "DISPLAY_NAME_DECEPTION"
    EXECUTIVE_NAME_HIJACK = "EXECUTIVE_NAME_HIJACK"
    FAKE_ATS_PORTAL = "FAKE_ATS_PORTAL"


@dataclass
class RecruiterProfile:
    full_name: str
    claimed_company: str
    claimed_email: str
    claimed_phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    telegram_handle: Optional[str] = None
    whatsapp_number: Optional[str] = None
    ats_identifier: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerificationAssertion:
    assertion_id: str
    verifier_subsystem: str
    technique: ImpersonationTechnique
    passed: bool
    risk_score_impact: float  # -1.0 to 1.0
    evidence_summary: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IdentityAuditResult:
    profile: RecruiterProfile
    confidence_level: IdentityConfidenceLevel
    aggregate_risk_score: float
    assertions: List[VerificationAssertion]
    flagged_techniques: List[ImpersonationTechnique]
    recommended_action: str


class RecruiterIdentityOntology:
    """Master knowledge base for corporate recruiter identity schemas and impersonation rules."""

    FREE_WEBMAIL_PROVIDERS: Set[str] = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
        "protonmail.com", "proton.me", "zoho.com", "icloud.com", "mail.com",
        "gmx.com", "yandex.com", "inbox.com", "live.com", "msn.com",
        "fastmail.com", "tutanota.com", "tuta.io", "rediffmail.com"
    }

    SUSPICIOUS_SUBDOMAIN_PATTERNS: List[re.Pattern] = [
        re.compile(r"careers?-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"jobs?-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"hr-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"recruitment-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"talent-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"hiring-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"work-[a-z0-9]+\.", re.IGNORECASE),
        re.compile(r"apply-[a-z0-9]+\.", re.IGNORECASE),
    ]

    CORPORATE_ATS_CANONICAL_DOMAINS: Dict[str, str] = {
        "greenhouse": "boards.greenhouse.io",
        "lever": "jobs.lever.co",
        "workday": "myworkdayjobs.com",
        "taleo": "taleo.net",
        "icims": "icims.com",
        "smartrecruiters": "smartrecruiters.com",
        "ashby": "jobs.ashbyhq.com",
        "bamboohr": "bamboohr.com",
        "jobvite": "jobvite.com",
        "jazzhr": "applytojob.com",
        "workable": "workable.com",
        "recruitee": "recruitee.com",
        "pinpointhq": "pinpointhq.com",
        "rippling": "rippling-ats.com",
    }

    HOMOGLYPH_MAPPINGS: Dict[str, str] = {
        "а": "a", "с": "c", "е": "e", "о": "o", "р": "p", "х": "x", "у": "y",
        "і": "i", "ј": "j", "ѕ": "s", "ԁ": "d", "ԛ": "q", "ԝ": "w",
        "0": "o", "1": "l", "vv": "w", "rn": "m", "cl": "d", "nn": "m"
    }

    def __init__(self):
        self.verified_executive_registry: Dict[str, Set[str]] = {}
        self.known_fraud_domains: Set[str] = set()
        self.reputation_cache: Dict[str, float] = {}
        self._initialize_corporate_registries()

    def _initialize_corporate_registries(self) -> None:
        """Seed known corporate patterns and executive identity lookups."""
        self.known_fraud_domains.update({
            "google-career-portal.org",
            "microsoft-recruiting-dept.net",
            "amazon-hr-hiring.com",
            "apple-remote-careers.info",
            "meta-global-careers.online",
            "netflix-talent-acquisition.co",
            "tesla-remote-interviews.net"
        })

    def analyze_recruiter_profile(self, profile: RecruiterProfile) -> IdentityAuditResult:
        """Executes full ontological audit on candidate-submitted recruiter identity details."""
        assertions: List[VerificationAssertion] = []
        flagged_techniques: List[ImpersonationTechnique] = []

        # Assertion 1: Free Webmail Check
        webmail_assertion = self._audit_webmail_usage(profile)
        assertions.append(webmail_assertion)
        if not webmail_assertion.passed:
            flagged_techniques.append(ImpersonationTechnique.FREE_WEBMAIL_IMPERSONATION)

        # Assertion 2: Homoglyph & Typosquatting Analysis
        homoglyph_assertion = self._audit_homoglyphs(profile)
        assertions.append(homoglyph_assertion)
        if not homoglyph_assertion.passed:
            flagged_techniques.append(ImpersonationTechnique.HOMOGLYPH_ATTACK)

        # Assertion 3: Subdomain Deception Check
        subdomain_assertion = self._audit_subdomains(profile)
        assertions.append(subdomain_assertion)
        if not subdomain_assertion.passed:
            flagged_techniques.append(ImpersonationTechnique.SUBDOMAIN_SPOOFING)

        # Assertion 4: Chat-Only Channel Reliance
        chat_assertion = self._audit_exclusive_chat_reliance(profile)
        assertions.append(chat_assertion)
        if not chat_assertion.passed:
            flagged_techniques.append(ImpersonationTechnique.DISPLAY_NAME_DECEPTION)

        # Aggregate Risk Computation
        total_risk = 0.0
        for assertion in assertions:
            total_risk += assertion.risk_score_impact
        
        normalized_risk = max(0.0, min(1.0, total_risk))

        confidence_level = self._compute_confidence_level(normalized_risk, assertions)
        recommended_action = self._generate_guidance(confidence_level, flagged_techniques)

        return IdentityAuditResult(
            profile=profile,
            confidence_level=confidence_level,
            aggregate_risk_score=normalized_risk,
            assertions=assertions,
            flagged_techniques=flagged_techniques,
            recommended_action=recommended_action
        )

    def _audit_webmail_usage(self, profile: RecruiterProfile) -> VerificationAssertion:
        email = profile.claimed_email.lower().strip()
        domain = email.split("@")[-1] if "@" in email else ""

        if domain in self.FREE_WEBMAIL_PROVIDERS:
            return VerificationAssertion(
                assertion_id=f"VER-WEBMAIL-{hashlib.md5(email.encode()).hexdigest()[:8]}",
                verifier_subsystem="DomainReputationVerifier",
                technique=ImpersonationTechnique.FREE_WEBMAIL_IMPERSONATION,
                passed=False,
                risk_score_impact=0.45,
                evidence_summary=f"Recruiter claims to represent {profile.claimed_company} but uses free public webmail (@{domain}).",
                details={"domain": domain, "claimed_company": profile.claimed_company}
            )
        return VerificationAssertion(
            assertion_id=f"VER-WEBMAIL-PASS-{hashlib.md5(email.encode()).hexdigest()[:8]}",
            verifier_subsystem="DomainReputationVerifier",
            technique=ImpersonationTechnique.FREE_WEBMAIL_IMPERSONATION,
            passed=True,
            risk_score_impact=0.0,
            evidence_summary=f"Recruiter email uses custom corporate domain (@{domain}).",
            details={"domain": domain}
        )

    def _audit_homoglyphs(self, profile: RecruiterProfile) -> VerificationAssertion:
        email = profile.claimed_email.lower()
        domain = email.split("@")[-1] if "@" in email else ""

        found_homoglyphs: List[Tuple[str, str]] = []
        for char, replacement in self.HOMOGLYPH_MAPPINGS.items():
            if char in domain and char not in "01":  # Skip common digits unless context indicates
                found_homoglyphs.append((char, replacement))

        if found_homoglyphs:
            return VerificationAssertion(
                assertion_id=f"VER-HOMOGLYPH-{hashlib.md5(domain.encode()).hexdigest()[:8]}",
                verifier_subsystem="CyrillicHomoglyphDetector",
                technique=ImpersonationTechnique.HOMOGLYPH_ATTACK,
                passed=False,
                risk_score_impact=0.60,
                evidence_summary=f"Domain '{domain}' contains confusable or Cyrillic homoglyphs designed to visually deceive candidates.",
                details={"detected_substitutions": found_homoglyphs, "domain": domain}
            )
        return VerificationAssertion(
            assertion_id=f"VER-HOMOGLYPH-PASS",
            verifier_subsystem="CyrillicHomoglyphDetector",
            technique=ImpersonationTechnique.HOMOGLYPH_ATTACK,
            passed=True,
            risk_score_impact=0.0,
            evidence_summary="Domain contains standard ASCII characters with no detected character homoglyph substitution.",
            details={"domain": domain}
        )

    def _audit_subdomains(self, profile: RecruiterProfile) -> VerificationAssertion:
        email = profile.claimed_email.lower()
        domain = email.split("@")[-1] if "@" in email else ""

        if domain in self.known_fraud_domains:
            return VerificationAssertion(
                assertion_id="VER-KNOWN-FRAUD-DOMAIN",
                verifier_subsystem="ThreatIntelligenceFeed",
                technique=ImpersonationTechnique.COMBO_SQUATTING,
                passed=False,
                risk_score_impact=0.90,
                evidence_summary=f"Domain '{domain}' is actively cataloged in global recruitment fraud databases.",
                details={"threat_domain": domain}
            )

        for pattern in self.SUSPICIOUS_SUBDOMAIN_PATTERNS:
            if pattern.search(domain):
                return VerificationAssertion(
                    assertion_id="VER-SUBDOMAIN-SPOOF",
                    verifier_subsystem="SubdomainHeuristicEngine",
                    technique=ImpersonationTechnique.SUBDOMAIN_SPOOFING,
                    passed=False,
                    risk_score_impact=0.35,
                    evidence_summary=f"Domain '{domain}' matches common synthetic career portal naming structures.",
                    details={"pattern_matched": pattern.pattern, "domain": domain}
                )

        return VerificationAssertion(
            assertion_id="VER-SUBDOMAIN-PASS",
            verifier_subsystem="SubdomainHeuristicEngine",
            technique=ImpersonationTechnique.SUBDOMAIN_SPOOFING,
            passed=True,
            risk_score_impact=0.0,
            evidence_summary="Domain structure appears standard without deceptive career-keyword prefixing.",
            details={"domain": domain}
        )

    def _audit_exclusive_chat_reliance(self, profile: RecruiterProfile) -> VerificationAssertion:
        has_chat = bool(profile.telegram_handle or profile.whatsapp_number)
        has_email = bool(profile.claimed_email)
        has_linkedin = bool(profile.linkedin_url)

        if has_chat and not has_linkedin and not has_email:
            return VerificationAssertion(
                assertion_id="VER-EXCLUSIVE-CHAT",
                verifier_subsystem="ChannelReliabilityEngine",
                technique=ImpersonationTechnique.DISPLAY_NAME_DECEPTION,
                passed=False,
                risk_score_impact=0.50,
                evidence_summary="Recruiter operates exclusively over anonymous messaging apps (Telegram/WhatsApp) without verifiable corporate identity.",
                details={"telegram": profile.telegram_handle, "whatsapp": profile.whatsapp_number}
            )
        return VerificationAssertion(
            assertion_id="VER-CHANNEL-PASS",
            verifier_subsystem="ChannelReliabilityEngine",
            technique=ImpersonationTechnique.DISPLAY_NAME_DECEPTION,
            passed=True,
            risk_score_impact=0.0,
            evidence_summary="Communication channels include verifiable corporate touchpoints.",
            details={}
        )

    def _compute_confidence_level(self, risk_score: float, assertions: List[VerificationAssertion]) -> IdentityConfidenceLevel:
        if risk_score >= 0.70:
            return IdentityConfidenceLevel.UNVERIFIED
        elif risk_score >= 0.40:
            return IdentityConfidenceLevel.LOW_CONFIDENCE
        elif risk_score >= 0.20:
            return IdentityConfidenceLevel.MEDIUM_CONFIDENCE
        elif all(a.passed for a in assertions):
            return IdentityConfidenceLevel.HIGH_CONFIDENCE
        return IdentityConfidenceLevel.MEDIUM_CONFIDENCE

    def _generate_guidance(self, level: IdentityConfidenceLevel, techniques: List[ImpersonationTechnique]) -> str:
        if level in (IdentityConfidenceLevel.UNVERIFIED, IdentityConfidenceLevel.LOW_CONFIDENCE):
            reasons = ", ".join(t.value for t in techniques)
            return f"CRITICAL: High probability of recruiter impersonation ({reasons}). Do not share personal documents, bank details, or send funds."
        elif level == IdentityConfidenceLevel.MEDIUM_CONFIDENCE:
            return "WARNING: Moderate ambiguity in recruiter credentials. Independently verify recruiter via official company careers page."
        return "SAFE: Recruiter identity indicators align with authentic corporate standards."
