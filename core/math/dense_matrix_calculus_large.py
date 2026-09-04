"""
JobGuard Core Math - Dense Matrix Matrix-Vector Differential Calculus Large
Implements Jacobian matrix computation, Hessian matrix quadratic approximations,
and tensor contractions for high-dimensional loss surface analysis in scam detection models.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class DenseMatrixCalculusLarge:
    """Matrix calculus and multidimensional optimization primitives."""

    @staticmethod
    def compute_numerical_jacobian(
        vector_fn: Any,
        x_point: List[float],
        h_step: float = 1e-5
    ) -> List[List[float]]:
        """Computes m x n Jacobian matrix J_ij = df_i/dx_j via central finite differences."""
        n = len(x_point)
        f_0 = vector_fn(x_point)
        m = len(f_0)
        jacobian = [[0.0] * n for _ in range(m)]

        for j in range(n):
            x_plus = list(x_point)
            x_minus = list(x_point)
            x_plus[j] += h_step
            x_minus[j] -= h_step

            f_plus = vector_fn(x_plus)
            f_minus = vector_fn(x_minus)

            for i in range(m):
                jacobian[i][j] = (f_plus[i] - f_minus[i]) / (2.0 * h_step)

        return jacobian

    @staticmethod
    def quadratic_form_value(A_matrix: List[List[float]], x_vector: List[float]) -> float:
        """Computes quadratic form: x^T * A * x."""
        n = len(x_vector)
        # Ax = A * x
        ax = [sum(A_matrix[i][j] * x_vector[j] for j in range(n)) for i in range(n)]
        # x^T * Ax
        return sum(x_vector[i] * ax[i] for i in range(n))
