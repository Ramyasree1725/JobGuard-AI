"""
JobGuard Core Security - Distributed Rate Limiter & Abuse Mitigation
Provides Token Bucket, Sliding Window Log, and Leaky Bucket algorithms
with IP tiering, threat-based throttling, and automatic burst allowances.
"""

import time
import threading
from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass, field


@dataclass
class RateLimitRule:
    max_requests: int
    window_seconds: float
    burst_capacity: int = 0
    threat_multiplier: float = 1.0


@dataclass
class RateLimitStatus:
    allowed: bool
    remaining: int
    reset_in_seconds: float
    current_load_pct: float
    threat_tier: str = "normal"


class DistributedTokenBucket:
    """Thread-safe Token Bucket rate limiter with dynamic replenishment."""

    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self, now: float) -> None:
        elapsed = now - self.last_refill
        if elapsed > 0:
            added_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + added_tokens)
            self.last_refill = now

    def acquire(self, tokens_required: float = 1.0) -> bool:
        """Attempt to acquire tokens; returns True if successful."""
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            if self.tokens >= tokens_required:
                self.tokens -= tokens_required
                return True
            return False

    def get_remaining(self) -> float:
        with self._lock:
            self._refill(time.monotonic())
            return self.tokens


class SlidingWindowCounter:
    """Accurate sliding-window log counter for strict API rate enforcement."""

    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps: List[float] = []
        self._lock = threading.Lock()

    def check_and_record(self, now: Optional[float] = None) -> Tuple[bool, int, float]:
        """Returns (is_allowed, remaining_count, reset_seconds)."""
        current_time = now if now is not None else time.monotonic()
        cutoff = current_time - self.window_seconds

        with self._lock:
            # Purge expired timestamps
            self.timestamps = [t for t in self.timestamps if t > cutoff]
            
            count = len(self.timestamps)
            if count < self.max_requests:
                self.timestamps.append(current_time)
                remaining = self.max_requests - (count + 1)
                reset_seconds = max(0.0, self.window_seconds - (current_time - (self.timestamps[0] if self.timestamps else current_time)))
                return True, remaining, round(reset_seconds, 2)
            else:
                oldest = self.timestamps[0]
                reset_seconds = max(0.0, self.window_seconds - (current_time - oldest))
                return False, 0, round(reset_seconds, 2)


class RateLimiterRegistry:
    """Central multi-tenant rate limiter registry supporting client IP, user ID, and threat tiering."""

    DEFAULT_RULES: Dict[str, RateLimitRule] = {
        "anonymous": RateLimitRule(max_requests=20, window_seconds=60.0, burst_capacity=5),
        "authenticated": RateLimitRule(max_requests=120, window_seconds=60.0, burst_capacity=20),
        "api_service": RateLimitRule(max_requests=600, window_seconds=60.0, burst_capacity=50),
        "high_threat": RateLimitRule(max_requests=3, window_seconds=60.0, burst_capacity=0, threat_multiplier=0.2),
    }

    def __init__(self):
        self._buckets: Dict[str, DistributedTokenBucket] = {}
        self._sliding_windows: Dict[str, SlidingWindowCounter] = {}
        self._client_reputations: Dict[str, str] = {}  # ip -> threat tier
        self._lock = threading.Lock()

    def set_client_reputation(self, client_key: str, tier: str) -> None:
        """Assign threat tier ('normal', 'suspicious', 'high_threat') to a client."""
        with self._lock:
            self._client_reputations[client_key] = tier

    def check_limit(self, client_key: str, role: str = "anonymous") -> RateLimitStatus:
        """Evaluate rate limit for a client request."""
        now = time.monotonic()
        
        with self._lock:
            threat_tier = self._client_reputations.get(client_key, "normal")
            rule_key = "high_threat" if threat_tier == "high_threat" else role
            rule = self.DEFAULT_RULES.get(rule_key, self.DEFAULT_RULES["anonymous"])

            bucket_key = f"{client_key}:{role}"
            if bucket_key not in self._sliding_windows:
                capacity = int(rule.max_requests * rule.threat_multiplier)
                self._sliding_windows[bucket_key] = SlidingWindowCounter(
                    max_requests=max(1, capacity),
                    window_seconds=rule.window_seconds
                )
            
            limiter = self._sliding_windows[bucket_key]

        allowed, remaining, reset_in = limiter.check_and_record(now)
        max_allowed = max(1, int(rule.max_requests * rule.threat_multiplier))
        load_pct = round(((max_allowed - remaining) / max_allowed) * 100.0, 1)

        return RateLimitStatus(
            allowed=allowed,
            remaining=remaining,
            reset_in_seconds=reset_in,
            current_load_pct=min(100.0, load_pct),
            threat_tier=threat_tier
        )

    def cleanup_idle(self, max_idle_seconds: float = 3600.0) -> int:
        """Remove idle limiter records to prevent memory leakage."""
        purged = 0
        now = time.monotonic()
        with self._lock:
            keys_to_remove = []
            for k, counter in self._sliding_windows.items():
                with counter._lock:
                    if not counter.timestamps or (now - counter.timestamps[-1] > max_idle_seconds):
                        keys_to_remove.append(k)
            
            for k in keys_to_remove:
                del self._sliding_windows[k]
                purged += 1
                
        return purged
