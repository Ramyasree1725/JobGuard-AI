"""
Aetheris Mathematical Foundations: Matrix Transformations & Linear Algebra
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Sequence, Optional, Union
from core.math.vectors import Vector3D


class Matrix3x3:
    """
    3x3 Special Orthogonal and general transformation matrix for rotational kinematics,
    inertia tensors, coordinate frame transitions, and strain tensors.
    """
    __slots__ = ('m',)

    def __init__(self, elements: Optional[Sequence[Sequence[float]]] = None) -> None:
        if elements is None:
            self.m = [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]
            ]
        else:
            if len(elements) != 3 or any(len(row) != 3 for row in elements):
                raise ValueError("Matrix3x3 requires a 3x3 nested structure")
            self.m = [[float(val) for val in row] for row in elements]

    def __repr__(self) -> str:
        rows = [f"  [{', '.join(f'{v:10.5f}' for v in row)}]" for row in self.m]
        return "Matrix3x3(\n" + ",\n".join(rows) + "\n)"

    def __getitem__(self, idx: int) -> List[float]:
        return self.m[idx]

    def __setitem__(self, idx: int, value: Sequence[float]) -> None:
        if len(value) != 3:
            raise ValueError("Row must contain exactly 3 floats")
        self.m[idx] = [float(v) for v in value]

    def get(self, r: int, c: int) -> float:
        return self.m[r][c]

    def set(self, r: int, c: int, val: float) -> None:
        self.m[r][c] = float(val)

    def __add__(self, other: Matrix3x3) -> Matrix3x3:
        return Matrix3x3([[self.m[r][c] + other.m[r][c] for c in range(3)] for r in range(3)])

    def __sub__(self, other: Matrix3x3) -> Matrix3x3:
        return Matrix3x3([[self.m[r][c] - other.m[r][c] for c in range(3)] for r in range(3)])

    def __mul__(self, other: Union[Matrix3x3, Vector3D, float, int]) -> Union[Matrix3x3, Vector3D]:
        if isinstance(other, (int, float)):
            s = float(other)
            return Matrix3x3([[self.m[r][c] * s for c in range(3)] for r in range(3)])
        elif isinstance(other, Matrix3x3):
            res = [[0.0] * 3 for _ in range(3)]
            for r in range(3):
                for c in range(3):
                    res[r][c] = (
                        self.m[r][0] * other.m[0][c] +
                        self.m[r][1] * other.m[1][c] +
                        self.m[r][2] * other.m[2][c]
                    )
            return Matrix3x3(res)
        elif isinstance(other, Vector3D):
            return Vector3D(
                self.m[0][0] * other.x + self.m[0][1] * other.y + self.m[0][2] * other.z,
                self.m[1][0] * other.x + self.m[1][1] * other.y + self.m[1][2] * other.z,
                self.m[2][0] * other.x + self.m[2][1] * other.y + self.m[2][2] * other.z
            )
        raise TypeError(f"Cannot multiply Matrix3x3 with {type(other).__name__}")

    def transpose(self) -> Matrix3x3:
        return Matrix3x3([[self.m[c][r] for c in range(3)] for r in range(3)])

    def trace(self) -> float:
        return self.m[0][0] + self.m[1][1] + self.m[2][2]

    def determinant(self) -> float:
        return (
            self.m[0][0] * (self.m[1][1] * self.m[2][2] - self.m[1][2] * self.m[2][1]) -
            self.m[0][1] * (self.m[1][0] * self.m[2][2] - self.m[1][2] * self.m[2][0]) +
            self.m[0][2] * (self.m[1][0] * self.m[2][1] - self.m[1][1] * self.m[2][0])
        )

    def inverse(self, epsilon: float = 1e-12) -> Matrix3x3:
        det = self.determinant()
        if abs(det) < epsilon:
            raise ValueError(f"Matrix3x3 is singular (det={det:.3e}), cannot invert")
        inv_det = 1.0 / det
        
        inv = [
            [
                (self.m[1][1] * self.m[2][2] - self.m[1][2] * self.m[2][1]) * inv_det,
                (self.m[0][2] * self.m[2][1] - self.m[0][1] * self.m[2][2]) * inv_det,
                (self.m[0][1] * self.m[1][2] - self.m[0][2] * self.m[1][1]) * inv_det
            ],
            [
                (self.m[1][2] * self.m[2][0] - self.m[1][0] * self.m[2][2]) * inv_det,
                (self.m[0][0] * self.m[2][2] - self.m[0][2] * self.m[2][0]) * inv_det,
                (self.m[0][2] * self.m[1][0] - self.m[0][0] * self.m[1][2]) * inv_det
            ],
            [
                (self.m[1][0] * self.m[2][1] - self.m[1][1] * self.m[2][0]) * inv_det,
                (self.m[0][1] * self.m[2][0] - self.m[0][0] * self.m[2][1]) * inv_det,
                (self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]) * inv_det
            ]
        ]
        return Matrix3x3(inv)

    @classmethod
    def identity(cls) -> Matrix3x3:
        return cls()

    @classmethod
    def zeros(cls) -> Matrix3x3:
        return cls([[0.0] * 3 for _ in range(3)])

    @classmethod
    def rotation_x(cls, radians: float) -> Matrix3x3:
        c = math.cos(radians)
        s = math.sin(radians)
        return cls([
            [1.0, 0.0, 0.0],
            [0.0,   c,  -s],
            [0.0,   s,   c]
        ])

    @classmethod
    def rotation_y(cls, radians: float) -> Matrix3x3:
        c = math.cos(radians)
        s = math.sin(radians)
        return cls([
            [  c, 0.0,   s],
            [0.0, 1.0, 0.0],
            [ -s, 0.0,   c]
        ])

    @classmethod
    def rotation_z(cls, radians: float) -> Matrix3x3:
        c = math.cos(radians)
        s = math.sin(radians)
        return cls([
            [  c,  -s, 0.0],
            [  s,   c, 0.0],
            [0.0, 0.0, 1.0]
        ])

    @classmethod
    def from_euler_zyx(cls, yaw: float, pitch: float, roll: float) -> Matrix3x3:
        """Tait-Bryan ZYX Euler angles composition (Yaw -> Pitch -> Roll)."""
        rz = cls.rotation_z(yaw)
        ry = cls.rotation_y(pitch)
        rx = cls.rotation_x(roll)
        return (rz * ry) * rx

    @classmethod
    def from_axis_angle(cls, axis: Vector3D, radians: float) -> Matrix3x3:
        """Rodrigues rotation formula."""
        u = axis.normalize()
        c = math.cos(radians)
        s = math.sin(radians)
        c1 = 1.0 - c

        return cls([
            [c + u.x * u.x * c1,       u.x * u.y * c1 - u.z * s, u.x * u.z * c1 + u.y * s],
            [u.y * u.x * c1 + u.z * s, c + u.y * u.y * c1,       u.y * u.z * c1 - u.x * s],
            [u.z * u.x * c1 - u.y * s, u.z * u.y * c1 + u.x * s, c + u.z * u.z * c1]
        ])


class Matrix4x4:
    """
    4x4 Homogeneous Transformation Matrix for robotics Forward Kinematics,
    rigid-body SE(3) poses, Denavit-Hartenberg frames, and 3D camera projections.
    """
    __slots__ = ('m',)

    def __init__(self, elements: Optional[Sequence[Sequence[float]]] = None) -> None:
        if elements is None:
            self.m = [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ]
        else:
            if len(elements) != 4 or any(len(row) != 4 for row in elements):
                raise ValueError("Matrix4x4 requires a 4x4 nested structure")
            self.m = [[float(val) for val in row] for row in elements]

    def __repr__(self) -> str:
        rows = [f"  [{', '.join(f'{v:10.5f}' for v in row)}]" for row in self.m]
        return "Matrix4x4(\n" + ",\n".join(rows) + "\n)"

    def __getitem__(self, idx: int) -> List[float]:
        return self.m[idx]

    def get_rotation(self) -> Matrix3x3:
        return Matrix3x3([
            [self.m[0][0], self.m[0][1], self.m[0][2]],
            [self.m[1][0], self.m[1][1], self.m[1][2]],
            [self.m[2][0], self.m[2][1], self.m[2][2]]
        ])

    def get_translation(self) -> Vector3D:
        return Vector3D(self.m[0][3], self.m[1][3], self.m[2][3])

    def __mul__(self, other: Union[Matrix4x4, Vector3D, float]) -> Union[Matrix4x4, Vector3D]:
        if isinstance(other, Matrix4x4):
            res = [[0.0] * 4 for _ in range(4)]
            for r in range(4):
                for c in range(4):
                    res[r][c] = (
                        self.m[r][0] * other.m[0][c] +
                        self.m[r][1] * other.m[1][c] +
                        self.m[r][2] * other.m[2][c] +
                        self.m[r][3] * other.m[3][c]
                    )
            return Matrix4x4(res)
        elif isinstance(other, Vector3D):
            # Homogeneous transform of 3D point (w=1.0)
            x = self.m[0][0] * other.x + self.m[0][1] * other.y + self.m[0][2] * other.z + self.m[0][3]
            y = self.m[1][0] * other.x + self.m[1][1] * other.y + self.m[1][2] * other.z + self.m[1][3]
            z = self.m[2][0] * other.x + self.m[2][1] * other.y + self.m[2][2] * other.z + self.m[2][3]
            w = self.m[3][0] * other.x + self.m[3][1] * other.y + self.m[3][2] * other.z + self.m[3][3]
            if abs(w - 1.0) > 1e-12 and abs(w) > 1e-12:
                inv_w = 1.0 / w
                return Vector3D(x * inv_w, y * inv_w, z * inv_w)
            return Vector3D(x, y, z)
        elif isinstance(other, (int, float)):
            s = float(other)
            return Matrix4x4([[self.m[r][c] * s for c in range(4)] for r in range(4)])
        raise TypeError(f"Cannot multiply Matrix4x4 with {type(other).__name__}")

    def transform_vector(self, v: Vector3D) -> Vector3D:
        """Transforms direction vector (w=0, translation ignored)."""
        return Vector3D(
            self.m[0][0] * v.x + self.m[0][1] * v.y + self.m[0][2] * v.z,
            self.m[1][0] * v.x + self.m[1][1] * v.y + self.m[1][2] * v.z,
            self.m[2][0] * v.x + self.m[2][1] * v.y + self.m[2][2] * v.z
        )

    def inverse_se3(self) -> Matrix4x4:
        """
        Optimized fast inversion for Rigid SE(3) Transformations:
        T = [R, p; 0, 1] => T^-1 = [R^T, -R^T * p; 0, 1]
        """
        r = self.get_rotation().transpose()
        p = self.get_translation()
        inv_p = -(r * p)
        return Matrix4x4([
            [r.m[0][0], r.m[0][1], r.m[0][2], inv_p.x],
            [r.m[1][0], r.m[1][1], r.m[1][2], inv_p.y],
            [r.m[2][0], r.m[2][1], r.m[2][2], inv_p.z],
            [0.0,       0.0,       0.0,       1.0]
        ])

    @classmethod
    def identity(cls) -> Matrix4x4:
        return cls()

    @classmethod
    def from_rotation_translation(cls, r: Matrix3x3, t: Vector3D) -> Matrix4x4:
        return cls([
            [r.m[0][0], r.m[0][1], r.m[0][2], t.x],
            [r.m[1][0], r.m[1][1], r.m[1][2], t.y],
            [r.m[2][0], r.m[2][1], r.m[2][2], t.z],
            [0.0,       0.0,       0.0,       1.0]
        ])

    @classmethod
    def from_dh_parameters(cls, a: float, alpha: float, d: float, theta: float) -> Matrix4x4:
        """
        Standard Denavit-Hartenberg (DH) Transformation Matrix for Robotic Manipulators:
        A_i = Rot_z(theta) * Trans_z(d) * Trans_x(a) * Rot_x(alpha)
        """
        ct = math.cos(theta)
        st = math.sin(theta)
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        return cls([
            [ct, -st * ca,  st * sa, a * ct],
            [st,  ct * ca, -ct * sa, a * st],
            [0.0,      sa,       ca,      d],
            [0.0,     0.0,      0.0,    1.0]
        ])


class MatrixDense:
    """
    Arbitrary M x N dense matrix for numerical solvers, Jacobians, Covariances,
    Gram matrices, SVD, and neural layer weights.
    """
    __slots__ = ('rows', 'cols', 'data')

    def __init__(self, rows: int, cols: int, initial: float = 0.0) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.data: List[List[float]] = [[float(initial)] * cols for _ in range(rows)]

    @classmethod
    def from_nested(cls, data: Sequence[Sequence[float]]) -> MatrixDense:
        r = len(data)
        if r == 0:
            return cls(0, 0)
        c = len(data[0])
        m = cls(r, c)
        m.data = [[float(val) for val in row] for row in data]
        return m

    def __getitem__(self, idx: int) -> List[float]:
        return self.data[idx]

    def __repr__(self) -> str:
        return f"MatrixDense({self.rows}x{self.cols})"

    def transpose(self) -> MatrixDense:
        t = MatrixDense(self.cols, self.rows)
        for r in range(self.rows):
            for c in range(self.cols):
                t.data[c][r] = self.data[r][c]
        return t

    def matmul(self, other: MatrixDense) -> MatrixDense:
        if self.cols != other.rows:
            raise ValueError(f"Incompatible dimensions for matmul: ({self.rows}x{self.cols}) and ({other.rows}x{other.cols})")
        res = MatrixDense(self.rows, other.cols)
        for i in range(self.rows):
            for k in range(self.cols):
                aik = self.data[i][k]
                for j in range(other.cols):
                    res.data[i][j] += aik * other.data[k][j]
        return res

    def solve_linear_system_gaussian(self, b: List[float]) -> List[float]:
        """
        Solves A * x = b via Gaussian elimination with partial pivoting.
        """
        if self.rows != self.cols:
            raise ValueError("Linear system must be square")
        n = self.rows
        if len(b) != n:
            raise ValueError(f"Target vector length {len(b)} != matrix size {n}")

        # Augmented matrix
        aug = [row[:] + [b[i]] for i, row in enumerate(self.data)]

        # Forward elimination with partial pivoting
        for i in range(n):
            max_row = i
            max_val = abs(aug[i][i])
            for k in range(i + 1, n):
                if abs(aug[k][i]) > max_val:
                    max_val = abs(aug[k][i])
                    max_row = k

            if max_val < 1e-12:
                raise ValueError(f"Matrix is singular or near-singular at pivot {i}")

            aug[i], aug[max_row] = aug[max_row], aug[i]

            for k in range(i + 1, n):
                factor = aug[k][i] / aug[i][i]
                for j in range(i, n + 1):
                    aug[k][j] -= factor * aug[i][j]

        # Back substitution
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            s = aug[i][n]
            for j in range(i + 1, n):
                s -= aug[i][j] * x[j]
            x[i] = s / aug[i][i]

        return x
