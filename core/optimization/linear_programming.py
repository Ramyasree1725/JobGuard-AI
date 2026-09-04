"""
JobGuard Core Optimization - Simplex Linear Programming (LP) Solver
Solves standard primal/dual linear programs (min c^T x s.t. Ax <= b, x >= 0)
for optimal budget allocation in threat mitigation resources.
"""

from typing import List, Tuple, Optional


class SimplexSolver:
    """Tableau Simplex algorithm for linear programming problems."""

    @staticmethod
    def solve_max(c: List[float], A: List[List[float]], b: List[float]) -> Tuple[Optional[List[float]], Optional[float]]:
        """Maximize c^T x subject to A x <= b, x >= 0."""
        m = len(A)       # Number of constraints
        n = len(c)       # Number of variables

        # Build initial tableau:
        # [ A | I | b ]
        # [ -c | 0 | 0 ]
        tableau = []
        for i in range(m):
            row = list(A[i]) + [1.0 if i == j else 0.0 for j in range(m)] + [b[i]]
            tableau.append(row)

        obj_row = [-val for val in c] + [0.0] * m + [0.0]
        tableau.append(obj_row)

        total_cols = n + m + 1

        while True:
            # Find pivot column (most negative in bottom row)
            pivot_col = -1
            min_val = -1e-9
            for j in range(total_cols - 1):
                if tableau[-1][j] < min_val:
                    min_val = tableau[-1][j]
                    pivot_col = j

            if pivot_col == -1:
                # Optimal reached
                break

            # Find pivot row by minimum ratio test
            pivot_row = -1
            min_ratio = float("inf")
            for i in range(m):
                if tableau[i][pivot_col] > 1e-9:
                    ratio = tableau[i][-1] / tableau[i][pivot_col]
                    if ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i

            if pivot_row == -1:
                # Unbounded
                return None, None

            # Pivot operation
            pivot_val = tableau[pivot_row][pivot_col]
            for j in range(total_cols):
                tableau[pivot_row][j] /= pivot_val

            for i in range(m + 1):
                if i != pivot_row:
                    factor = tableau[i][pivot_col]
                    for j in range(total_cols):
                        tableau[i][j] -= factor * tableau[pivot_row][j]

        # Extract solution
        x = [0.0] * n
        for j in range(n):
            # Check if basic column
            col_vals = [tableau[i][j] for i in range(m)]
            if col_vals.count(1.0) == 1 and col_vals.count(0.0) == m - 1:
                row_idx = col_vals.index(1.0)
                x[j] = round(tableau[row_idx][-1], 4)

        opt_val = round(tableau[-1][-1], 4)
        return x, opt_val
