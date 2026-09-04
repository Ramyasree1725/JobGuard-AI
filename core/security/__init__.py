"""
JobGuard Security & Zero-Trust Verification Framework
Provides cryptographic guarantees, certificate chain auditing, token bucket rate limiting,
attribute-based access control, and real-time threat signature detection.
"""

from .crypto_primitives import HKDF, ChaCha20, Poly1305, ChaCha20Poly1305AEAD, ConstantTime, SHA256HMAC, SecureTokenGenerator
from .cert_auditor import CertificateChainAuditor, X509Parser, CertificateValidationResult
from .rate_limiter import DistributedTokenBucket, SlidingWindowCounter, RateLimiterRegistry
from .zero_trust_policy import ZeroTrustPolicyEngine, AccessPolicy, SecurityContext, TokenIssuer
from .threat_signature_db import ThreatSignatureDatabase, SignatureRule, ThreatMatchResult

__all__ = [
    "HKDF",
    "ChaCha20",
    "Poly1305",
    "ChaCha20Poly1305AEAD",
    "ConstantTime",
    "SHA256HMAC",
    "SecureTokenGenerator",
    "CertificateChainAuditor",
    "X509Parser",
    "CertificateValidationResult",
    "DistributedTokenBucket",
    "SlidingWindowCounter",
    "RateLimiterRegistry",
    "ZeroTrustPolicyEngine",
    "AccessPolicy",
    "SecurityContext",
    "TokenIssuer",
    "ThreatSignatureDatabase",
    "SignatureRule",
    "ThreatMatchResult",
]
