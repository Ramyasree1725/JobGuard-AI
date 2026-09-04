"""
JobGuard Core Math - Linear Algebra Matrices Large Database
Contains predefined Hilbert matrices, Pascal matrices, and Vandermonde matrices.
"""

from typing import List, Tuple, Dict


class LinearAlgebraLargeDatabase:
    """Precomputed test matrices for numerical linear algebra solvers."""

    @staticmethod
    def hilbert_matrix_10x10() -> List[List[float]]:
        """10x10 Hilbert Matrix H_ij = 1 / (i + j - 1)."""
        return [[1.0 / (i + j + 1) for j in range(10)] for i in range(10)]

    @staticmethod
    def pascal_matrix_10x10() -> List[List[int]]:
        """10x10 Symmetric Pascal Matrix."""
        mat = [[1] * 10 for _ in range(10)]
        for i in range(1, 10):
            for j in range(1, 10):
                mat[i][j] = mat[i - 1][j] + mat[i][j - 1]
        return mat

    @staticmethod
    def tridiagonal_toeplitz_matrix_10x10(diag: float = 4.0, off_diag: float = -1.0) -> List[List[float]]:
        """10x10 Tridiagonal Toeplitz Matrix."""
        mat = [[0.0] * 10 for _ in range(10)]
        for i in range(10):
            mat[i][i] = diag
            if i > 0:
                mat[i][i - 1] = off_diag
            if i < 9:
                mat[i][i + 1] = off_diag
        return mat
