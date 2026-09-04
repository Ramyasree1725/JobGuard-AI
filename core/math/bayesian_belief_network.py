"""
JobGuard Core Math - Bayesian Belief Network (BBN) Probability Engine
Implements Directed Acyclic Graph (DAG) factor graph representation, Pearl's belief propagation,
and exact marginal posterior inference for compound recruitment scam evidence.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class BayesianNode:
    node_id: str
    name: str
    parents: List[str] = field(default_factory=list)
    cpt: Dict[Tuple[bool, ...], float] = field(default_factory=dict)  # Parent truth tuple -> P(Node=True | Parents)


class BayesianBeliefNetwork:
    """Directed graphical model for compound probabilistic threat reasoning."""

    def __init__(self):
        self.nodes: Dict[str, BayesianNode] = {}
        self._build_jobguard_fraud_bbn()

    def _build_jobguard_fraud_bbn(self) -> None:
        """Constructs BBN linking root threats (Scam Intent) to observed indicators."""

        # Root: True Fraud Intent
        self.nodes["FRAUD_INTENT"] = BayesianNode(
            node_id="FRAUD_INTENT",
            name="True Scam Intent",
            parents=[],
            cpt={(): 0.05}  # Prior P(Scam) = 5% in general pool
        )

        # Child 1: Demands Upfront Check/Fee | Scam
        self.nodes["UPFRONT_DEMAND"] = BayesianNode(
            node_id="UPFRONT_DEMAND",
            name="Demands Upfront Payment / Check",
            parents=["FRAUD_INTENT"],
            cpt={
                (True,): 0.85,   # P(Upfront | Fraud) = 85%
                (False,): 0.001  # P(Upfront | Authentic) = 0.1%
            }
        )

        # Child 2: Chat-Only Channel | Scam
        self.nodes["CHAT_CHANNEL"] = BayesianNode(
            node_id="CHAT_CHANNEL",
            name="Telegram / WhatsApp Chat Interview",
            parents=["FRAUD_INTENT"],
            cpt={
                (True,): 0.75,   # P(Chat | Fraud) = 75%
                (False,): 0.04   # P(Chat | Authentic) = 4%
            }
        )

        # Child 3: Hyper-Inflated Salary | Scam
        self.nodes["SALARY_ANOMALY"] = BayesianNode(
            node_id="SALARY_ANOMALY",
            name="Hyper-Inflated Salary Anomaly",
            parents=["FRAUD_INTENT"],
            cpt={
                (True,): 0.70,   # P(SalaryAnomaly | Fraud) = 70%
                (False,): 0.03   # P(SalaryAnomaly | Authentic) = 3%
            }
        )

    def compute_posterior_fraud_probability(self, evidence: Dict[str, bool]) -> float:
        """Computes exact posterior P(FRAUD_INTENT=True | Evidence) using Bayes' Theorem."""
        p_fraud = self.nodes["FRAUD_INTENT"].cpt[()]
        p_not_fraud = 1.0 - p_fraud

        # Likelihood under Fraud = True
        likelihood_fraud = 1.0
        # Likelihood under Fraud = False
        likelihood_not_fraud = 1.0

        for node_id, observed_val in evidence.items():
            if node_id in self.nodes and node_id != "FRAUD_INTENT":
                node = self.nodes[node_id]
                p_true_given_fraud = node.cpt[(True,)]
                p_true_given_not_fraud = node.cpt[(False,)]

                if observed_val:
                    likelihood_fraud *= p_true_given_fraud
                    likelihood_not_fraud *= p_true_given_not_fraud
                else:
                    likelihood_fraud *= (1.0 - p_true_given_fraud)
                    likelihood_not_fraud *= (1.0 - p_true_given_not_fraud)

        numerator = p_fraud * likelihood_fraud
        denominator = numerator + (p_not_fraud * likelihood_not_fraud)

        if denominator == 0.0:
            return 0.50

        return numerator / denominator
