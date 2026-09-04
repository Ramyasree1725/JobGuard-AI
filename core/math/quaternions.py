"""
Aetheris Mathematical Foundations: Unit Quaternions & Rotations in SO(3)
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import Tuple, List, Union, Optional
from core.math.vectors import Vector3D
from core.math.matrices import Matrix3x3


class Quaternion:
    """
    Unit Quaternion representation of SO(3) rotations q = [w, x, y, z] = w + xi + yj + zk.
    Eliminates gimbal lock, supports smooth spherical interpolation (SLERP),
    and fast rotation chaining for robotics and 3D simulation.
    """
    __slots__ = ('w', 'x', 'y', 'z')

    def __init__(self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.w: float = float(w)
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def __repr__(self) -> str:
        return f"Quaternion(w={self.w:.6f}, x={self.x:.6f}, y={self.y:.6f}, z={self.z:.6f})"

    def __getitem__(self, idx: int) -> float:
        if idx == 0:
            return self.w
        elif idx == 1:
            return self.x
        elif idx == 2:
            return self.y
        elif idx == 3:
            return self.z
        raise IndexError(f"Quaternion index {idx} out of range [0, 3]")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quaternion):
            return False
        # Quaternions q and -q represent identical rotations
        same = (
            math.isclose(self.w, other.w, abs_tol=1e-8) and
            math.isclose(self.x, other.x, abs_tol=1e-8) and
            math.isclose(self.y, other.y, abs_tol=1e-8) and
            math.isclose(self.z, other.z, abs_tol=1e-8)
        )
        neg_same = (
            math.isclose(self.w, -other.w, abs_tol=1e-8) and
            math.isclose(self.x, -other.x, abs_tol=1e-8) and
            math.isclose(self.y, -other.y, abs_tol=1e-8) and
            math.isclose(self.z, -other.z, abs_tol=1e-8)
        )
        return same or neg_same

    def norm_sq(self) -> float:
        return self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z

    def norm(self) -> float:
        return math.sqrt(self.norm_sq())

    def normalize(self, epsilon: float = 1e-12) -> Quaternion:
        n = self.norm()
        if n < epsilon:
            return Quaternion(1.0, 0.0, 0.0, 0.0)
        inv = 1.0 / n
        return Quaternion(self.w * inv, self.x * inv, self.y * inv, self.z * inv)

    def conjugate(self) -> Quaternion:
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> Quaternion:
        n2 = self.norm_sq()
        if n2 < 1e-12:
            return Quaternion.identity()
        inv_n2 = 1.0 / n2
        return Quaternion(self.w * inv_n2, -self.x * inv_n2, -self.y * inv_n2, -self.z * inv_n2)

    def __mul__(self, other: Union[Quaternion, Vector3D, float]) -> Union[Quaternion, Vector3D]:
        """
        Hamilton Product: q1 * q2, or vector rotation: q * v * q^-1.
        """
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        elif isinstance(other, Vector3D):
            # Optimized vector rotation: v' = v + 2*r x (r x v + w*v) where r = (x, y, z)
            r = Vector3D(self.x, self.y, self.z)
            rxv = r.cross(other)
            return other + (rxv * self.w + r.cross(rxv)) * 2.0
        elif isinstance(other, (int, float)):
            s = float(other)
            return Quaternion(self.w * s, self.x * s, self.y * s, self.z * s)
        raise TypeError(f"Unsupported operand for Quaternion multiplication: {type(other).__name__}")

    def rotate_vector(self, v: Vector3D) -> Vector3D:
        """Rotates 3D vector by this quaternion."""
        return self * v

    def to_rotation_matrix(self) -> Matrix3x3:
        """Converts unit quaternion to 3x3 rotation matrix."""
        q = self.normalize()
        w, x, y, z = q.w, q.x, q.y, q.z
        
        xx, yy, zz = x * x, y * y, z * z
        xy, xz, yz = x * y, x * z, y * z
        wx, wy, wz = w * x, w * y, w * z

        return Matrix3x3([
            [1.0 - 2.0 * (yy + zz),       2.0 * (xy - wz),       2.0 * (xz + wy)],
            [      2.0 * (xy + wz), 1.0 - 2.0 * (xx + zz),       2.0 * (yz - wx)],
            [      2.0 * (xz - wy),       2.0 * (yz + wx), 1.0 - 2.0 * (xx + yy)]
        ])

    def to_euler_zyx(self) -> Tuple[float, float, float]:
        """
        Converts to Euler angles (Yaw, Pitch, Roll) in radians.
        """
        q = self.normalize()
        w, x, y, z = q.w, q.x, q.y, q.z

        # Roll (X-axis rotation)
        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (Y-axis rotation)
        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1.0:
            pitch = math.copysign(math.pi / 2.0, sinp)
        else:
            pitch = math.asin(sinp)

        # Yaw (Z-axis rotation)
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return (yaw, pitch, roll)

    def slerp(self, target: Quaternion, t: float) -> Quaternion:
        """
        Spherical Linear Interpolation between two quaternions with factor t in [0, 1].
        """
        t = max(0.0, min(1.0, float(t)))
        q1 = self.normalize()
        q2 = target.normalize()

        dot = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z

        # If negative dot, invert rotation to take the shortest path on S3
        if dot < 0.0:
            q2 = Quaternion(-q2.w, -q2.x, -q2.y, -q2.z)
            dot = -dot

        if dot > 0.9995:
            # Linear interpolation if almost identical
            res = Quaternion(
                q1.w + t * (q2.w - q1.w),
                q1.x + t * (q2.x - q1.x),
                q1.y + t * (q2.y - q1.y),
                q1.z + t * (q2.z - q1.z)
            )
            return res.normalize()

        theta_0 = math.acos(dot)
        theta = theta_0 * t
        sin_theta = math.sin(theta)
        sin_theta_0 = math.sin(theta_0)

        s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0

        return Quaternion(
            s0 * q1.w + s1 * q2.w,
            s0 * q1.x + s1 * q2.x,
            s0 * q1.y + s1 * q2.y,
            s0 * q1.z + s1 * q2.z
        )

    @classmethod
    def identity(cls) -> Quaternion:
        return cls(1.0, 0.0, 0.0, 0.0)

    @classmethod
    def from_axis_angle(cls, axis: Vector3D, angle_rad: float) -> Quaternion:
        u = axis.normalize()
        half = angle_rad * 0.5
        s = math.sin(half)
        return cls(math.cos(half), u.x * s, u.y * s, u.z * s).normalize()

    @classmethod
    def from_euler_zyx(cls, yaw: float, pitch: float, roll: float) -> Quaternion:
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        return cls(w, x, y, z).normalize()
