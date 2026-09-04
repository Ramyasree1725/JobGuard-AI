"""
JobGuard Backend Services Architecture
Microservices for domain reputation scoring, multi-tier job post verification pipelines,
Prometheus telemetry instrumentation, and real-time threat intelligence ingestion.
"""

from .domain_reputation import DomainReputationService, DomainRiskScore
from .job_pipeline import JobVerificationPipeline, VerificationStageResult
from .telemetry_hub import TelemetryHub, MetricSnapshot, PrometheusExporter
from .threat_intel import ThreatIntelligenceFeed, ThreatIndicator

__all__ = [
    "DomainReputationService",
    "DomainRiskScore",
    "JobVerificationPipeline",
    "VerificationStageResult",
    "TelemetryHub",
    "MetricSnapshot",
    "PrometheusExporter",
    "ThreatIntelligenceFeed",
    "ThreatIndicator",
]
