"""
Aetheris Robotics & Simulation: 6-DoF Rigid Body Physical State Integrator
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import Dict, Any, Optional
from core.math.vectors import Vector3D
from core.math.matrices import Matrix3x3
from core.math.quaternions import Quaternion
from core.math.integrators import NumericalIntegrator


class RigidBody6DoF:
    """
    6-Degree-of-Freedom rigid body dynamics simulator.
    Integrates linear momentum: m * v_dot = F_net
    Integrates angular momentum: I * omega_dot + omega x (I * omega) = Tau_net
    Quaternion attitude kinematics: q_dot = 0.5 * q * [0, omega]
    """
    def __init__(
        self,
        name: str = "drone_body",
        mass: float = 1.5,
        inertia_tensor: Optional[Matrix3x3] = None,
        drag_linear_coeff: float = 0.05,
        drag_angular_coeff: float = 0.02
    ) -> None:
        self.name = name
        self.mass = max(0.01, float(mass))
        self.inv_mass = 1.0 / self.mass

        if inertia_tensor is None:
            # Default diagonal inertia for symmetric body
            self.inertia = Matrix3x3([
                [0.05, 0.0,  0.0],
                [0.0,  0.05, 0.0],
                [0.0,  0.0,  0.09]
            ])
        else:
            self.inertia = inertia_tensor

        self.inv_inertia = self.inertia.inverse()
        self.drag_linear = drag_linear_coeff
        self.drag_angular = drag_angular_coeff

        # State vectors
        self.position = Vector3D(0.0, 0.0, 0.0)
        self.linear_velocity = Vector3D(0.0, 0.0, 0.0)
        self.orientation = Quaternion.identity()
        self.angular_velocity = Vector3D(0.0, 0.0, 0.0) # in body frame

        # Applied forces & torques
        self.accumulated_force = Vector3D(0.0, 0.0, 0.0) # world frame
        self.accumulated_torque = Vector3D(0.0, 0.0, 0.0) # body frame

    def apply_force_world(self, force: Vector3D) -> None:
        self.accumulated_force += force

    def apply_force_body(self, force: Vector3D) -> None:
        """Applies force in body coordinates, transformed to world frame."""
        world_f = self.orientation.rotate_vector(force)
        self.accumulated_force += world_f

    def apply_torque_body(self, torque: Vector3D) -> None:
        self.accumulated_torque += torque

    def clear_forces(self) -> None:
        self.accumulated_force = Vector3D(0.0, 0.0, 0.0)
        self.accumulated_torque = Vector3D(0.0, 0.0, 0.0)

    def step(self, dt: float, gravity: float = 9.81) -> None:
        """Integrates physical equations of motion over timestep dt."""
        if dt <= 1e-6:
            return

        # Linear dynamics
        gravity_force = Vector3D(0.0, 0.0, -self.mass * gravity)
        drag_force = self.linear_velocity * (-self.drag_linear * self.linear_velocity.norm())
        total_force = self.accumulated_force + gravity_force + drag_force

        linear_acceleration = total_force * self.inv_mass
        self.linear_velocity += linear_acceleration * dt
        self.position += self.linear_velocity * dt

        # Angular dynamics in body frame (Euler's equations):
        # I * d_omega/dt = Tau - omega x (I * omega) - drag
        i_omega = self.inertia * self.angular_velocity
        gyroscopic_torque = self.angular_velocity.cross(i_omega)
        angular_drag = self.angular_velocity * (-self.drag_angular * self.angular_velocity.norm())
        
        total_torque = self.accumulated_torque - gyroscopic_torque + angular_drag
        angular_acceleration = self.inv_inertia * total_torque

        self.angular_velocity += angular_acceleration * dt

        # Integrate attitude quaternion
        # q_dot = 0.5 * q * [0, wx, wy, wz]
        w_quat = Quaternion(0.0, self.angular_velocity.x, self.angular_velocity.y, self.angular_velocity.z)
        q_dot = (self.orientation * w_quat) * 0.5
        
        self.orientation = Quaternion(
            self.orientation.w + q_dot.w * dt,
            self.orientation.x + q_dot.x * dt,
            self.orientation.y + q_dot.y * dt,
            self.orientation.z + q_dot.z * dt
        ).normalize()

        self.clear_forces()

    def to_dict(self) -> Dict[str, Any]:
        yaw, pitch, roll = self.orientation.to_euler_zyx()
        return {
            "name": self.name,
            "position": self.position.to_list(),
            "velocity": self.linear_velocity.to_list(),
            "orientation_quat": [self.orientation.w, self.orientation.x, self.orientation.y, self.orientation.z],
            "euler_degrees": [math.degrees(yaw), math.degrees(pitch), math.degrees(roll)],
            "angular_velocity": self.angular_velocity.to_list(),
            "speed": self.linear_velocity.norm()
        }
