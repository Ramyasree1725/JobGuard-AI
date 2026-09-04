"""
JobGuard Core Optimization - Ant Colony Optimization (ACO)
Solves discrete graph path routing and minimum-cost threat investigation paths
via pheromone trail updating and heuristic attractiveness.
"""

import math
import random
from typing import List, Tuple, Dict, Optional


class AntColonyOptimizer:
    """Ant System (AS) for graph path and sequence optimization."""

    def __init__(
        self,
        distance_matrix: List[List[float]],
        num_ants: int = 20,
        alpha: float = 1.0,  # Pheromone importance
        beta: float = 2.0,   # Distance priority
        evaporation_rate: float = 0.5,
        q: float = 100.0
    ):
        self.distances = distance_matrix
        self.num_nodes = len(distance_matrix)
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = evaporation_rate
        self.q = q
        
        # Initial pheromone matrix
        self.pheromones = [[1.0] * self.num_nodes for _ in range(self.num_nodes)]

    def run(self, iterations: int = 50) -> Tuple[List[int], float]:
        best_path: List[int] = []
        best_dist = float("inf")

        for _ in range(iterations):
            paths = []
            lengths = []

            for _ in range(self.num_ants):
                path = self._construct_path()
                dist = self._path_distance(path)
                paths.append(path)
                lengths.append(dist)

                if dist < best_dist:
                    best_dist = dist
                    best_path = path

            # Evaporation
            for i in range(self.num_nodes):
                for j in range(self.num_nodes):
                    self.pheromones[i][j] *= (1.0 - self.rho)

            # Deposit pheromones
            for path, dist in zip(paths, lengths):
                deposit = self.q / max(1e-4, dist)
                for step in range(len(path) - 1):
                    u, v = path[step], path[step + 1]
                    self.pheromones[u][v] += deposit
                    self.pheromones[v][u] += deposit

        return best_path, best_dist

    def _construct_path(self) -> List[int]:
        unvisited = set(range(self.num_nodes))
        curr = random.randint(0, self.num_nodes - 1)
        unvisited.remove(curr)
        path = [curr]

        while unvisited:
            weights = []
            candidates = list(unvisited)
            for cand in candidates:
                tau = self.pheromones[curr][cand] ** self.alpha
                eta = (1.0 / max(1e-4, self.distances[curr][cand])) ** self.beta
                weights.append(tau * eta)

            total_w = sum(weights)
            if total_w == 0:
                next_node = random.choice(candidates)
            else:
                probs = [w / total_w for w in weights]
                r = random.random()
                cum = 0.0
                next_node = candidates[-1]
                for idx, p in enumerate(probs):
                    cum += p
                    if r <= cum:
                        next_node = candidates[idx]
                        break

            path.append(next_node)
            unvisited.remove(next_node)
            curr = next_node

        return path

    def _path_distance(self, path: List[int]) -> float:
        total = 0.0
        for i in range(len(path) - 1):
            total += self.distances[path[i]][path[i + 1]]
        return total
