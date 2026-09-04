"""
JobGuard Core Security - Zero-Trust Policy Engine & Token Manager
Attribute-Based Access Control (ABAC), fine-grained permission scopes,
secure stateless JWT/token signer, and dynamic context authorization.
"""

import base64
import json
import time
import hashlib
import hmac
from typing import Dict, List, Optional, Set, Any, Union
from dataclasses import dataclass, field
from .crypto_primitives import ConstantTime, SHA256HMAC


@dataclass
class SecurityContext:
    user_id: str
    tenant_id: str
    roles: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    ip_address: str = "127.0.0.1"
    is_mfa_verified: bool = False
    issued_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 3600.0)


@dataclass
class AccessPolicy:
    policy_id: str
    description: str
    required_roles: Set[str] = field(default_factory=set)
    required_attributes: Dict[str, Any] = field(default_factory=dict)
    require_mfa: bool = False
    allowed_ip_ranges: Optional[List[str]] = None
    max_risk_score_allowed: float = 80.0


class TokenIssuer:
    """Cryptographic signed token generator and validator (HMAC-SHA256 based compact JWT-like format)."""

    def __init__(self, secret_key: bytes, issuer_id: str = "jobguard-auth-authority"):
        self.secret_key = secret_key
        self.issuer_id = issuer_id

    def issue_token(self, context: SecurityContext) -> str:
        """Create a compact signed token containing the security context claims."""
        header = {"alg": "HS256", "typ": "JGA", "iss": self.issuer_id}
        payload = {
            "sub": context.user_id,
            "tid": context.tenant_id,
            "roles": context.roles,
            "attrs": context.attributes,
            "ip": context.ip_address,
            "mfa": context.is_mfa_verified,
            "iat": int(context.issued_at),
            "exp": int(context.expires_at)
        }

        h_b64 = self._b64_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        p_b64 = self._b64_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
        
        signature = SHA256HMAC.sign(self.secret_key, signing_input)
        s_b64 = self._b64_encode(signature)

        return f"{h_b64}.{p_b64}.{s_b64}"

    def verify_token(self, token_str: str) -> Tuple[bool, Optional[SecurityContext], Optional[str]]:
        """Verify token signature, expiration, and reconstruct SecurityContext."""
        parts = token_str.strip().split(".")
        if len(parts) != 3:
            return False, None, "Malformed token structure: must contain 3 dot-separated segments"

        h_b64, p_b64, s_b64 = parts
        signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
        expected_sig = SHA256HMAC.sign(self.secret_key, signing_input)
        
        try:
            provided_sig = self._b64_decode(s_b64)
        except Exception:
            return False, None, "Invalid Base64 signature encoding"

        if not ConstantTime.compare_bytes(expected_sig, provided_sig):
            return False, None, "Signature mismatch / token tampering detected"

        try:
            payload_bytes = self._b64_decode(p_b64)
            payload = json.loads(payload_bytes.decode("utf-8"))
        except Exception as e:
            return False, None, f"Invalid token payload JSON: {str(e)}"

        now = time.time()
        if payload.get("exp", 0) < now:
            return False, None, f"Token has expired at {payload.get('exp')}"

        context = SecurityContext(
            user_id=payload.get("sub", "anonymous"),
            tenant_id=payload.get("tid", "default"),
            roles=payload.get("roles", []),
            attributes=payload.get("attrs", {}),
            ip_address=payload.get("ip", "127.0.0.1"),
            is_mfa_verified=payload.get("mfa", False),
            issued_at=float(payload.get("iat", now)),
            expires_at=float(payload.get("exp", now + 3600))
        )

        return True, context, None

    @staticmethod
    def _b64_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

    @staticmethod
    def _b64_decode(s: str) -> bytes:
        rem = len(s) % 4
        if rem > 0:
            s += "=" * (4 - rem)
        return base64.urlsafe_b64decode(s.encode("ascii"))


class ZeroTrustPolicyEngine:
    """Zero-Trust ABAC Policy Evaluator."""

    def __init__(self):
        self._policies: Dict[str, AccessPolicy] = {}
        self._register_default_policies()

    def _register_default_policies(self) -> None:
        self._policies["scan:read"] = AccessPolicy(
            policy_id="scan:read",
            description="Allows querying scam scan telemetry and public detection records",
            required_roles={"user", "analyst", "admin"},
            max_risk_score_allowed=100.0
        )
        self._policies["scan:execute"] = AccessPolicy(
            policy_id="scan:execute",
            description="Allows running high-throughput AI heuristics and OCR ingestion",
            required_roles={"user", "subscriber", "admin"},
            max_risk_score_allowed=90.0
        )
        self._policies["admin:manage"] = AccessPolicy(
            policy_id="admin:manage",
            description="Allows managing scam blacklist, user tiers, and policy configurations",
            required_roles={"admin"},
            require_mfa=True,
            max_risk_score_allowed=30.0
        )
        self._policies["batch:audit"] = AccessPolicy(
            policy_id="batch:audit",
            description="Allows batch audit of uploaded enterprise offer contracts",
            required_roles={"subscriber", "admin", "enterprise"},
            max_risk_score_allowed=75.0
        )

    def register_policy(self, policy: AccessPolicy) -> None:
        self._policies[policy.policy_id] = policy

    def evaluate_access(
        self,
        action: str,
        context: SecurityContext,
        current_risk_score: float = 0.0
    ) -> Tuple[bool, str]:
        """Evaluate whether the security context is authorized to perform the requested action."""
        if action not in self._policies:
            return False, f"Denied: Undefined access policy for action '{action}'"

        policy = self._policies[action]

        # 1. MFA Requirement Check
        if policy.require_mfa and not context.is_mfa_verified:
            return False, f"Denied: Multi-Factor Authentication (MFA) required for '{action}'"

        # 2. Risk Score Guard
        if current_risk_score > policy.max_risk_score_allowed:
            return False, f"Denied: Client risk score ({current_risk_score}) exceeds policy threshold ({policy.max_risk_score_allowed})"

        # 3. Role-Based Check
        if policy.required_roles:
            user_roles = set(context.roles)
            if not user_roles.intersection(policy.required_roles) and "admin" not in user_roles:
                return False, f"Denied: Missing required role(s). Allowed: {policy.required_roles}, User has: {context.roles}"

        # 4. Attribute-Based Check (ABAC)
        for attr_key, expected_val in policy.required_attributes.items():
            actual_val = context.attributes.get(attr_key)
            if actual_val != expected_val:
                return False, f"Denied: Attribute mismatch for '{attr_key}'. Required: {expected_val}, Found: {actual_val}"

        return True, f"Authorized: Action '{action}' permitted under policy '{policy.policy_id}'"
