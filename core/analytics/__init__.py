"""
JobGuard Core Analytics & Threat Intelligence Framework
Provides time-series forecasting, statistical outlier/anomaly detectors,
and high-precision quantile / HyperLogLog metric aggregation.
"""

from .timeseries_forecast import ExponentialSmoothingForecaster, ForecastResult
from .anomaly_detector import IsolationForestAnomalyDetector, MahalanobisOutlierDetector, AnomalyReport
from .metric_aggregator import TDigestQuantileEstimator, HyperLogLogCounter, HistogramBinner

__all__ = [
    "ExponentialSmoothingForecaster",
    "ForecastResult",
    "IsolationForestAnomalyDetector",
    "MahalanobisOutlierDetector",
    "AnomalyReport",
    "TDigestQuantileEstimator",
    "HyperLogLogCounter",
    "HistogramBinner",
]
