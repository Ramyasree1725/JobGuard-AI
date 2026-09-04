"""
JobGuard Core Security - Decoy Honeypot & Adversarial Lure Telemetry Collector
Deploys synthetic candidate profiles across open job forums to capture live scam campaigns,
extract malicious wire instructions, and map threat actor command-and-control handles.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import time
import uuid


@dataclass
class DecoyCandidateProfile:
    decoy_id: str
    synthetic_name: str
    canary_email: str
    virtual_phone: str
    deployed_platform: str
    target_role: str
    created_at: float


@dataclass
class HoneypotInteractionLog:
    interaction_id: str
    decoy_id: str
    recruiter_identifier: str
    channel_type: str
    received_message: str
    extracted_demands: List[str]  # e.g., 'WIRE_FEE', 'TELEGRAM_CONTACT', 'CHECK_DEPOSIT'
    timestamp_utc: float


class HoneypotTelemetryCollector:
    """Manages canary personas and logs interactions with active fraud operators."""

    def __init__(self):
        self.decoys: Dict[str, DecoyCandidateProfile] = {}
        self.interaction_logs: List[HoneypotInteractionLog] = []

    def deploy_decoy(self, platform: str, role: str) -> DecoyCandidateProfile:
        """Spawns a new canary persona for passive threat intelligence harvesting."""
        decoy_id = f"CANARY-{uuid.uuid4().hex[:6].upper()}"
        profile = DecoyCandidateProfile(
            decoy_id=decoy_id,
            synthetic_name=f"Alex Hunter {decoy_id[-3:]}",
            canary_email=f"candidate.{decoy_id.lower()}@jobguard-honeynet.org",
            virtual_phone="+1-555-019-8234",
            deployed_platform=platform,
            target_role=role,
            created_at=time.time()
        )
        self.decoys[decoy_id] = profile
        return profile

    def log_interaction(
        self,
        decoy_id: str,
        recruiter_id: str,
        channel: str,
        message: str
    ) -> HoneypotInteractionLog:
        """Records inbound scam solicitation directed at canary personas."""
        demands = []
        lower = message.lower()
        if "telegram" in lower or "whatsapp" in lower:
            demands.append("MESSAGING_REDIRECT")
        if "check" in lower or "cheque" in lower:
            demands.append("CHECK_DEPOSIT")
        if "fee" in lower or "zelle" in lower or "crypto" in lower:
            demands.append("UPFRONT_PAYMENT")

        log = HoneypotInteractionLog(
            interaction_id=f"INT-{uuid.uuid4().hex[:8].upper()}",
            decoy_id=decoy_id,
            recruiter_identifier=recruiter_id,
            channel_type=channel,
            received_message=message,
            extracted_demands=demands,
            timestamp_utc=time.time()
        )
        self.interaction_logs.append(log)
        return log
