"""
Aetheris Robotics & Simulation: 6-DoF Forward Kinematics & Manipulator Dynamics
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Sequence, Optional, Dict, Any
from core.math.vectors import Vector3D
from core.math.matrices import Matrix4x4, Matrix3x3, MatrixDense


class DHParameter:
    """
    Standard Denavit-Hartenberg parameters for a single robotic joint link:
    a_i: link length (meters)
    alpha_i: link twist (radians)
    d_i: link offset (meters)
    theta_i: joint angle (radians)
    is_revolute: True for rotational joint, False for prismatic
    """
    __slots__ = ('a', 'alpha', 'd', 'theta_offset', 'is_revolute', 'min_limit', 'max_limit', 'joint_name')

    def __init__(
        self,
        a: float,
        alpha: float,
        d: float,
        theta_offset: float = 0.0,
        is_revolute: bool = True,
        min_limit: float = -math.pi,
        max_limit: float = math.pi,
        joint_name: str = "joint"
    ) -> None:
        self.a = float(a)
        self.alpha = float(alpha)
        self.d = float(d)
        self.theta_offset = float(theta_offset)
        self.is_revolute = is_revolute
        self.min_limit = float(min_limit)
        self.max_limit = float(max_limit)
        self.joint_name = joint_name

    def compute_transform(self, joint_val: float) -> Matrix4x4:
        """Calculates 4x4 homogenous matrix A_i for given joint value."""
        clamped_val = max(self.min_limit, min(self.max_limit, joint_val))
        if self.is_revolute:
            theta = self.theta_offset + clamped_val
            d = self.d
        else:
            theta = self.theta_offset
            d = self.d + clamped_val
        return Matrix4x4.from_dh_parameters(self.a, self.alpha, d, theta)


class RoboticManipulator6DoF:
    """
    Industrial & Research 6-Degree-of-Freedom Articulated Manipulator Robot.
    Implements standard and modified DH kinematics, frame chain propagation,
    analytical and geometric Jacobian computation for velocity and force control.
    """
    def __init__(self, name: str = "Aetheris-Arm-6R") -> None:
        self.name = name
        self.links: List[DHParameter] = [
            # Standard Universal-type 6-DoF DH parameters (e.g. UR5/KUKA style research arm)
            DHParameter(a=0.0,    alpha=math.pi / 2.0, d=0.1625, joint_name="base_pan", min_limit=-2*math.pi, max_limit=2*math.pi),
            DHParameter(a=-0.425, alpha=0.0,           d=0.0,    joint_name="shoulder_lift", min_limit=-math.pi, max_limit=math.pi),
            DHParameter(a=-0.3922,alpha=0.0,           d=0.0,    joint_name="elbow", min_limit=-math.pi, max_limit=math.pi),
            DHParameter(a=0.0,    alpha=math.pi / 2.0, d=0.1333, joint_name="wrist_1", min_limit=-2*math.pi, max_limit=2*math.pi),
            DHParameter(a=0.0,    alpha=-math.pi / 2.0,d=0.0997, joint_name="wrist_2", min_limit=-2*math.pi, max_limit=2*math.pi),
            DHParameter(a=0.0,    alpha=0.0,           d=0.0996, joint_name="wrist_3", min_limit=-2*math.pi, max_limit=2*math.pi)
        ]
        self.base_transform: Matrix4x4 = Matrix4x4.identity()
        self.joint_positions: List[float] = [0.0] * 6
        self.joint_velocities: List[float] = [0.0] * 6

    def num_joints(self) -> int:
        return len(self.links)

    def set_joint_positions(self, angles: Sequence[float]) -> None:
        if len(angles) != self.num_joints():
            raise ValueError(f"Expected {self.num_joints()} joint angles, got {len(angles)}")
        self.joint_positions = [
            max(link.min_limit, min(link.max_limit, float(q)))
            for link, q in zip(self.links, angles)
        ]

    def forward_kinematics(self, joint_angles: Optional[Sequence[float]] = None) -> List[Matrix4x4]:
        """
        Computes forward kinematics along all joint links.
        Returns list of 4x4 transformation matrices for each frame from base to end-effector.
        """
        angles = self.joint_positions if joint_angles is None else joint_angles
        if len(angles) != self.num_joints():
            raise ValueError(f"Joint count mismatch: {len(angles)} vs {self.num_joints()}")

        cumulative = [self.base_transform]
        current_t = self.base_transform

        for link, q in zip(self.links, angles):
            a_i = link.compute_transform(q)
            current_t = current_t * a_i
            cumulative.append(current_t)

        return cumulative

    def end_effector_pose(self, joint_angles: Optional[Sequence[float]] = None) -> Matrix4x4:
        """Returns 4x4 transformation of the end-effector tool frame."""
        transforms = self.forward_kinematics(joint_angles)
        return transforms[-1]

    def end_effector_position(self, joint_angles: Optional[Sequence[float]] = None) -> Vector3D:
        """Returns 3D cartesian coordinates (x, y, z) of end effector."""
        ee_mat = self.end_effector_pose(joint_angles)
        return ee_mat.get_translation()

    def compute_geometric_jacobian(self, joint_angles: Optional[Sequence[float]] = None) -> MatrixDense:
        """
        Calculates 6xN Geometric Jacobian matrix J = [J_v; J_omega]
        J_v_i = z_{i-1} x (p_e - p_{i-1}) (for revolute joint)
        J_omega_i = z_{i-1}
        """
        transforms = self.forward_kinematics(joint_angles)
        p_e = transforms[-1].get_translation()
        n = self.num_joints()

        jacobian = MatrixDense(6, n)

        for i in range(n):
            t_prev = transforms[i]
            p_prev = t_prev.get_translation()
            # z-axis of frame i-1 is the 3rd column of rotation
            rot = t_prev.get_rotation()
            z_prev = Vector3D(rot[0][2], rot[1][2], rot[2][2])

            if self.links[i].is_revolute:
                # Linear velocity component: z_{i-1} x (p_e - p_{i-1})
                arm_vec = p_e - p_prev
                j_v = z_prev.cross(arm_vec)
                jacobian[0][i] = j_v.x
                jacobian[1][i] = j_v.y
                jacobian[2][i] = j_v.z
                # Angular velocity component: z_{i-1}
                jacobian[3][i] = z_prev.x
                jacobian[4][i] = z_prev.y
                jacobian[5][i] = z_prev.z
            else:
                # Prismatic joint
                jacobian[0][i] = z_prev.x
                jacobian[1][i] = z_prev.y
                jacobian[2][i] = z_prev.z
                jacobian[3][i] = 0.0
                jacobian[4][i] = 0.0
                jacobian[5][i] = 0.0

        return jacobian

    def to_dict(self) -> Dict[str, Any]:
        transforms = self.forward_kinematics()
        return {
            "name": self.name,
            "num_joints": self.num_joints(),
            "joint_positions": list(self.joint_positions),
            "joint_limits": [[l.min_limit, l.max_limit] for l in self.links],
            "joint_names": [l.joint_name for l in self.links],
            "end_effector_position": self.end_effector_position().to_list(),
            "link_frames": [t.get_translation().to_list() for t in transforms]
        }
