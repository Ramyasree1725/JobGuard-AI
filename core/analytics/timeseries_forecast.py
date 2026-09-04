"""
JobGuard Core Analytics - Time-Series Forecasting & Trend Extrapolator
Implements Holt-Winters Triple Exponential Smoothing (Level, Trend, Seasonality)
to forecast upcoming scam attack surges and domain registration waves.
"""

import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ForecastResult:
    point_forecasts: List[float]
    upper_confidence_bounds: List[float]
    lower_confidence_bounds: List[float]
    estimated_trend_slope: float
    seasonal_factors: List[float]


class ExponentialSmoothingForecaster:
    """Holt-Winters Triple Exponential Smoothing Forecaster."""

    def __init__(
        self,
        season_length: int = 7,
        alpha: float = 0.3,
        beta: float = 0.1,
        gamma: float = 0.2
    ):
        self.season_length = max(2, season_length)
        self.alpha = alpha  # Level smoothing factor
        self.beta = beta    # Trend smoothing factor
        self.gamma = gamma  # Seasonal smoothing factor

        self.level: float = 0.0
        self.trend: float = 0.0
        self.seasonal: List[float] = [1.0] * self.season_length

    def fit(self, series: List[float]) -> "ExponentialSmoothingForecaster":
        """Fit model parameters on historical time series data."""
        n = len(series)
        L = self.season_length

        if n < L * 2:
            # Fallback simple initialization
            self.level = series[0] if series else 0.0
            self.trend = (series[-1] - series[0]) / max(1, n) if n > 1 else 0.0
            self.seasonal = [1.0] * L
            return self

        # Initial level and trend from first two seasons
        s1 = sum(series[:L]) / L
        s2 = sum(series[L:2 * L]) / L
        self.level = s1
        self.trend = (s2 - s1) / L

        # Initial seasonal indices
        self.seasonal = []
        for i in range(L):
            self.seasonal.append((series[i] + series[L + i]) / (2.0 * max(1e-4, (s1 + s2) / 2.0)))

        # Recursive updates
        for t in range(n):
            val = series[t]
            s_idx = t % L
            old_level = self.level
            
            # Level update
            self.level = self.alpha * (val / max(1e-4, self.seasonal[s_idx])) + (1.0 - self.alpha) * (self.level + self.trend)
            # Trend update
            self.trend = self.beta * (self.level - old_level) + (1.0 - self.beta) * self.trend
            # Seasonality update
            self.seasonal[s_idx] = self.gamma * (val / max(1e-4, self.level)) + (1.0 - self.gamma) * self.seasonal[s_idx]

        return self

    def forecast(self, horizon: int = 7, confidence_interval: float = 0.95) -> ForecastResult:
        """Forecast future horizon periods ahead with confidence intervals."""
        forecasts: List[float] = []
        uppers: List[float] = []
        lowers: List[float] = []
        z = 1.96 if confidence_interval >= 0.95 else 1.645

        std_err = math.sqrt(max(0.1, abs(self.level * 0.05)))

        for m in range(1, horizon + 1):
            s_idx = (m - 1) % self.season_length
            point = (self.level + m * self.trend) * self.seasonal[s_idx]
            point = max(0.0, point)
            
            margin = z * std_err * math.sqrt(m)
            forecasts.append(round(point, 2))
            uppers.append(round(point + margin, 2))
            lowers.append(round(max(0.0, point - margin), 2))

        return ForecastResult(
            point_forecasts=forecasts,
            upper_confidence_bounds=uppers,
            lower_confidence_bounds=lowers,
            estimated_trend_slope=round(self.trend, 4),
            seasonal_factors=[round(s, 3) for s in self.seasonal]
        )
