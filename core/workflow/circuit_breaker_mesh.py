"""
JobGuard Core Workflow - Distributed Circuit Breaker & Resiliency Mesh
Implements three-state circuit breakers (CLOSED, OPEN, HALF_OPEN) with adaptive exponential
backoff, error rate sliding windows, and graceful fallback routing for external verification APIs.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import time


class CircuitState(Enum):
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Tripped, rejecting calls immediately
    HALF_OPEN = "HALF_OPEN"  # Testing if remote service has recovered


@dataclass
class CircuitBreakerConfig:
    failure_threshold_rate: float = 0.50  # Trip if > 50% errors
    minimum_sample_size: int = 10
    cooldown_period_seconds: float = 30.0
    half_open_success_threshold: int = 3


class CircuitBreaker:
    """Protects downstream threat intelligence and domain lookup endpoints from cascade failures."""

    def __init__(self, service_name: str, config: Optional[CircuitBreakerConfig] = None):
        self.service_name = service_name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.last_state_change = time.time()
        self.recent_calls: List[bool] = []  # True = success, False = failure
        self.consecutive_half_open_successes = 0

    def call(self, action: Callable[..., Any], fallback: Callable[..., Any], *args, **kwargs) -> Any:
        """Executes action wrapped by circuit breaker state logic."""
        now = time.time()

        if self.state == CircuitState.OPEN:
            if now - self.last_state_change > self.config.cooldown_period_seconds:
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = now
                self.consecutive_half_open_successes = 0
            else:
                # Still tripped
                return fallback(*args, **kwargs)

        try:
            result = action(*args, **kwargs)
            self._record_result(success=True)
            return result
        except Exception as ex:
            self._record_result(success=False)
            return fallback(*args, **kwargs)

    def _record_result(self, success: bool) -> None:
        self.recent_calls.append(success)
        if len(self.recent_calls) > 50:
            self.recent_calls.pop(0)

        if self.state == CircuitState.HALF_OPEN:
            if success:
                self.consecutive_half_open_successes += 1
                if self.consecutive_half_open_successes >= self.config.half_open_success_threshold:
                    self.state = CircuitState.CLOSED
                    self.last_state_change = time.time()
                    self.recent_calls.clear()
            else:
                self.state = CircuitState.OPEN
                self.last_state_change = time.time()

        elif self.state == CircuitState.CLOSED:
            if len(self.recent_calls) >= self.config.minimum_sample_size:
                failures = sum(1 for s in self.recent_calls if not s)
                rate = failures / len(self.recent_calls)
                if rate >= self.config.failure_threshold_rate:
                    self.state = CircuitState.OPEN
                    self.last_state_change = time.time()
