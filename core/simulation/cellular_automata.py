"""
JobGuard Core Simulation - 2D Cellular Automata & Epidemic Fraud Propagation
Models contagion spreading of WhatsApp task scams across peer networks.
"""

from typing import List, Tuple, Dict, Optional


class EpidemicContagionAutomaton:
    """Susceptible-Infectious-Recovered (SIR) 2D Grid Cellular Automaton."""

    SUSCEPTIBLE = 0
    INFECTIOUS = 1
    RECOVERED = 2

    def __init__(self, width: int = 20, height: int = 20, infection_prob: float = 0.3, recovery_prob: float = 0.1):
        self.w = width
        self.h = height
        self.beta = infection_prob
        self.gamma = recovery_prob
        self.grid = [[self.SUSCEPTIBLE] * width for _ in range(height)]
        # Seed infection at center
        self.grid[height // 2][width // 2] = self.INFECTIOUS

    def step(self) -> Dict[str, int]:
        new_grid = [[self.grid[r][c] for c in range(self.w)] for r in range(self.h)]
        stats = {"susceptible": 0, "infectious": 0, "recovered": 0}

        for r in range(self.h):
            for c in range(self.w):
                state = self.grid[r][c]
                if state == self.SUSCEPTIBLE:
                    # Count infectious neighbors
                    inf_neighbors = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.h and 0 <= nc < self.w:
                                if self.grid[nr][nc] == self.INFECTIOUS:
                                    inf_neighbors += 1
                    
                    if inf_neighbors > 0 and random.random() < (1.0 - (1.0 - self.beta) ** inf_neighbors):
                        new_grid[r][c] = self.INFECTIOUS
                elif state == self.INFECTIOUS:
                    if random.random() < self.gamma:
                        new_grid[r][c] = self.RECOVERED

                # Count stats
                final_state = new_grid[r][c]
                if final_state == self.SUSCEPTIBLE:
                    stats["susceptible"] += 1
                elif final_state == self.INFECTIOUS:
                    stats["infectious"] += 1
                else:
                    stats["recovered"] += 1

        self.grid = new_grid
        return stats
