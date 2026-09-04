"""
JobGuard Core Workflow - Circuit Breaker & Fault-Tolerant Retry Orchestrator
Implements Martin Fowler's Circuit Breaker pattern (Closed, Open, Half-Open)
with randomized jitter exponential backoff for outbound threat lookups and APIs.
"""

import time
import random
import enum
import threading
from typing import Callable, Optional, Any, Dict, Type


class CircuitState(enum.Enum):
    CLOSED = "CLOSED"        # Normal operations: passing requests through
    OPEN = "OPEN"            # Failing: blocking all requests immediately
    HALF_OPEN = "HALF_OPEN"  # Testing: allowing limited trial requests


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    """Thread-safe circuit breaker protecting downstream services from cascade failure."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 30.0,
        half_open_success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.half_open_success_threshold = half_open_success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = time.monotonic()
        self._lock = threading.Lock()

    def call(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """Execute callable through circuit breaker guard."""
        with self._lock:
            now = time.monotonic()
            if self.state == CircuitState.OPEN:
                if now - self.last_state_change > self.recovery_timeout_sec:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    self.last_state_change = now
                else:
                    raise CircuitBreakerOpenException(f"Circuit is OPEN. Fast failing request to avoid overload.")

        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self) -> None:
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.half_open_success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.last_state_change = time.monotonic()
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    def _on_failure(self) -> None:
        with self._lock:
            self.failure_count += 1
            if self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
                if self.failure_count >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
                    self.state = CircuitState.OPEN
                    self.last_state_change = time.monotonic()


class ExponentialBackoff:
    """Full jitter exponential backoff calculator."""

    @staticmethod
    def calculate_delay(attempt: int, base_delay: float = 0.5, max_delay: float = 30.0) -> float:
        exponential = min(max_delay, base_delay * (2 ** attempt))
        return random.uniform(0.0, exponential)


class RetryOrchestrator:
    """Executes callables with configurable retry backoff and circuit breaker protection."""

    def __init__(self, max_retries: int = 3, circuit_breaker: Optional[CircuitBreaker] = None):
        self.max_retries = max_retries
        self.circuit_breaker = circuit_breaker or CircuitBreaker()

    def execute_with_retry(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                return self.circuit_breaker.call(fn, *args, **kwargs)
            except CircuitBreakerOpenException:
                raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = ExponentialBackoff.calculate_delay(attempt)
                    time.sleep(delay)

        raise last_exception
