"""
Aetheris Optimization & Neural-Symbolic: Gaussian Process Surrogate & Acquisition Functions
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Optional, Sequence, Dict, Any
from core.math.vectors import VectorND
from core.math.matrices import MatrixDense
from core.optimization.gp_kernels import BaseKernel, RBFKernel, Matern52Kernel


class GaussianProcessRegressor:
    """
    Gaussian Process Regression (Kriging surrogate model) for expensive black-box function optimization.
    Computes analytical posterior mean mu(x*) and epistemic uncertainty sigma^2(x*).
    """
    def __init__(self, kernel: Optional[BaseKernel] = None, noise_variance: float = 1e-4) -> None:
        self.kernel = kernel if kernel is not None else Matern52Kernel()
        self.noise_var = max(1e-8, float(noise_variance))
        self.X_train: List[VectorND] = []
        self.y_train: List[float] = []
        self.alpha_weights: List[float] = []
        self.L_inv: Optional[MatrixDense] = None

    def fit(self, X: Sequence[VectorND], y: Sequence[float]) -> None:
        self.X_train = [VectorND(x.data) for x in X]
        self.y_train = [float(val) for val in y]
        n = len(self.X_train)
        if n == 0:
            return

        # K(X, X) + sigma_n^2 * I
        k_matrix = self.kernel.compute_gram_matrix(self.X_train)
        for i in range(n):
            k_matrix[i][i] += self.noise_var

        k_dense = MatrixDense.from_nested(k_matrix)
        # Solve (K + sigma^2*I) * alpha = y
        self.alpha_weights = k_dense.solve_linear_system_gaussian(self.y_train)

    def predict(self, x_star: VectorND) -> Tuple[float, float]:
        """
        Returns (posterior_mean, posterior_variance) for query point x_star.
        """
        n = len(self.X_train)
        if n == 0:
            return 0.0, 1.0

        k_star = [self.kernel(x_star, x_train) for x_train in self.X_train]
        
        # Mean = k_star^T * alpha
        mean = sum(k_star[i] * self.alpha_weights[i] for i in range(n))

        # Prior variance k(x*, x*)
        k_self = self.kernel(x_star, x_star)
        
        # Variance reduction from observation: var = k(x*, x*) - k_star^T (K + sigma^2*I)^-1 k_star
        # Approximate estimation via weight projection
        k_dense = MatrixDense.from_nested(self.kernel.compute_gram_matrix(self.X_train))
        for i in range(n):
            k_dense[i][i] += self.noise_var
        try:
            v_vec = k_dense.solve_linear_system_gaussian(k_star)
            var_reduction = sum(k_star[i] * v_vec[i] for i in range(n))
        except ValueError:
            var_reduction = 0.0

        posterior_var = max(1e-6, k_self - var_reduction)
        return mean, posterior_var


class BayesianOptimizer:
    """
    Bayesian Optimization for black-box physical/hyperparameter search.
    Acquisition Functions: Expected Improvement (EI), Upper Confidence Bound (UCB).
    """
    def __init__(
        self,
        bounds_min: Sequence[float],
        bounds_max: Sequence[float],
        kernel: Optional[BaseKernel] = None,
        acquisition: str = "ucb",
        beta: float = 2.0,
        seed: Optional[int] = None
    ) -> None:
        self.bounds_min = [float(v) for v in bounds_min]
        self.bounds_max = [float(v) for v in bounds_max]
        self.dim = len(self.bounds_min)
        self.gp = GaussianProcessRegressor(kernel=kernel)
        self.acquisition = acquisition.lower()
        self.beta = beta
        self.rng = random.Random(seed)

        self.history_X: List[VectorND] = []
        self.history_y: List[float] = []

    def tell(self, x: Sequence[float], y: float) -> None:
        """Register a new evaluated experiment observation."""
        self.history_X.append(VectorND(x))
        self.history_y.append(float(y))
        self.gp.fit(self.history_X, self.history_y)

    def _eval_acquisition(self, x: VectorND) -> float:
        """Evaluates acquisition function at point x."""
        mean, var = self.gp.predict(x)
        std = math.sqrt(var)

        if self.acquisition == "ucb":
            # Upper Confidence Bound (for maximization)
            return mean + self.beta * std
        elif self.acquisition == "ei":
            # Expected Improvement
            if not self.history_y:
                return std
            best_y = max(self.history_y)
            delta = mean - best_y
            if std < 1e-9:
                return 0.0
            z = delta / std
            pdf_z = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * z * z)
            cdf_z = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
            return delta * cdf_z + std * pdf_z
        return mean

    def ask(self, num_candidates: int = 200) -> List[float]:
        """Proposes next best parameter point to evaluate."""
        if len(self.history_X) < 3:
            # Initial random exploration
            return [self.rng.uniform(self.bounds_min[i], self.bounds_max[i]) for i in range(self.dim)]

        best_cand = None
        best_acq = -float('inf')

        for _ in range(num_candidates):
            cand = VectorND([self.rng.uniform(self.bounds_min[i], self.bounds_max[i]) for i in range(self.dim)])
            acq_val = self._eval_acquisition(cand)
            if acq_val > best_acq:
                best_acq = acq_val
                best_cand = cand

        return best_cand.to_list() if best_cand else [0.0] * self.dim
