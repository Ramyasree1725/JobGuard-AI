"""
JobGuard Core ML - Probability Calibration & Confidence Post-Processing
Temperature scaling, Platt scaling, and Isotonic regression to transform
raw neural network logit outputs into true statistical probabilities.
"""

import math
from typing import List, Tuple, Dict, Any, Optional


class TemperatureScaling:
    """Post-processing temperature scalar for calibrated Softmax outputs."""

    def __init__(self, initial_temperature: float = 1.5):
        self.temperature = max(0.01, float(initial_temperature))

    def calibrate_logits(self, logits: List[float]) -> List[float]:
        """Apply learned temperature scaling and return calibrated probabilities."""
        scaled_logits = [l / self.temperature for l in logits]
        max_logit = max(scaled_logits)
        exp_vals = [math.exp(max(-50.0, min(50.0, l - max_logit))) for l in scaled_logits]
        sum_exp = sum(exp_vals)
        return [v / sum_exp for v in exp_vals]

    def fit(self, logits_list: List[List[float]], true_labels: List[int], lr: float = 0.01, epochs: int = 50) -> None:
        """Gradient descent on Negative Log Likelihood (NLL) to learn optimal temperature T."""
        t = self.temperature
        for _ in range(epochs):
            grad = 0.0
            for logits, label in zip(logits_list, true_labels):
                scaled = [l / t for l in logits]
                max_l = max(scaled)
                exp_v = [math.exp(max(-50.0, min(50.0, l - max_l))) for l in scaled]
                sum_e = sum(exp_v)
                probs = [v / sum_e for v in exp_v]
                
                # Derivative of NLL w.r.t temperature T
                p_y = probs[label]
                exp_term = sum(probs[i] * logits[i] for i in range(len(logits)))
                grad += -(logits[label] - exp_term) / (t ** 2)

            t = max(0.1, t - lr * (grad / len(logits_list)))
        self.temperature = round(t, 4)


class PlattScaling:
    """Logistic calibration for single-class raw scores: P(Y=1|S) = 1 / (1 + exp(A*S + B))."""

    def __init__(self, a: float = -1.0, b: float = 0.0):
        self.a = a
        self.b = b

    def predict_probability(self, raw_score: float) -> float:
        z = self.a * raw_score + self.b
        return 1.0 / (1.0 + math.exp(-max(-50.0, min(50.0, z))))

    def fit(self, scores: List[float], labels: List[int], lr: float = 0.05, epochs: int = 100) -> None:
        a = self.a
        b = self.b
        n = len(scores)

        for _ in range(epochs):
            grad_a = 0.0
            grad_b = 0.0
            for s, y in zip(scores, labels):
                z = a * s + b
                p = 1.0 / (1.0 + math.exp(-max(-50.0, min(50.0, z))))
                err = p - y
                grad_a += err * s
                grad_b += err

            a -= lr * (grad_a / n)
            b -= lr * (grad_b / n)

        self.a = round(a, 4)
        self.b = round(b, 4)


class IsotonicCalibrator:
    """Non-parametric piecewise-constant isotonic regression for monotonic score calibration."""

    def __init__(self):
        self.thresholds: List[float] = []
        self.calibrated_probs: List[float] = []

    def fit(self, scores: List[float], labels: List[int]) -> "IsotonicCalibrator":
        """Pool Adjacent Violators Algorithm (PAVA)."""
        paired = sorted(zip(scores, labels), key=lambda x: x[0])
        x_vals = [p[0] for p in paired]
        y_vals = [float(p[1]) for p in paired]
        weights = [1.0] * len(y_vals)

        blocks: List[List[float]] = [[x_vals[i], y_vals[i], weights[i]] for i in range(len(y_vals))]

        i = 0
        while i < len(blocks) - 1:
            if blocks[i][1] > blocks[i + 1][1]:
                # Violates monotonicity: pool adjacent blocks
                w1, w2 = blocks[i][2], blocks[i + 1][2]
                pooled_y = (blocks[i][1] * w1 + blocks[i + 1][1] * w2) / (w1 + w2)
                blocks[i][1] = pooled_y
                blocks[i][2] = w1 + w2
                blocks.pop(i + 1)
                if i > 0:
                    i -= 1
            else:
                i += 1

        self.thresholds = [b[0] for b in blocks]
        self.calibrated_probs = [b[1] for b in blocks]
        return self

    def calibrate(self, score: float) -> float:
        if not self.thresholds:
            return max(0.0, min(1.0, score))
        if score <= self.thresholds[0]:
            return self.calibrated_probs[0]
        if score >= self.thresholds[-1]:
            return self.calibrated_probs[-1]

        # Linear interpolation between isotonic steps
        for i in range(len(self.thresholds) - 1):
            if self.thresholds[i] <= score <= self.thresholds[i + 1]:
                t1, t2 = self.thresholds[i], self.thresholds[i + 1]
                p1, p2 = self.calibrated_probs[i], self.calibrated_probs[i + 1]
                if t2 == t1:
                    return p1
                ratio = (score - t1) / (t2 - t1)
                return p1 + ratio * (p2 - p1)

        return self.calibrated_probs[-1]
