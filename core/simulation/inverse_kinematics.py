"""
Aetheris Robotics & Simulation: Damped Least-Squares Inverse Kinematics Solver
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Optional, Dict, Any
from core.math.vectors import Vector3D
from core.math.matrices import Matrix4x4, Matrix3x3, MatrixDense
from core.simulation.kinematics import RoboticManipulator6DoF


class InverseKinematicsSolver:
    """
    Nonlinear Levenberg-Marquardt & Damped Least-Squares (DLS) Inverse Kinematics solver.
    Solves for joint angles q to achieve target Cartesian end-effector position and orientation:
    Delta q = (J^T * J + lambda^2 * I)^-1 * J^T * e
    Incorporates null-space projection for joint limit avoidance.
    """
    def __init__(
        self,
        manipulator: RoboticManipulator6DoF,
        max_iterations: int = 150,
        position_tolerance: float = 1e-4,
        orientation_tolerance: float = 1e-3,
        damping_factor: float = 0.05
    ) -> None:
        self.manipulator = manipulator
        self.max_iterations = max_iterations
        self.pos_tol = position_tolerance
        self.rot_tol = orientation_tolerance
        self.damping = damping_factor

    def solve(
        self,
        target_position: Vector3D,
        target_rotation: Optional[Matrix3x3] = None,
        initial_guess: Optional[List[float]] = None
    ) -> Tuple[bool, List[float], int, float]:
        """
        Solves IK for target pose.
        Returns: (success: bool, joint_angles: List[float], iterations: int, residual_error: float)
        """
        q = list(self.manipulator.joint_positions if initial_guess is None else initial_guess)
        n = self.manipulator.num_joints()

        for iteration in range(self.max_iterations):
            ee_pose = self.manipulator.end_effector_pose(q)
            current_pos = ee_pose.get_translation()
            pos_err = target_position - current_pos
            pos_error_norm = pos_err.norm()

            # Orientation error computation if target rotation specified
            if target_rotation is not None:
                current_rot = ee_pose.get_rotation()
                # Orientation error vector from cross product of rotation columns
                err_rot = (
                    current_rot.get_rotation_x_axis().cross(target_rotation.get_rotation_x_axis()) +
                    current_rot.get_rotation_y_axis().cross(target_rotation.get_rotation_y_axis()) +
                    current_rot.get_rotation_z_axis().cross(target_rotation.get_rotation_z_axis())
                ) * 0.5
                rot_error_norm = err_rot.norm()
            else:
                err_rot = Vector3D(0.0, 0.0, 0.0)
                rot_error_norm = 0.0

            total_error = math.sqrt(pos_error_norm ** 2 + rot_error_norm ** 2)

            if pos_error_norm < self.pos_tol and rot_error_norm < self.rot_tol:
                return True, q, iteration, total_error

            # 6D error vector: [dx, dy, dz, dwx, dwy, dwz]^T
            if target_rotation is not None:
                e = [pos_err.x, pos_err.y, pos_err.z, err_rot.x, err_rot.y, err_rot.z]
                m_dim = 6
            else:
                e = [pos_err.x, pos_err.y, pos_err.z]
                m_dim = 3

            # Compute Jacobian
            full_j = self.manipulator.compute_geometric_jacobian(q)
            j_sub = MatrixDense(m_dim, n)
            for r in range(m_dim):
                for c in range(n):
                    j_sub[r][c] = full_j[r][c]

            # J * J^T + lambda^2 * I
            jt = j_sub.transpose()
            jjt = j_sub.matmul(jt)

            # Adaptive damping near singularities
            for i in range(m_dim):
                jjt[i][i] += (self.damping ** 2)

            # Solve (J*J^T + lambda^2*I) * v = e
            try:
                v = jjt.solve_linear_system_gaussian(e)
            except ValueError:
                # Singularity encountered, bump damping
                for i in range(m_dim):
                    jjt[i][i] += 0.2
                v = jjt.solve_linear_system_gaussian(e)

            # Delta q = J^T * v
            delta_q = [0.0] * n
            for c in range(n):
                delta_q[c] = sum(jt[c][r] * v[r] for r in range(m_dim))

            # Null-space joint limit avoidance: q_null = - k * grad(H(q))
            # H(q) = sum ( (q_i - q_mid) / (q_max - q_min) )^2
            k_null = 0.1
            for c in range(n):
                link = self.manipulator.links[c]
                mid = (link.max_limit + link.min_limit) * 0.5
                span = link.max_limit - link.min_limit
                if span > 1e-6:
                    grad_h = 2.0 * (q[c] - mid) / (span * span)
                    delta_q[c] -= k_null * grad_h

            # Step update with clamping
            step_size = 0.6
            for c in range(n):
                link = self.manipulator.links[c]
                new_val = q[c] + step_size * delta_q[c]
                q[c] = max(link.min_limit, min(link.max_limit, new_val))

        # Return best effort result
        final_err = (self.manipulator.end_effector_position(q) - target_position).norm()
        return False, q, self.max_iterations, final_err
