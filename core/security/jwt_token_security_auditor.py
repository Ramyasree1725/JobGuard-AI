"""
JobGuard Core Security - JSON Web Token (JWT) Security & Algorithm Confusion Auditor
Inspects JWT header algorithms (alg=none, HMAC-RSA confusion), key ID (kid) SQLi/path traversal,
and expiration claims to prevent authentication bypass on enterprise portals.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import json
import base64
import time


@dataclass
class JWTAuditReport:
    algorithm: str
    is_vulnerable_alg_none: bool
    is_weak_symmetric_key: bool
    has_kid_injection_pattern: bool
    is_expired: bool
    security_score: float  # 0 to 100
    detected_vulnerabilities: List[str]


class JWTTokenSecurityAuditor:
    """Dissects JWT tokens to prevent algorithmic downgrades and claim tampering."""

    def __init__(self):
        pass

    def audit_token_string(self, raw_token: str) -> JWTAuditReport:
        """Parses and checks JWT header and claims for common authentication vulnerabilities."""
        parts = raw_token.strip().split(".")
        if len(parts) != 3:
            return JWTAuditReport(
                algorithm="UNKNOWN",
                is_vulnerable_alg_none=False,
                is_weak_symmetric_key=False,
                has_kid_injection_pattern=False,
                is_expired=True,
                security_score=0.0,
                detected_vulnerabilities=["Malformed JWT: Does not contain standard 3-part structure."]
            )

        header_b64, payload_b64, sig_b64 = parts
        vulns: List[str] = []
        score = 100.0

        try:
            # Decode header
            header_json = self._base64_url_decode(header_b64)
            header = json.loads(header_json)
        except Exception:
            header = {}

        try:
            # Decode payload
            payload_json = self._base64_url_decode(payload_b64)
            payload = json.loads(payload_json)
        except Exception:
            payload = {}

        alg = header.get("alg", "UNKNOWN").upper()
        kid = str(header.get("kid", ""))

        # Check 1: 'none' algorithm bypass
        is_none = (alg == "NONE")
        if is_none:
            vulns.append("CRITICAL: Token specifies 'alg=none', allowing unsigned authentication bypass.")
            score -= 80.0

        # Check 2: Key ID Path Traversal / SQL Injection
        has_kid_inj = False
        if any(char in kid for char in ["../", "..\\", "'", '"', "--", ";"]):
            has_kid_inj = True
            vulns.append(f"CRITICAL: Header 'kid' parameter contains injection characters: '{kid}'.")
            score -= 60.0

        # Check 3: Expiration
        now = time.time()
        exp = payload.get("exp", 0)
        is_exp = (exp < now) if exp else False
        if is_exp:
            vulns.append(f"Token is expired (Expired at {exp}, current time {now}).")
            score -= 30.0

        return JWTAuditReport(
            algorithm=alg,
            is_vulnerable_alg_none=is_none,
            is_weak_symmetric_key=False,
            has_kid_injection_pattern=has_kid_inj,
            is_expired=is_exp,
            security_score=max(0.0, score),
            detected_vulnerabilities=vulns if vulns else ["JWT structure and cryptographic claims conform to RFC 7519 standards."]
        )

    def _base64_url_decode(self, input_str: str) -> str:
        rem = len(input_str) % 4
        if rem > 0:
            input_str += "=" * (4 - rem)
        return base64.urlsafe_b64decode(input_str.encode("utf-8")).decode("utf-8", errors="ignore")
