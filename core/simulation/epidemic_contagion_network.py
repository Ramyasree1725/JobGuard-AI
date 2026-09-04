"""
JobGuard Core Simulation - Epidemic Contagion & Viral Hoax Propagation Network
Simulates SEIR (Susceptible-Exposed-Infectious-Recovered) network spreading models
for analyzing viral fake job post propagation across social communication graphs.
"""

import random
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class NetworkNode:
    node_id: str
    state: str  # "S", "E", "I", "R"
    neighbors: List[str] = field(default_factory=list)
    viral_receptivity: float = 0.5
    time_in_state: int = 0


class ViralContagionSimulator:
    """Network-level SEIR epidemic propagation model."""

    def __init__(
        self,
        num_nodes: int = 200,
        beta_infection_rate: float = 0.3,
        sigma_latency_rate: float = 0.2,
        gamma_recovery_rate: float = 0.1
    ):
        self.beta = beta_infection_rate
        self.sigma = sigma_latency_rate
        self.gamma = gamma_recovery_rate
        self.nodes: Dict[str, NetworkNode] = {}
        self._build_small_world_graph(num_nodes)

    def _build_small_world_graph(self, num_nodes: int, k_nearest: int = 4) -> None:
        """Watts-Strogatz small-world network topology."""
        for i in range(num_nodes):
            nid = f"USER_{i:04d}"
            # Ring lattice connections
            neighbors = [f"USER_{(i + j) % num_nodes:04d}" for j in range(1, k_nearest // 2 + 1)]
            neighbors += [f"USER_{(i - j) % num_nodes:04d}" for j in range(1, k_nearest // 2 + 1)]
            self.nodes[nid] = NetworkNode(node_id=nid, state="S", neighbors=neighbors)

        # Seed initial infectious nodes
        self.nodes["USER_0000"].state = "I"
        self.nodes["USER_0001"].state = "I"

    def step(self) -> Dict[str, int]:
        """Advance one viral dissemination cycle."""
        counts = {"S": 0, "E": 0, "I": 0, "R": 0}
        next_states: Dict[str, str] = {}

        for nid, node in self.nodes.items():
            node.time_in_state += 1
            if node.state == "S":
                # Infection pressure from infectious neighbors
                inf_neighbors = sum(1 for neigh in node.neighbors if self.nodes[neigh].state == "I")
                prob_infected = 1.0 - ((1.0 - self.beta * node.viral_receptivity) ** inf_neighbors)
                if random.random() < prob_infected:
                    next_states[nid] = "E"
                else:
                    next_states[nid] = "S"

            elif node.state == "E":
                if random.random() < self.sigma:
                    next_states[nid] = "I"
                else:
                    next_states[nid] = "E"

            elif node.state == "I":
                if random.random() < self.gamma:
                    next_states[nid] = "R"
                else:
                    next_states[nid] = "I"

            else:
                next_states[nid] = "R"

        for nid, state in next_states.items():
            self.nodes[nid].state = state
            counts[state] += 1

        return counts
