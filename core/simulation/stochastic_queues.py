"""
JobGuard Core Simulation - M/M/1 and M/M/k Kendall Queueing Networks
Calculates steady-state probabilities, average queue lengths, and waiting time distributions.
"""

import math
from typing import List, Tuple, Dict, Optional


class QueueingNetworkModel:
    """Analytical M/M/1 and M/M/k queue formulas."""

    @staticmethod
    def mm1_metrics(arrival_rate_lambda: float, service_rate_mu: float) -> Dict[str, float]:
        """Calculates performance metrics for M/M/1 queue."""
        if arrival_rate_lambda >= service_rate_mu:
            raise ValueError("Queue is unstable (lambda >= mu)")

        rho = arrival_rate_lambda / service_rate_mu  # Utilization
        L = rho / (1.0 - rho)                        # Average customers in system
        Lq = (rho ** 2) / (1.0 - rho)                # Average customers in queue
        W = 1.0 / (service_rate_mu - arrival_rate_lambda) # Average response time
        Wq = rho / (service_rate_mu - arrival_rate_lambda) # Average wait time in queue

        return {
            "traffic_intensity_rho": round(rho, 4),
            "avg_customers_system_L": round(L, 3),
            "avg_customers_queue_Lq": round(Lq, 3),
            "avg_time_system_W": round(W, 4),
            "avg_time_queue_Wq": round(Wq, 4)
        }
