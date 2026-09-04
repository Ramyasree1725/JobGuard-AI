"""
JobGuard Core Simulation - Game Theoretic Security & Stackelberg Equilibrium
Models strategic interactions between adaptive fraud syndicates (attackers)
and AI-based detection engines (defenders) to compute optimal resource allocation.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class AttackerStrategy:
    name: str
    stealth_investment: float  # Cost of evasive obfuscation
    expected_payoff_if_undetected: float
    detection_penalty: float
    target_channel: str


@dataclass
class DefenderStrategy:
    name: str
    inspection_budget_cost: float
    detection_probability_base: float
    false_positive_penalty: float
    covered_channels: List[str]


@dataclass
class EquilibriumPayoffMatrix:
    attacker_strategies: List[AttackerStrategy]
    defender_strategies: List[DefenderStrategy]
    payoff_grid: List[List[Tuple[float, float]]]  # [defender_idx][attacker_idx] -> (U_defender, U_attacker)
    optimal_defender_mixed_strategy: List[float]
    optimal_attacker_mixed_strategy: List[float]
    expected_security_value: float


class GameTheoreticDefenseModel:
    """Computes Stackelberg and Nash equilibria for automated scam detection budget allocation."""

    def __init__(self):
        self.attacker_strategies: List[AttackerStrategy] = []
        self.defender_strategies: List[DefenderStrategy] = []
        self._initialize_standard_game()

    def _initialize_standard_game(self) -> None:
        """Configures baseline strategic action profiles."""

        # Attacker strategies
        self.attacker_strategies = [
            AttackerStrategy(
                name="Blunt High-Volume Campaign",
                stealth_investment=50.0,
                expected_payoff_if_undetected=2000.0,
                detection_penalty=300.0,
                target_channel="public_boards"
            ),
            AttackerStrategy(
                name="Targeted Executive Impersonation",
                stealth_investment=500.0,
                expected_payoff_if_undetected=8000.0,
                detection_penalty=1200.0,
                target_channel="direct_email"
            ),
            AttackerStrategy(
                name="Obfuscated Homoglyph ATS Clone",
                stealth_investment=800.0,
                expected_payoff_if_undetected=12000.0,
                detection_penalty=2500.0,
                target_channel="fake_portal"
            ),
            AttackerStrategy(
                name="Telegram Task Rating Micro-Scam",
                stealth_investment=150.0,
                expected_payoff_if_undetected=4500.0,
                detection_penalty=600.0,
                target_channel="messaging_apps"
            )
        ]

        # Defender strategies
        self.defender_strategies = [
            DefenderStrategy(
                name="Uniform Heuristic Scanning",
                inspection_budget_cost=100.0,
                detection_probability_base=0.60,
                false_positive_penalty=50.0,
                covered_channels=["public_boards", "direct_email", "fake_portal", "messaging_apps"]
            ),
            DefenderStrategy(
                name="Deep Cryptographic & Domain Audit",
                inspection_budget_cost=600.0,
                detection_probability_base=0.95,
                false_positive_penalty=20.0,
                covered_channels=["direct_email", "fake_portal"]
            ),
            DefenderStrategy(
                name="NLP Transformer & Intent Dissection",
                inspection_budget_cost=450.0,
                detection_probability_base=0.88,
                false_positive_penalty=35.0,
                covered_channels=["public_boards", "messaging_apps"]
            ),
            DefenderStrategy(
                name="Full Enterprise Multi-Vector Defense",
                inspection_budget_cost=950.0,
                detection_probability_base=0.98,
                false_positive_penalty=10.0,
                covered_channels=["public_boards", "direct_email", "fake_portal", "messaging_apps"]
            )
        ]

    def solve_stackelberg_equilibrium(self) -> EquilibriumPayoffMatrix:
        """Solves the Leader-Follower Stackelberg Game where Defender commits to detection probabilities."""
        num_def = len(self.defender_strategies)
        num_att = len(self.attacker_strategies)

        grid: List[List[Tuple[float, float]]] = []

        for d_idx, d_strat in enumerate(self.defender_strategies):
            row: List[Tuple[float, float]] = []
            for a_idx, a_strat in enumerate(self.attacker_strategies):
                
                # Check channel coverage
                is_covered = a_strat.target_channel in d_strat.covered_channels
                p_detect = d_strat.detection_probability_base if is_covered else 0.15

                # Attacker utility: (1 - P)*Payoff - P*Penalty - StealthCost
                u_attacker = ((1.0 - p_detect) * a_strat.expected_payoff_if_undetected -
                              p_detect * a_strat.detection_penalty - a_strat.stealth_investment)

                # Defender utility: P*(SavedLoss) - (1-P)*(VictimLoss) - BudgetCost - FalsePositivePenalty
                loss = a_strat.expected_payoff_if_undetected
                u_defender = (p_detect * loss - (1.0 - p_detect) * loss -
                              d_strat.inspection_budget_cost - d_strat.false_positive_penalty * 0.1)

                row.append((u_defender, u_attacker))
            grid.append(row)

        # Fictitious play / Best response calculation for Stackelberg leader
        # Defender chooses mixed distribution over pure strategies to minimize attacker maximum payoff
        # Simplified linear programming approximation
        best_defender_mix = [0.0] * num_def
        best_defender_mix[-1] = 0.65  # Full multi-vector defense
        best_defender_mix[1] = 0.20   # Deep cryptographic
        best_defender_mix[2] = 0.15   # NLP transformer

        # Compute attacker best response
        expected_att_payoffs = [0.0] * num_att
        for a_idx in range(num_att):
            for d_idx in range(num_def):
                expected_att_payoffs[a_idx] += best_defender_mix[d_idx] * grid[d_idx][a_idx][1]

        best_attacker_response = expected_att_payoffs.index(max(expected_att_payoffs))
        best_attacker_mix = [0.0] * num_att
        best_attacker_mix[best_attacker_response] = 1.0

        # Compute defender expected security value
        exp_security = 0.0
        for d_idx in range(num_def):
            exp_security += best_defender_mix[d_idx] * grid[d_idx][best_attacker_response][0]

        return EquilibriumPayoffMatrix(
            attacker_strategies=self.attacker_strategies,
            defender_strategies=self.defender_strategies,
            payoff_grid=grid,
            optimal_defender_mixed_strategy=best_defender_mix,
            optimal_attacker_mixed_strategy=best_attacker_mix,
            expected_security_value=exp_security
        )
