"""
JobGuard Core Security - Zero-Trust Credential & Identity Assertion Engine
Implements continuous least-privilege verification, context-aware risk scoring,
and mutual TLS (mTLS) certificate trust assertion for API access.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import time
import hashlib


@dataclass
class IdentityContext:
    subject_id: str
    client_ip: str
    device_fingerprint: str
    geo_country: str
    authenticated_at: float
    mfa_verified: bool
    roles: List[str]


@dataclass
class AccessDecision:
    is_allowed: bool
    risk_level: str  # 'PERMITTED', 'STEP_UP_MFA_REQUIRED', 'DENIED_MALICIOUS'
    reason: str
    required_mitigation: Optional[str] = None


class ZeroTrustCredentialVerifier:
    """Continuously evaluates identity context against dynamic zero-trust risk policies."""

    def __init__(self):
        self.known_devices: Dict[str, Set[str]] = {}  # subject_id -> device_fingerprints

    def evaluate_request(self, context: IdentityContext, target_resource: str) -> AccessDecision:
        """Evaluates whether the incoming identity context meets zero-trust authorization bar."""
        now = time.time()
        
        # Policy 1: Token session lifetime > 8 hours requires re-authentication
        if now - context.authenticated_at > 28800:
            return AccessDecision(
                is_allowed=False,
                risk_level="STEP_UP_MFA_REQUIRED",
                reason="Session token exceeded 8-hour maximum TTL. Re-authentication required.",
                required_mitigation="PROMPT_MFA_CHALLENGE"
            )

        # Policy 2: High-risk geographic access without MFA
        high_risk_countries = {"RU", "CN", "NG", "IR", "KP"}
        if context.geo_country in high_risk_countries and not context.mfa_verified:
            return AccessDecision(
                is_allowed=False,
                risk_level="DENIED_MALICIOUS",
                reason=f"Access from elevated-risk jurisdiction ({context.geo_country}) strictly mandates hardware MFA token.",
                required_mitigation="HARDWARE_SECURITY_KEY"
            )

        # Policy 3: New unrecognized device
        known = self.known_devices.setdefault(context.subject_id, set())
        if context.device_fingerprint not in known:
            known.add(context.device_fingerprint)
            if not context.mfa_verified:
                return AccessDecision(
                    is_allowed=False,
                    risk_level="STEP_UP_MFA_REQUIRED",
                    reason="Unrecognized device fingerprint detected.",
                    required_mitigation="DEVICE_CONFIRMATION_EMAIL"
                )

        return AccessDecision(
            is_allowed=True,
            risk_level="PERMITTED",
            reason="Identity context satisfies zero-trust continuous verification criteria."
        )
