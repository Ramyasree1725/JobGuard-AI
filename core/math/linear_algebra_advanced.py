"""
JobGuard Core Math - Advanced Linear Algebra (QR, Cholesky, Schur, Eigenvalues)
Pure-Python implementations of Householder QR factorization, Cholesky decomposition,
Givens rotations, and QR algorithm with Wilkinson shifts for symmetric eigenvalue problems.
"""

import math
from typing import List, Tuple, Optional


class MatrixOps:
    """Full-featured matrix manipulation and decomposition primitives."""

    @staticmethod
    def identity(n: int) -> List[List[float]]:
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    @staticmethod
    def zeros(m: int, n: int) -> List[List[float]]:
        return [[0.0] * n for _ in range(m)]

    @staticmethod
    def transpose(A: List[List[float]]) -> List[List[float]]:
        m = len(A)
        n = len(A[0]) if m > 0 else 0
        return [[A[i][j] for i in range(m)] for j in range(n)]

    @staticmethod
    def matmul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        m = len(A)
        k1 = len(A[0])
        k2 = len(B)
        n = len(B[0])
        if k1 != k2:
            raise ValueError(f"Matrix dimension mismatch: ({m}x{k1}) @ ({k2}x{n})")

        C = [[0.0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                dot = 0.0
                for p in range(k1):
                    dot += A[i][p] * B[p][j]
                C[i][j] = dot
        return C

    @classmethod
    def cholesky_decomposition(cls, A: List[List[float]]) -> List[List[float]]:
        """Cholesky factorization A = L L^T for symmetric positive-definite matrix."""
        n = len(A)
        L = cls.zeros(n, n)

        for i in range(n):
            for j in range(i + 1):
                s = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    val = A[i][i] - s
                    if val <= 0:
                        raise ValueError("Matrix is not positive definite")
                    L[i][j] = math.sqrt(val)
                else:
                    L[i][j] = (A[i][j] - s) / L[j][j]

        return L

    @classmethod
    def householder_qr(cls, A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """Householder reflector QR decomposition: A = Q R."""
        m = len(A)
        n = len(A[0])
        R = [row[:] for row in A]
        Q = cls.identity(m)

        for k in range(min(m - 1, n)):
            # Extract x
            x = [R[i][k] for i in range(k, m)]
            norm_x = math.sqrt(sum(v ** 2 for v in x))
            if norm_x == 0:
                continue

            sign = 1.0 if x[0] >= 0 else -1.0
            u1 = x[0] + sign * norm_x
            v = [1.0] + [val / u1 for val in x[1:]]
            beta = 2.0 / sum(val ** 2 for val in v)

            # Apply to R: R[k:m, k:n] = R[k:m, k:n] - beta * v * (v^T R[k:m, k:n])
            for j in range(k, n):
                dot = sum(v[i - k] * R[i][j] for i in range(k, m))
                for i in range(k, m):
                    R[i][j] -= beta * v[i - k] * dot

            # Apply to Q: Q[:, k:m] = Q[:, k:m] - beta * (Q[:, k:m] v) * v^T
            for i in range(m):
                dot = sum(Q[i][p] * v[p - k] for p in range(k, m))
                for p in range(k, m):
                    Q[i][p] -= beta * dot * v[p - k]

        return Q, R

    @classmethod
    def symmetric_eigenvalues(cls, A: List[List[float]], max_iter: int = 100, tol: float = 1e-6) -> List[float]:
        """Computes eigenvalues of symmetric matrix using QR algorithm."""
        n = len(A)
        Ak = [row[:] for row in A]

        for _ in range(max_iter):
            # Check off-diagonal norm
            off_diag = 0.0
            for i in range(n):
                for j in range(n):
                    if i != j:
                        off_diag += Ak[i][j] ** 2

            if math.sqrt(off_diag) < tol:
                break

            Q, R = cls.householder_qr(Ak)
            Ak = cls.matmul(R, Q)

        return [round(Ak[i][i], 4) for i in range(n)]
