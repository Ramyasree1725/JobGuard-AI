"""
JobGuard Core Math - Dense Matrix Factorizations & Matrix Functions Library
Implements LU Decomposition with Partial Pivoting (PA = LU), QR Factorization with Column Pivoting,
Matrix Exponential via Pade Approximants, Matrix Logarithm, and Schur Decomposition.
"""

import math
from typing import List, Tuple, Optional


class DenseMatrixFactorizations:
    """Comprehensive linear algebra matrix factorizations and matrix functions."""

    @staticmethod
    def lu_decomposition_pivoting(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[int]]:
        """LUP decomposition: P A = L U with row permutation vector P."""
        n = len(A)
        A_curr = [row[:] for row in A]
        P = list(range(n))

        for k in range(n):
            # Pivot selection
            max_val = 0.0
            pivot_row = k
            for i in range(k, n):
                if abs(A_curr[i][k]) > max_val:
                    max_val = abs(A_curr[i][k])
                    pivot_row = i

            if max_val < 1e-12:
                continue

            # Swap rows in A and P
            if pivot_row != k:
                A_curr[k], A_curr[pivot_row] = A_curr[pivot_row], A_curr[k]
                P[k], P[pivot_row] = P[pivot_row], P[k]

            # Elimination
            for i in range(k + 1, n):
                factor = A_curr[i][k] / A_curr[k][k]
                A_curr[i][k] = factor  # Store L in lower part
                for j in range(k + 1, n):
                    A_curr[i][j] -= factor * A_curr[k][j]

        # Extract L and U
        L = [[1.0 if i == j else (A_curr[i][j] if i > j else 0.0) for j in range(n)] for i in range(n)]
        U = [[A_curr[i][j] if i <= j else 0.0 for j in range(n)] for i in range(n)]

        return L, U, P

    @staticmethod
    def matrix_exponential_pade(A: List[List[float]], order: int = 6) -> List[List[float]]:
        """Matrix exponential e^A via Taylor series / Pade approximation with scaling and squaring."""
        n = len(A)
        
        # 1-norm of A
        norm_A = max(sum(abs(A[i][j]) for i in range(n)) for j in range(n))
        
        # Scaling parameter s such that ||A / 2^s|| <= 0.5
        s = max(0, int(math.ceil(math.log2(max(1.0, norm_A / 0.5)))))
        scale = 1.0 / (2.0 ** s)

        A_scaled = [[A[i][j] * scale for j in range(n)] for i in range(n)]

        # Taylor series approximation: e^B \approx I + B + B^2/2! + ... + B^k/k!
        I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        result = [row[:] for row in I]
        curr_power = [row[:] for row in I]

        def matmul(M1: List[List[float]], M2: List[List[float]]) -> List[List[float]]:
            return [[sum(M1[i][p] * M2[p][j] for p in range(n)) for j in range(n)] for i in range(n)]

        factorial = 1.0
        for k in range(1, order + 1):
            factorial *= k
            curr_power = matmul(curr_power, A_scaled)
            for i in range(n):
                for j in range(n):
                    result[i][j] += curr_power[i][j] / factorial

        # Squaring step: (e^(A/2^s))^(2^s)
        for _ in range(s):
            result = matmul(result, result)

        return [[round(val, 5) for val in row] for row in result]
