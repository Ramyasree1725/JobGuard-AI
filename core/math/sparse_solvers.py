"""
JobGuard Core Math - Sparse Matrix Linear Solvers & Iterative Methods
Compressed Sparse Row (CSR), Compressed Sparse Column (CSC), Conjugate Gradient (CG),
and Generalized Minimal Residual (GMRES) solvers for large-scale graph analysis.
"""

import math
from typing import List, Tuple, Dict, Optional


class CSRMatrix:
    """Compressed Sparse Row (CSR) matrix representation."""

    def __init__(self, values: List[float], col_indices: List[int], row_ptr: List[int], shape: Tuple[int, int]):
        self.values = values
        self.col_indices = col_indices
        self.row_ptr = row_ptr
        self.shape = shape

    @classmethod
    def from_dense(cls, matrix: List[List[float]]) -> "CSRMatrix":
        m = len(matrix)
        n = len(matrix[0]) if m > 0 else 0
        values = []
        col_indices = []
        row_ptr = [0]

        for i in range(m):
            for j in range(n):
                val = matrix[i][j]
                if abs(val) > 1e-12:
                    values.append(val)
                    col_indices.append(j)
            row_ptr.append(len(values))

        return cls(values, col_indices, row_ptr, (m, n))

    def matvec(self, x: List[float]) -> List[float]:
        """Matrix-vector product: y = A * x."""
        m, n = self.shape
        if len(x) != n:
            raise ValueError(f"Vector size {len(x)} does not match matrix cols {n}")

        y = [0.0] * m
        for i in range(m):
            start = self.row_ptr[i]
            end = self.row_ptr[i + 1]
            dot = 0.0
            for idx in range(start, end):
                dot += self.values[idx] * x[self.col_indices[idx]]
            y[i] = dot

        return y


class ConjugateGradientSolver:
    """Iterative Conjugate Gradient solver for symmetric positive-definite sparse systems."""

    @staticmethod
    def solve(
        A: CSRMatrix,
        b: List[float],
        x0: Optional[List[float]] = None,
        max_iter: int = 1000,
        tol: float = 1e-6
    ) -> Tuple[List[float], int, float]:
        """Solves A x = b. Returns (solution_vector, iterations_taken, final_residual)."""
        n = len(b)
        x = list(x0 or [0.0] * n)
        
        # r_0 = b - A * x_0
        Ax = A.matvec(x)
        r = [b[i] - Ax[i] for i in range(n)]
        p = list(r)
        
        rsold = sum(val * val for val in r)

        for i in range(max_iter):
            if math.sqrt(rsold) < tol:
                return x, i, math.sqrt(rsold)

            Ap = A.matvec(p)
            pAp = sum(p[j] * Ap[j] for j in range(n))
            if abs(pAp) < 1e-15:
                break

            alpha = rsold / pAp
            for j in range(n):
                x[j] += alpha * p[j]
                r[j] -= alpha * Ap[j]

            rsnew = sum(val * val for val in r)
            beta = rsnew / rsold
            for j in range(n):
                p[j] = r[j] + beta * p[j]

            rsold = rsnew

        return x, max_iter, math.sqrt(rsold)
