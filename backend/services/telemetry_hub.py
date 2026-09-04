"""
JobGuard Backend Service - Telemetry Hub & Prometheus Metric Exporter
Collects real-time scan latencies, fraud detection counts, and exposes
Prometheus-compliant /metrics endpoints for cluster observability.
"""

import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class MetricSnapshot:
    total_scans_processed: int
    scams_intercepted_count: int
    safe_offers_verified_count: int
    average_latency_ms: float
    active_threat_rules: int
    uptime_seconds: float


class TelemetryHub:
    """Thread-safe Prometheus and APM telemetry accumulator."""

    def __init__(self):
        self._start_time = time.time()
        self._total_scans = 0
        self._scams_detected = 0
        self._safe_offers = 0
        self._latencies: List[float] = []
        self._lock = threading.Lock()

    def record_scan(self, is_scam: bool, is_safe_offer: bool, latency_ms: float) -> None:
        with self._lock:
            self._total_scans += 1
            if is_scam:
                self._scams_detected += 1
            if is_safe_offer:
                self._safe_offers += 1
            self._latencies.append(latency_ms)
            if len(self._latencies) > 500:
                self._latencies.pop(0)

    def get_snapshot(self) -> MetricSnapshot:
        with self._lock:
            avg_lat = sum(self._latencies) / len(self._latencies) if self._latencies else 0.0
            return MetricSnapshot(
                total_scans_processed=self._total_scans,
                scams_intercepted_count=self._scams_detected,
                safe_offers_verified_count=self._safe_offers,
                average_latency_ms=round(avg_lat, 2),
                active_threat_rules=64,
                uptime_seconds=round(time.time() - self._start_time, 1)
            )


class PrometheusExporter:
    """Formats telemetry snapshot into OpenMetrics / Prometheus text standard."""

    @staticmethod
    def export(snapshot: MetricSnapshot) -> str:
        lines = [
            "# HELP jobguard_scans_total Total count of job posts and offers scanned.",
            "# TYPE jobguard_scans_total counter",
            f"jobguard_scans_total {snapshot.total_scans_processed}",
            "",
            "# HELP jobguard_scams_detected_total Count of fraudulent scam jobs intercepted.",
            "# TYPE jobguard_scams_detected_total counter",
            f"jobguard_scams_detected_total {snapshot.scams_intercepted_count}",
            "",
            "# HELP jobguard_safe_offers_total Count of zero-risk verified legitimate offers.",
            "# TYPE jobguard_safe_offers_total counter",
            f"jobguard_safe_offers_total {snapshot.safe_offers_verified_count}",
            "",
            "# HELP jobguard_scan_latency_ms Average end-to-end scan latency in milliseconds.",
            "# TYPE jobguard_scan_latency_ms gauge",
            f"jobguard_scan_latency_ms {snapshot.average_latency_ms}",
            "",
            "# HELP jobguard_uptime_seconds Service uptime in seconds.",
            "# TYPE jobguard_uptime_seconds gauge",
            f"jobguard_uptime_seconds {snapshot.uptime_seconds}"
        ]
        return "\n".join(lines) + "\n"
