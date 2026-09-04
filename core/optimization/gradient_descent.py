"""
JobGuard Core Optimization - Advanced First-Order Gradient Optimizers
Implements SGD with Momentum, Nesterov Accelerated Gradient (NAG),
RMSprop, and AdamW (Decoupled Weight Decay Regularization).
"""

import math
from typing import List, Tuple, Callable, Optional


class AdamWOptimizer:
    """AdamW optimizer with decoupled weight decay."""

    def __init__(
        self,
        params: List[float],
        lr: float = 0.001,
        betas: Tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 0.01
    ):
        self.params = params
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay

        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.t = 0

    def step(self, grads: List[float]) -> List[float]:
        self.t += 1
        n = len(self.params)

        for i in range(n):
            g = grads[i]
            
            # Weight decay step: theta = theta - lr * weight_decay * theta
            self.params[i] -= self.lr * self.weight_decay * self.params[i]

            # Biased first and second moment estimate updates
            self.m[i] = self.beta1 * self.m[i] + (1.0 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1.0 - self.beta2) * (g ** 2)

            # Bias correction
            m_hat = self.m[i] / (1.0 - math.pow(self.beta1, self.t))
            v_hat = self.v[i] / (1.0 - math.pow(self.beta2, self.t))

            # Parameter update
            self.params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.eps)

        return list(self.params)
