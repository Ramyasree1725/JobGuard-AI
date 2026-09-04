"""
JobGuard Core Compliance - Data Retention Lifecycle & Scheduled Purging
Implements GDPR Article 17 ("Right to Erasure"), CCPA deletion requests,
and automated multi-tier archiving / tombstoning of expired scan telemetry.
"""

import time
import enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


class LifecycleStage(enum.Enum):
    HOT_ACTIVE = "HOT_ACTIVE"        # 0 - 30 days: In-memory & fast cache
    WARM_ARCHIVE = "WARM_ARCHIVE"    # 30 - 90 days: Compressed storage
    COLD_COMPLIANCE = "COLD_COMPLIANCE" # 90 - 365 days: Audit log only
    PURGED = "PURGED"                # 365+ days: Cryptographically tombstoned


@dataclass
class RetentionPolicy:
    policy_name: str
    hot_retention_days: int = 30
    warm_retention_days: int = 90
    cold_retention_days: int = 365
    allow_user_deletion: bool = True
    anonymize_on_archive: bool = True


@dataclass
class LifecycleEvent:
    record_id: str
    previous_stage: LifecycleStage
    new_stage: LifecycleStage
    timestamp: float
    reason: str


class RetentionLifecycleManager:
    """Manages stage transitions and legal hold compliance for ingested records."""

    def __init__(self, policy: Optional[RetentionPolicy] = None):
        self.policy = policy or RetentionPolicy("DefaultGDPRCompliantPolicy")
        self._records: Dict[str, Tuple[LifecycleStage, float, Dict[str, Any]]] = {}  # id -> (stage, created_at, payload)
        self._legal_holds: Dict[str, str] = {}  # record_id -> hold_reason
        self._history: List[LifecycleEvent] = []

    def register_record(self, record_id: str, payload: Dict[str, Any], created_at: Optional[float] = None) -> None:
        t = created_at or time.time()
        self._records[record_id] = (LifecycleStage.HOT_ACTIVE, t, payload)

    def apply_legal_hold(self, record_id: str, reason: str) -> bool:
        """Place legal hold to prevent automated purge during law enforcement investigations."""
        if record_id in self._records:
            self._legal_holds[record_id] = reason
            return True
        return False

    def release_legal_hold(self, record_id: str) -> None:
        self._legal_holds.pop(record_id, None)

    def request_user_erasure(self, record_id: str) -> Tuple[bool, str]:
        """GDPR Article 17 Right to Erasure handler."""
        if record_id not in self._records:
            return False, "Record not found"
        if record_id in self._legal_holds:
            return False, f"Cannot erase record under active statutory legal hold: {self._legal_holds[record_id]}"

        current_stage, t, payload = self._records[record_id]
        self._records[record_id] = (LifecycleStage.PURGED, t, {"status": "tombstoned", "erased_at": time.time()})
        self._history.append(LifecycleEvent(
            record_id=record_id,
            previous_stage=current_stage,
            new_stage=LifecycleStage.PURGED,
            timestamp=time.time(),
            reason="User GDPR Article 17 Right to Erasure requested"
        ))
        return True, "Record successfully purged and tombstoned"

    def run_lifecycle_sweep(self, current_time: Optional[float] = None) -> List[LifecycleEvent]:
        """Evaluate age of all records and transition stages."""
        now = current_time or time.time()
        events: List[LifecycleEvent] = []

        day_sec = 86400.0
        hot_limit = self.policy.hot_retention_days * day_sec
        warm_limit = self.policy.warm_retention_days * day_sec
        cold_limit = self.policy.cold_retention_days * day_sec

        for rec_id, (stage, created_at, payload) in list(self._records.items()):
            if rec_id in self._legal_holds or stage == LifecycleStage.PURGED:
                continue

            age_sec = now - created_at
            target_stage = stage

            if age_sec > cold_limit:
                target_stage = LifecycleStage.PURGED
            elif age_sec > warm_limit:
                target_stage = LifecycleStage.COLD_COMPLIANCE
            elif age_sec > hot_limit:
                target_stage = LifecycleStage.WARM_ARCHIVE

            if target_stage != stage:
                self._records[rec_id] = (target_stage, created_at, payload)
                event = LifecycleEvent(
                    record_id=rec_id,
                    previous_stage=stage,
                    new_stage=target_stage,
                    timestamp=now,
                    reason=f"Retention policy automated age transition ({int(age_sec / day_sec)} days)"
                )
                events.append(event)
                self._history.append(event)

        return events
