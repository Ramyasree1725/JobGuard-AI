"""
JobGuard Core Simulation - Macroeconomic Labor Dynamics & Beveridge Curve Econometrics
Simulates aggregate matching functions, labor market tightness, Okun's Law GDP fluctuations,
and wage Phillips Curve inflation feedback across multi-sector economies.
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class MacroEconomicState:
    period: int
    unemployment_rate_u: float
    vacancy_rate_v: float
    labor_market_tightness_theta: float
    output_gdp_billions: float
    inflation_rate_pi: float
    nominal_wage_index: float


class MacroLaborDynamicsSimulator:
    """Dynamic Stochastic General Equilibrium (DSGE) simplified labor block simulator."""

    def __init__(
        self,
        initial_unemployment: float = 0.05,
        initial_vacancies: float = 0.04,
        productivity_trend_growth: float = 0.02,
        matching_elasticity_alpha: float = 0.5
    ):
        self.u = initial_unemployment
        self.v = initial_vacancies
        self.growth = productivity_trend_growth
        self.alpha = matching_elasticity_alpha
        self.gdp = 20000.0  # Billion USD
        self.wage_index = 100.0
        self.inflation = 0.02
        self.history: List[MacroEconomicState] = []

    def step(self, shock_productivity: float = 0.0) -> MacroEconomicState:
        """Simulate one quarterly macroeconomic cycle."""
        period_idx = len(self.history) + 1
        
        # Labor tightness theta = v / u
        theta = self.v / max(0.001, self.u)

        # Job finding rate f(theta) = theta^(1 - alpha)
        job_finding_rate = theta ** (1.0 - self.alpha)
        separation_rate = 0.03

        # Unemployment law of motion: u_{t+1} = u_t + s*(1 - u_t) - f(theta)*u_t
        next_u = self.u + separation_rate * (1.0 - self.u) - job_finding_rate * self.u
        self.u = max(0.01, min(0.30, next_u))

        # Vacancies respond positively to productivity shocks
        self.v = max(0.01, min(0.20, 0.04 * (1.0 + shock_productivity) + 0.5 * (self.v - 0.04)))

        # Output via Okun's Law: dY/Y = growth - 2 * dU
        gdp_growth = self.growth - 2.0 * (self.u - (self.history[-1].unemployment_rate_u if self.history else self.u))
        self.gdp *= (1.0 + gdp_growth)

        # Wage Phillips Curve: dW/W = inflation + 0.5*(1/u - 1/0.05)
        wage_growth = self.inflation + 0.1 * (0.05 / max(0.01, self.u) - 1.0)
        self.wage_index *= (1.0 + wage_growth)

        state = MacroEconomicState(
            period=period_idx,
            unemployment_rate_u=round(self.u, 4),
            vacancy_rate_v=round(self.v, 4),
            labor_market_tightness_theta=round(theta, 3),
            output_gdp_billions=round(self.gdp, 2),
            inflation_rate_pi=round(self.inflation, 4),
            nominal_wage_index=round(self.wage_index, 2)
        )
        self.history.append(state)
        return state
