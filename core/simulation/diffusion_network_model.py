"""
JobGuard Core Simulation - Diffusion Network & Viral Contagion Engine
Models the viral propagation, reposting dynamics, and syndicate syndication
of fraudulent job offers across heterogeneous social and professional networks.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


@dataclass
class NetworkNode:
    node_id: str
    network_type: str  # 'linkedin', 'telegram', 'facebook_group', 'job_board', 'discord'
    followers_count: int
    repost_probability: float
    verification_tier: float  # 0.0 (unverified) to 1.0 (strict moderator)
    state: str = "SUSCEPTIBLE"  # SUSCEPTIBLE, EXPOSED, INFECTED (reposting scam), RECOVERED (flagged/removed)
    neighbors: List[str] = field(default_factory=list)


@dataclass
class DiffusionStepSummary:
    step_index: int
    susceptible_count: int
    exposed_count: int
    infected_count: int
    recovered_count: int
    new_infections: int
    total_impressions: int


@dataclass
class NetworkDiffusionReport:
    total_steps: int
    peak_infected: int
    total_reached_users: int
    effective_reproduction_number_r0: float
    platform_vulnerability_index: Dict[str, float]
    step_history: List[DiffusionStepSummary]


class DiffusionNetworkModel:
    """Epidemiological SEIR-based simulation of viral scam propagation across social platforms."""

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)
        self.nodes: Dict[str, NetworkNode] = {}

    def generate_scale_free_network(self, num_nodes: int = 500, m_edges: int = 3) -> None:
        """Generates a Barabasi-Albert scale-free network representing social channels and job boards."""
        self.nodes.clear()
        platform_types = ["linkedin", "telegram", "facebook_group", "job_board", "discord"]

        # Initial seed clique
        for i in range(m_edges + 1):
            p_type = random.choice(platform_types)
            node = NetworkNode(
                node_id=f"NODE_{i:04d}",
                network_type=p_type,
                followers_count=random.randint(50, 500),
                repost_probability=random.uniform(0.05, 0.25),
                verification_tier=random.uniform(0.2, 0.9)
            )
            self.nodes[node.node_id] = node

        for i in range(m_edges + 1):
            for j in range(m_edges + 1):
                if i != j:
                    self.nodes[f"NODE_{i:04d}"].neighbors.append(f"NODE_{j:04d}")

        # Preferential attachment
        for i in range(m_edges + 1, num_nodes):
            p_type = random.choice(platform_types)
            
            # Moderation tiers by platform
            if p_type == "linkedin":
                verification = random.uniform(0.6, 0.95)
                followers = int(random.paretovariate(1.5) * 200)
            elif p_type == "telegram":
                verification = random.uniform(0.05, 0.3)
                followers = int(random.paretovariate(1.2) * 500)
            elif p_type == "facebook_group":
                verification = random.uniform(0.1, 0.45)
                followers = int(random.paretovariate(1.3) * 1000)
            else:
                verification = random.uniform(0.3, 0.7)
                followers = int(random.paretovariate(1.4) * 300)

            node_id = f"NODE_{i:04d}"
            new_node = NetworkNode(
                node_id=node_id,
                network_type=p_type,
                followers_count=max(20, min(100000, followers)),
                repost_probability=random.uniform(0.02, 0.30),
                verification_tier=verification
            )
            self.nodes[node_id] = new_node

            # Select m_edges targets with probability proportional to degree
            all_existing = list(self.nodes.keys())[:-1]
            degrees = [len(self.nodes[nid].neighbors) for nid in all_existing]
            total_degree = max(1, sum(degrees))
            probs = [d / total_degree for d in degrees]

            chosen = set()
            while len(chosen) < min(m_edges, len(all_existing)):
                # Weighted sampling
                r = random.random()
                cum = 0.0
                for idx, p in enumerate(probs):
                    cum += p
                    if r <= cum:
                        chosen.add(all_existing[idx])
                        break

            for target in chosen:
                self.nodes[node_id].neighbors.append(target)
                self.nodes[target].neighbors.append(node_id)

    def simulate_propagation(
        self,
        initial_infected_count: int = 5,
        beta_transmission: float = 0.45,
        gamma_recovery_daily: float = 0.20,
        jobguard_moderator_efficacy: float = 0.75,
        max_steps: int = 40
    ) -> NetworkDiffusionReport:
        """Executes stochastic discrete-time SEIR propagation simulation."""
        if not self.nodes:
            self.generate_scale_free_network(500)

        # Reset states
        for node in self.nodes.values():
            node.state = "SUSCEPTIBLE"

        # Seed initial infections (fraudulent post originators)
        all_ids = list(self.nodes.keys())
        infected_seeds = random.sample(all_ids, min(initial_infected_count, len(all_ids)))
        for nid in infected_seeds:
            self.nodes[nid].state = "INFECTED"

        history: List[DiffusionStepSummary] = []
        peak_infected = len(infected_seeds)
        total_impressions = 0
        total_secondary_infections = 0

        for step in range(1, max_steps + 1):
            new_infected: Set[str] = set()
            new_recovered: Set[str] = set()

            # Process active infected nodes
            for nid, node in self.nodes.items():
                if node.state == "INFECTED":
                    total_impressions += node.followers_count
                    
                    # Spread to susceptible neighbors
                    for neighbor_id in node.neighbors:
                        neighbor = self.nodes[neighbor_id]
                        if neighbor.state == "SUSCEPTIBLE":
                            # Effective infection probability
                            # Higher verification tier decreases infection
                            p_infect = (beta_transmission * neighbor.repost_probability *
                                        (1.0 - neighbor.verification_tier * jobguard_moderator_efficacy))
                            if random.random() < p_infect:
                                new_infected.add(neighbor_id)
                                total_secondary_infections += 1

                    # Check recovery (flagged / taken down)
                    p_recover = gamma_recovery_daily + (node.verification_tier * jobguard_moderator_efficacy * 0.3)
                    if random.random() < min(0.95, p_recover):
                        new_recovered.add(nid)

            # Apply state updates
            for nid in new_infected:
                self.nodes[nid].state = "INFECTED"
            for nid in new_recovered:
                self.nodes[nid].state = "RECOVERED"

            # Compute census
            s_count = sum(1 for n in self.nodes.values() if n.state == "SUSCEPTIBLE")
            e_count = 0  # Simplified SEIR
            i_count = sum(1 for n in self.nodes.values() if n.state == "INFECTED")
            r_count = sum(1 for n in self.nodes.values() if n.state == "RECOVERED")

            peak_infected = max(peak_infected, i_count)

            history.append(DiffusionStepSummary(
                step_index=step,
                susceptible_count=s_count,
                exposed_count=e_count,
                infected_count=i_count,
                recovered_count=r_count,
                new_infections=len(new_infected),
                total_impressions=total_impressions
            ))

            if i_count == 0:
                break

        # Calculate R0 estimate
        r0 = (total_secondary_infections / max(1, initial_infected_count))

        # Calculate platform vulnerability
        platform_vuln: Dict[str, float] = {}
        for p in ["linkedin", "telegram", "facebook_group", "job_board", "discord"]:
            p_nodes = [n for n in self.nodes.values() if n.network_type == p]
            if p_nodes:
                inf_count = sum(1 for n in p_nodes if n.state in ("INFECTED", "RECOVERED"))
                platform_vuln[p] = (inf_count / len(p_nodes)) * 100.0
            else:
                platform_vuln[p] = 0.0

        return NetworkDiffusionReport(
            total_steps=len(history),
            peak_infected=peak_infected,
            total_reached_users=total_impressions,
            effective_reproduction_number_r0=r0,
            platform_vulnerability_index=platform_vuln,
            step_history=history
        )
