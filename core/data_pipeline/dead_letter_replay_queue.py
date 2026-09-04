"""
JobGuard Core Data Pipeline - Dead Letter Queue (DLQ) & Replay Engine
Captures corrupted, unparseable, or schema-violating telemetry payloads with
exponential retry backoff, quarantine triage, and replay execution audit logs.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
import time
import uuid


@dataclass
class PoisonMessage:
    message_id: str
    original_topic: str
    raw_payload: str
    failure_reason: str
    retry_count: int = 0
    first_failed_at: float = field(default_factory=time.time)
    last_retry_at: Optional[float] = None
    quarantined: bool = False


@dataclass
class ReplayExecutionResult:
    total_messages_replayed: int
    successful_replays: int
    permanent_failures: int
    remaining_in_dlq: int


class DeadLetterReplayQueue:
    """Manages poisoned stream messages and controlled retry batch operations."""

    def __init__(self, max_retry_limit: int = 5):
        self.max_retry_limit = max_retry_limit
        self.messages: Dict[str, PoisonMessage] = {}

    def push_failed_message(self, topic: str, payload: str, reason: str) -> str:
        """Enqueues a failed payload into the dead letter queue."""
        msg_id = f"DLQ-{uuid.uuid4().hex[:8].upper()}"
        msg = PoisonMessage(
            message_id=msg_id,
            original_topic=topic,
            raw_payload=payload,
            failure_reason=reason
        )
        self.messages[msg_id] = msg
        return msg_id

    def replay_batch(self, target_topic: str, consumer_fn: Callable[[str], bool]) -> ReplayExecutionResult:
        """Attempts reprocessing on non-quarantined messages matching target topic."""
        candidates = [m for m in self.messages.values() if m.original_topic == target_topic and not m.quarantined]
        success_count = 0
        perm_failures = 0

        for msg in candidates:
            msg.retry_count += 1
            msg.last_retry_at = time.time()
            try:
                success = consumer_fn(msg.raw_payload)
                if success:
                    success_count += 1
                    del self.messages[msg.message_id]
                else:
                    if msg.retry_count >= self.max_retry_limit:
                        msg.quarantined = True
                        perm_failures += 1
            except Exception as ex:
                if msg.retry_count >= self.max_retry_limit:
                    msg.quarantined = True
                    perm_failures += 1

        return ReplayExecutionResult(
            total_messages_replayed=len(candidates),
            successful_replays=success_count,
            permanent_failures=perm_failures,
            remaining_in_dlq=len(self.messages)
        )
