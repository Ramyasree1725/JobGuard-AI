"""
Aetheris Robotics & Simulation: Autonomous Multi-Agent Swarm Dynamics
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Dict, Any, Optional, Sequence
from core.math.vectors import Vector3D


class SwarmAgent:
    """Individual autonomous mobile agent with perception sphere and steering behavior."""
    __slots__ = ('agent_id', 'position', 'velocity', 'acceleration', 'max_speed', 'max_force', 'radius')

    def __init__(
        self,
        agent_id: int,
        position: Vector3D,
        velocity: Optional[Vector3D] = None,
        max_speed: float = 3.0,
        max_force: float = 5.0,
        radius: float = 0.2
    ) -> None:
        self.agent_id = agent_id
        self.position = position
        self.velocity = velocity if velocity is not None else Vector3D.zero()
        self.acceleration = Vector3D.zero()
        self.max_speed = float(max_speed)
        self.max_force = float(max_force)
        self.radius = float(radius)

    def apply_force(self, force: Vector3D) -> None:
        self.acceleration += force

    def update(self, dt: float) -> None:
        # Clamp force
        if self.acceleration.norm() > self.max_force:
            self.acceleration = self.acceleration.normalize() * self.max_force

        self.velocity += self.acceleration * dt
        # Clamp speed
        if self.velocity.norm() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.position += self.velocity * dt
        self.acceleration = Vector3D.zero()


class MultiAgentSwarmEngine:
    """
    Decentralized multi-agent swarm controller implementing Reynolds flocking principles:
    1. Separation: Avoid crowding local flockmates
    2. Alignment: Steer towards the average heading of local flockmates
    3. Cohesion: Steer to move toward the average position of local flockmates
    4. Target Seeking & Obstacle Avoidance
    """
    def __init__(
        self,
        num_agents: int = 50,
        perception_radius: float = 2.5,
        separation_radius: float = 0.8,
        weight_separation: float = 2.0,
        weight_alignment: float = 1.0,
        weight_cohesion: float = 1.0,
        weight_target: float = 1.5,
        seed: Optional[int] = None
    ) -> None:
        self.perception_r = perception_radius
        self.separation_r = separation_radius
        self.w_sep = weight_separation
        self.w_ali = weight_alignment
        self.w_coh = weight_cohesion
        self.w_tgt = weight_target

        self.rng = random.Random(seed)
        self.agents: List[SwarmAgent] = []
        self._init_agents(num_agents)

    def _init_agents(self, count: int) -> None:
        self.agents.clear()
        for i in range(count):
            pos = Vector3D(
                self.rng.uniform(-10.0, 10.0),
                self.rng.uniform(-10.0, 10.0),
                self.rng.uniform(1.0, 10.0)
            )
            vel = Vector3D(
                self.rng.uniform(-1.0, 1.0),
                self.rng.uniform(-1.0, 1.0),
                self.rng.uniform(-0.5, 0.5)
            ).normalize() * 1.5
            self.agents.append(SwarmAgent(agent_id=i, position=pos, velocity=vel))

    def step(self, dt: float, target: Optional[Vector3D] = None) -> None:
        """Executes 1 simulation tick across all swarm agents."""
        n = len(self.agents)
        if n == 0 or dt <= 1e-6:
            return

        forces = [Vector3D.zero() for _ in range(n)]

        for i in range(n):
            agent_i = self.agents[i]
            sep_force = Vector3D.zero()
            ali_force = Vector3D.zero()
            coh_force = Vector3D.zero()

            neighbors_count = 0
            sep_count = 0
            center_of_mass = Vector3D.zero()
            avg_velocity = Vector3D.zero()

            for j in range(n):
                if i == j:
                    continue
                agent_j = self.agents[j]
                dist = agent_i.position.distance_to(agent_j.position)

                if dist < self.perception_r and dist > 1e-6:
                    neighbors_count += 1
                    center_of_mass += agent_j.position
                    avg_velocity += agent_j.velocity

                    if dist < self.separation_r:
                        # Inverse distance repulsive force
                        diff = (agent_i.position - agent_j.position).normalize()
                        sep_force += diff / dist
                        sep_count += 1

            if sep_count > 0:
                sep_force = (sep_force / float(sep_count)).normalize() * agent_i.max_speed - agent_i.velocity

            if neighbors_count > 0:
                # Alignment
                avg_velocity = (avg_velocity / float(neighbors_count)).normalize() * agent_i.max_speed
                ali_force = avg_velocity - agent_i.velocity

                # Cohesion
                center_of_mass = center_of_mass / float(neighbors_count)
                desired_to_center = (center_of_mass - agent_i.position).normalize() * agent_i.max_speed
                coh_force = desired_to_center - agent_i.velocity

            # Target Seeking
            tgt_force = Vector3D.zero()
            if target is not None:
                desired_tgt = (target - agent_i.position).normalize() * agent_i.max_speed
                tgt_force = desired_tgt - agent_i.velocity

            # Weighted sum
            total_force = (
                sep_force * self.w_sep +
                ali_force * self.w_ali +
                coh_force * self.w_coh +
                tgt_force * self.w_tgt
            )
            forces[i] = total_force

        # Apply forces and integrate
        for i in range(n):
            self.agents[i].apply_force(forces[i])
            self.agents[i].update(dt)

    def get_swarm_center(self) -> Vector3D:
        if not self.agents:
            return Vector3D.zero()
        return sum([a.position for a in self.agents], Vector3D.zero()) / float(len(self.agents))

    def to_state_list(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": a.agent_id,
                "position": a.position.to_list(),
                "velocity": a.velocity.to_list(),
                "speed": a.velocity.norm()
            }
            for a in self.agents
        ]
