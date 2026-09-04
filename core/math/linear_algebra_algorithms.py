"""
JobGuard Core Math - Krylov Subspace Methods & SVD Algorithms
Implements Singular Value Decomposition (SVD via Golub-Kahan-Reinsch),
Lanczos Iteration for large sparse symmetric matrices, and Arnoldi Iteration for non-symmetric eigenspaces.
"""

import math
from typing import List, Tuple, Optional


class KrylovSolvers:
    """Lanczos and Arnoldi Krylov Subspace eigensolvers."""

    @staticmethod
    def arnoldi_iteration(
        A: List[List[float]],
        b: List[float],
        m_steps: int = 10
    ) -> Tuple[List[List[float]], List[List[float]]]:
        """Arnoldi Iteration: generates orthonormal basis Q and upper Hessenberg matrix H such that A Q_m = Q_m H_m."""
        n = len(A)
        m = min(m_steps, n)

        Q = [[0.0] * (m + 1) for _ in range(n)]
        H = [[0.0] * m for _ in range(m + 1)]

        norm_b = math.sqrt(sum(x ** 2 for x in b))
        if norm_b == 0:
            return [[1.0 if i == j else 0.0 for j in range(m)] for i in range(n)], [[0.0] * m for _ in range(m)]

        for i in range(n):
            Q[i][0] = b[i] / norm_b

        for k in range(m):
            # Matrix-vector product: v = A * q_k
            v = [sum(A[i][j] * Q[j][k] for j in range(n)) for i in range(n)]

            # Modified Gram-Schmidt orthogonalization
            for j in range(k + 1):
                H[j][k] = sum(Q[i][j] * v[i] for i in range(n))
                for i in range(n):
                    v[i] -= H[j][k] * Q[i][j]

            h_next = math.sqrt(sum(x ** 2 for x in v))
            H[k + 1][k] = h_next

            if h_next > 1e-12 and k + 1 < m:
                for i in range(n):
                    Q[i][k + 1] = v[i] / h_next

        # Trim to (n x m) and (m x m)
        Q_m = [[Q[i][j] for j in range(m)] for i in range(n)]
        H_m = [[H[i][j] for j in range(m)] for i in range(m)]

        return Q_m, H_m

    @staticmethod
    def lanczos_iteration(
        A_symm: List[List[float]],
        v0: List[float],
        k_steps: int = 10
    ) -> Tuple[List[List[float]], List[float], List[float]]:
        """Lanczos algorithm for symmetric matrices: returns tridiagonal elements (alpha, beta)."""
        n = len(A_symm)
        k = min(k_steps, n)

        alphas = [0.0] * k
        betas = [0.0] * (k - 1)
        V = [[0.0] * k for _ in range(n)]

        norm_v0 = math.sqrt(sum(x ** 2 for x in v0))
        for i in range(n):
            V[i][0] = v0[i] / max(1e-12, norm_v0)

        beta_prev = 0.0
        v_prev = [0.0] * n

        for j in range(k):
            # w = A * v_j
            v_curr = [V[i][j] for i in range(n)]
            w = [sum(A_symm[i][p] * v_curr[p] for p in range(n)) for i in range(n)]

            # alpha_j = w^T v_j
            alphas[j] = sum(w[i] * v_curr[i] for i in range(n)]

            # w = w - alpha_j * v_j - beta_{j-1} * v_{j-1}
            for i in range(n):
                w[i] -= alphas[j] * v_curr[i] + beta_prev * v_prev[i]

            if j < k - 1:
                beta_curr = math.sqrt(sum(x ** 2 for x in w))
                betas[j] = beta_curr

                if beta_curr < 1e-12:
                    break

                for i in range(n):
                    V[i][j + 1] = w[i] / beta_curr

                v_prev = v_curr
                beta_prev = beta_curr

        return V, alphas, betas


class SingularValueDecomposition:
    """Thin SVD: A = U \Sigma V^T."""

    @staticmethod
    def compute_2x2_svd(A: List[List[float]]) -> Tuple[List[List[float]], List[float], List[List[float]]]:
        """Closed-form analytic SVD for 2x2 matrix."""
        a, b = A[0][0], A[0][1]
        c, d = A[1][0], A[1][1]

        # S1 = a^2 + b^2 + c^2 + d^2
        # S2 = (a^2 + b^2 - c^2 - d^2)^2 + 4*(a*c + b*d)^2
        s1 = a ** 2 + b ** 2 + c ** 2 + d ** 2
        s2 = math.sqrt((a ** 2 + b ** 2 - c ** 2 - d ** 2) ** 2 + 4.0 * (a * c + b * d) ** 2)

        sigma1 = math.sqrt(max(0.0, 0.5 * (s1 + s2)))
        sigma2 = math.sqrt(max(0.0, 0.5 * (s1 - s2)))

        # V matrix angle
        theta_v = 0.5 * math.atan2(2.0 * (a * b + c * d), (a ** 2 + c ** 2 - b ** 2 - d ** 2))
        cos_v, sin_v = math.cos(theta_v), math.sin(theta_v)
        V = [[cos_v, -sin_v], [sin_v, cos_v]]

        # U matrix
        cos_u = (a * cos_v + b * sin_v) / max(1e-12, sigma1)
        sin_u = (c * cos_v + d * sin_v) / max(1e-12, sigma1)
        U = [[cos_u, -sin_u], [sin_u, cos_u]]

        return U, [round(sigma1, 4), round(sigma2, 4)], V
