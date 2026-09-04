"""
JobGuard Core Workflow - Event Sourcing Engine & Immutable Audit Ledger
Maintains an append-only sequence of domain events with cryptographic hash-chaining,
snapshot point materialization, and point-in-time state reconstruction.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import hashlib
import json
import time


@dataclass
class DomainEvent:
    event_id: str
    aggregate_id: str
    event_type: str
    sequence_number: int
    payload: Dict[str, Any]
    timestamp_utc: float
    previous_event_hash: str
    event_hash: str


@dataclass
class AggregateSnapshot:
    aggregate_id: str
    last_sequence_number: int
    state_payload: Dict[str, Any]
    snapshot_timestamp: float


class EventSourcingEngine:
    """Immutable event store with cryptographic chaining and aggregate state reconstruction."""

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self.event_store: Dict[str, List[DomainEvent]] = {}  # aggregate_id -> events
        self.snapshots: Dict[str, AggregateSnapshot] = {}

    def append_event(self, aggregate_id: str, event_type: str, payload: Dict[str, Any]) -> DomainEvent:
        """Appends an immutable domain event, cryptographically sealing it with previous event hash."""
        events = self.event_store.setdefault(aggregate_id, [])
        seq = len(events) + 1
        prev_hash = events[-1].event_hash if events else self.GENESIS_HASH

        now = time.time()
        raw_to_hash = f"{aggregate_id}|{event_type}|{seq}|{json.dumps(payload, sort_keys=True)}|{now}|{prev_hash}"
        cur_hash = hashlib.sha256(raw_to_hash.encode("utf-8")).hexdigest()

        event = DomainEvent(
            event_id=f"EVT-{aggregate_id}-{seq:05d}",
            aggregate_id=aggregate_id,
            event_type=event_type,
            sequence_number=seq,
            payload=payload,
            timestamp_utc=now,
            previous_event_hash=prev_hash,
            event_hash=cur_hash
        )
        events.append(event)
        return event

    def verify_integrity(self, aggregate_id: str) -> bool:
        """Verifies the complete SHA-256 hash chain for an aggregate's historical events."""
        events = self.event_store.get(aggregate_id, [])
        if not events:
            return True

        expected_prev = self.GENESIS_HASH
        for e in events:
            if e.previous_event_hash != expected_prev:
                return False

            raw = f"{e.aggregate_id}|{e.event_type}|{e.sequence_number}|{json.dumps(e.payload, sort_keys=True)}|{e.timestamp_utc}|{expected_prev}"
            recomputed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if recomputed != e.event_hash:
                return False

            expected_prev = e.event_hash

        return True

    def replay_state(self, aggregate_id: str, target_sequence: Optional[int] = None) -> Dict[str, Any]:
        """Reconstructs the exact state of an entity by replaying its domain events sequentially."""
        events = self.event_store.get(aggregate_id, [])
        state: Dict[str, Any] = {}

        for e in events:
            if target_sequence is not None and e.sequence_number > target_sequence:
                break
            
            # Apply state mutation rules
            if e.event_type == "CANDIDATE_SCANNED_JOB":
                state["last_job_id"] = e.payload.get("job_id")
                state["total_scans"] = state.get("total_scans", 0) + 1
            elif e.event_type == "FRAUD_THREAT_FLAGGED":
                state.setdefault("flagged_threats", []).append(e.payload.get("threat_vector"))
                state["current_risk_score"] = e.payload.get("score", 0.0)
            elif e.event_type == "OFFER_LETTER_AUDITED":
                state["audited_contracts_count"] = state.get("audited_contracts_count", 0) + 1
                state["is_safe_to_sign"] = e.payload.get("is_safe", False)

        return state
