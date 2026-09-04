"""
Aetheris Mathematical Foundations: Vector & Coordinate Operations
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import Tuple, List, Union, Sequence, Optional


class Vector3D:
    """
    High-performance 3-dimensional Euclidean vector with extensive spatial operations,
    homogeneous coordinates conversion, projections, rotations, and vector calculus utilities.
    """
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def __repr__(self) -> str:
        return f"Vector3D(x={self.x:.6f}, y={self.y:.6f}, z={self.z:.6f})"

    def __str__(self) -> str:
        return f"[{self.x:.4f}, {self.y:.4f}, {self.z:.4f}]"

    def __getitem__(self, idx: int) -> float:
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        raise IndexError(f"Vector3D index {idx} out of range [0, 2]")

    def __setitem__(self, idx: int, value: float) -> None:
        val = float(value)
        if idx == 0:
            self.x = val
        elif idx == 1:
            self.y = val
        elif idx == 2:
            self.z = val
        else:
            raise IndexError(f"Vector3D index {idx} out of range [0, 2]")

    def __len__(self) -> int:
        return 3

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3D):
            return False
        return (
            math.isclose(self.x, other.x, abs_tol=1e-9) and
            math.isclose(self.y, other.y, abs_tol=1e-9) and
            math.isclose(self.z, other.z, abs_tol=1e-9)
        )

    def __add__(self, other: Union[Vector3D, Sequence[float]]) -> Vector3D:
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (list, tuple)) and len(other) == 3:
            return Vector3D(self.x + other[0], self.y + other[1], self.z + other[2])
        raise TypeError(f"Unsupported operand type for +: 'Vector3D' and '{type(other).__name__}'")

    def __radd__(self, other: Union[Vector3D, Sequence[float]]) -> Vector3D:
        return self.__add__(other)

    def __sub__(self, other: Union[Vector3D, Sequence[float]]) -> Vector3D:
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (list, tuple)) and len(other) == 3:
            return Vector3D(self.x - other[0], self.y - other[1], self.z - other[2])
        raise TypeError(f"Unsupported operand type for -: 'Vector3D' and '{type(other).__name__}'")

    def __rsub__(self, other: Sequence[float]) -> Vector3D:
        if isinstance(other, (list, tuple)) and len(other) == 3:
            return Vector3D(other[0] - self.x, other[1] - self.y, other[2] - self.z)
        raise TypeError(f"Unsupported operand type for -: '{type(other).__name__}' and 'Vector3D'")

    def __mul__(self, scalar: Union[int, float]) -> Vector3D:
        if isinstance(scalar, (int, float)):
            return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
        raise TypeError(f"Scalar multiplication requires float or int, got {type(scalar).__name__}")

    def __rmul__(self, scalar: Union[int, float]) -> Vector3D:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]) -> Vector3D:
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Division requires numeric scalar, got {type(scalar).__name__}")
        if math.isclose(scalar, 0.0, abs_tol=1e-12):
            raise ZeroDivisionError("Vector3D division by zero scalar")
        inv = 1.0 / float(scalar)
        return Vector3D(self.x * inv, self.y * inv, self.z * inv)

    def __neg__(self) -> Vector3D:
        return Vector3D(-self.x, -self.y, -self.z)

    def __pos__(self) -> Vector3D:
        return Vector3D(self.x, self.y, self.z)

    def __abs__(self) -> float:
        return self.norm()

    def norm_sq(self) -> float:
        """Returns squared L2 Euclidean norm."""
        return self.x * self.x + self.y * self.y + self.z * self.z

    def norm(self) -> float:
        """Returns L2 Euclidean norm (magnitude)."""
        return math.sqrt(self.norm_sq())

    def norm_l1(self) -> float:
        """Returns Manhattan L1 norm."""
        return abs(self.x) + abs(self.y) + abs(self.z)

    def norm_linf(self) -> float:
        """Returns Chebyshev L-infinity norm."""
        return max(abs(self.x), abs(self.y), abs(self.z))

    def normalize(self, epsilon: float = 1e-12) -> Vector3D:
        """Returns unit vector in the same direction, or zero vector if degenerate."""
        m = self.norm()
        if m < epsilon:
            return Vector3D(0.0, 0.0, 0.0)
        inv = 1.0 / m
        return Vector3D(self.x * inv, self.y * inv, self.z * inv)

    def is_normalized(self, tolerance: float = 1e-6) -> bool:
        """Check if vector is unit length."""
        return math.isclose(self.norm_sq(), 1.0, abs_tol=tolerance)

    def is_zero(self, tolerance: float = 1e-9) -> bool:
        """Check if all components are zero within tolerance."""
        return self.norm_sq() < (tolerance * tolerance)

    def dot(self, other: Vector3D) -> float:
        """Computes Euclidean inner dot product: self . other."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        """Computes cross product: self x other."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def angle_between(self, other: Vector3D) -> float:
        """Computes radians angle between two non-zero vectors."""
        n1 = self.norm()
        n2 = other.norm()
        if n1 < 1e-12 or n2 < 1e-12:
            return 0.0
        cos_theta = self.dot(other) / (n1 * n2)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)

    def distance_to(self, other: Vector3D) -> float:
        """Computes Euclidean distance to another 3D point."""
        return (self - other).norm()

    def distance_sq_to(self, other: Vector3D) -> float:
        """Computes squared Euclidean distance to another 3D point."""
        return (self - other).norm_sq()

    def lerp(self, target: Vector3D, alpha: float) -> Vector3D:
        """Linear interpolation between self and target with parameter alpha in [0, 1]."""
        return Vector3D(
            self.x + alpha * (target.x - self.x),
            self.y + alpha * (target.y - self.y),
            self.z + alpha * (target.z - self.z)
        )

    def slerp(self, target: Vector3D, alpha: float) -> Vector3D:
        """Spherical linear interpolation on unit sphere."""
        v0 = self.normalize()
        v1 = target.normalize()
        dot_val = max(-1.0, min(1.0, v0.dot(v1)))
        
        if dot_val > 0.9995:
            return v0.lerp(v1, alpha).normalize()
            
        theta_0 = math.acos(dot_val)
        theta = theta_0 * alpha
        sin_theta = math.sin(theta)
        sin_theta_0 = math.sin(theta_0)
        
        s0 = math.cos(theta) - dot_val * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0
        return (v0 * s0 + v1 * s1).normalize()

    def project_onto(self, normal: Vector3D) -> Vector3D:
        """Orthogonal projection of self onto target direction vector."""
        denom = normal.norm_sq()
        if denom < 1e-12:
            return Vector3D(0.0, 0.0, 0.0)
        return normal * (self.dot(normal) / denom)

    def project_onto_plane(self, plane_normal: Vector3D) -> Vector3D:
        """Orthogonal projection of self onto a plane defined by its normal."""
        return self - self.project_onto(plane_normal)

    def reflect(self, surface_normal: Vector3D) -> Vector3D:
        """Reflects vector off a surface with given unit normal."""
        n = surface_normal.normalize()
        return self - (n * (2.0 * self.dot(n)))

    def clamp(self, min_val: float, max_val: float) -> Vector3D:
        """Clamps each component within [min_val, max_val]."""
        return Vector3D(
            max(min_val, min(max_val, self.x)),
            max(min_val, min(max_val, self.y)),
            max(min_val, min(max_val, self.z))
        )

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]

    def to_homogeneous(self) -> List[float]:
        """Returns 4D homogeneous coordinate representation [x, y, z, 1.0]."""
        return [self.x, self.y, self.z, 1.0]

    @classmethod
    def from_homogeneous(cls, h_coords: Sequence[float]) -> Vector3D:
        """Converts 4D homogeneous coordinate back to 3D Cartesian."""
        if len(h_coords) < 4:
            raise ValueError("Homogeneous coordinates require at least 4 components")
        w = h_coords[3]
        if math.isclose(w, 0.0, abs_tol=1e-12):
            return cls(h_coords[0], h_coords[1], h_coords[2])
        inv_w = 1.0 / w
        return cls(h_coords[0] * inv_w, h_coords[1] * inv_w, h_coords[2] * inv_w)

    @classmethod
    def zero(cls) -> Vector3D:
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def unit_x(cls) -> Vector3D:
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def unit_y(cls) -> Vector3D:
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def unit_z(cls) -> Vector3D:
        return cls(0.0, 0.0, 1.0)


class VectorND:
    """
    Arbitrary N-dimensional continuous vector for high-dimensional feature spaces,
    gradient optimization, parameter vectors, and state representations.
    """
    __slots__ = ('data', '_dim')

    def __init__(self, values: Sequence[float]) -> None:
        self.data: List[float] = [float(v) for v in values]
        self._dim: int = len(self.data)

    @property
    def dim(self) -> int:
        return self._dim

    def __len__(self) -> int:
        return self._dim

    def __getitem__(self, idx: int) -> float:
        return self.data[idx]

    def __setitem__(self, idx: int, value: float) -> None:
        self.data[idx] = float(value)

    def __repr__(self) -> str:
        preview = ", ".join(f"{v:.4f}" for v in self.data[:6])
        if self._dim > 6:
            preview += f", ... ({self._dim} dims)"
        return f"VectorND([{preview}])"

    def __add__(self, other: VectorND) -> VectorND:
        if self._dim != other.dim:
            raise ValueError(f"Dimension mismatch: {self._dim} vs {other.dim}")
        return VectorND([a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other: VectorND) -> VectorND:
        if self._dim != other.dim:
            raise ValueError(f"Dimension mismatch: {self._dim} vs {other.dim}")
        return VectorND([a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, scalar: Union[int, float]) -> VectorND:
        s = float(scalar)
        return VectorND([v * s for v in self.data])

    def __rmul__(self, scalar: Union[int, float]) -> VectorND:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]) -> VectorND:
        s = float(scalar)
        if math.isclose(s, 0.0, abs_tol=1e-12):
            raise ZeroDivisionError("VectorND division by zero")
        inv = 1.0 / s
        return VectorND([v * inv for v in self.data])

    def __neg__(self) -> VectorND:
        return VectorND([-v for v in self.data])

    def dot(self, other: VectorND) -> float:
        """Inner dot product across all components."""
        if self._dim != other.dim:
            raise ValueError(f"Dimension mismatch: {self._dim} vs {other.dim}")
        return sum(a * b for a, b in zip(self.data, other.data))

    def norm_sq(self) -> float:
        return sum(v * v for v in self.data)

    def norm(self) -> float:
        return math.sqrt(self.norm_sq())

    def normalize(self, epsilon: float = 1e-12) -> VectorND:
        n = self.norm()
        if n < epsilon:
            return VectorND([0.0] * self._dim)
        inv = 1.0 / n
        return VectorND([v * inv for v in self.data])

    def cosine_similarity(self, other: VectorND) -> float:
        """Calculates cosine similarity in [-1.0, 1.0]."""
        n1 = self.norm()
        n2 = other.norm()
        if n1 < 1e-12 or n2 < 1e-12:
            return 0.0
        dot_p = self.dot(other)
        return max(-1.0, min(1.0, dot_p / (n1 * n2)))

    def to_list(self) -> List[float]:
        return list(self.data)

    @classmethod
    def zeros(cls, dim: int) -> VectorND:
        return cls([0.0] * dim)

    @classmethod
    def ones(cls, dim: int) -> VectorND:
        return cls([1.0] * dim)

    @classmethod
    def uniform(cls, dim: int, low: float = -1.0, high: float = 1.0, seed: Optional[int] = None) -> VectorND:
        import random
        rng = random.Random(seed)
        return cls([rng.uniform(low, high) for _ in range(dim)])
