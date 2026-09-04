"""
JobGuard Core Analytics - Anomaly & Outlier Detection Algorithms
Implements Isolation Forest partitioning and Mahalanobis multivariate distance
to detect sudden surges in scam campaign activities and salary distortions.
"""

import math
import random
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class AnomalyReport:
    is_anomaly: bool
    anomaly_score: float  # 0.0 (normal) to 1.0 (extreme anomaly)
    threshold: float
    distance_metric: float
    contributing_dimensions: List[str]


class IsolationTreeNode:
    def __init__(self, split_feature: Optional[int] = None, split_value: Optional[float] = None, size: int = 0):
        self.split_feature = split_feature
        self.split_value = split_value
        self.size = size
        self.left: Optional[IsolationTreeNode] = None
        self.right: Optional[IsolationTreeNode] = None

    def is_leaf(self) -> bool:
        return self.split_feature is None


class IsolationForestAnomalyDetector:
    """Ensemble of random recursive partitioning trees for anomaly isolation."""

    def __init__(self, num_trees: int = 50, max_samples: int = 128):
        self.num_trees = num_trees
        self.max_samples = max_samples
        self.trees: List[IsolationTreeNode] = []

    def fit(self, X: List[List[float]]) -> "IsolationForestAnomalyDetector":
        n = len(X)
        if n == 0:
            return self
        
        max_height = math.ceil(math.log2(max(2, min(n, self.max_samples))))
        self.trees = []

        for _ in range(self.num_trees):
            sample_size = min(n, self.max_samples)
            sample_indices = random.sample(range(n), sample_size)
            sample_X = [X[i] for i in sample_indices]
            tree = self._build_i_tree(sample_X, current_height=0, max_height=max_height)
            self.trees.append(tree)

        return self

    def _build_i_tree(self, X: List[List[float]], current_height: int, max_height: int) -> IsolationTreeNode:
        num_samples = len(X)
        if current_height >= max_height or num_samples <= 1:
            return IsolationTreeNode(size=num_samples)

        num_feats = len(X[0])
        split_feat = random.randint(0, num_feats - 1)
        feat_vals = [row[split_feat] for row in X]
        min_v, max_v = min(feat_vals), max(feat_vals)

        if min_v == max_v:
            return IsolationTreeNode(size=num_samples)

        split_val = random.uniform(min_v, max_v)
        left_X = [row for row in X if row[split_feat] < split_val]
        right_X = [row for row in X if row[split_feat] >= split_val]

        node = IsolationTreeNode(split_feature=split_feat, split_value=split_val, size=num_samples)
        node.left = self._build_i_tree(left_X, current_height + 1, max_height)
        node.right = self._build_i_tree(right_X, current_height + 1, max_height)
        return node

    def _path_length(self, x: List[float], node: IsolationTreeNode, current_depth: int) -> float:
        if node.is_leaf():
            return current_depth + self._c_factor(node.size)
        
        feat = node.split_feature
        if x[feat] < node.split_value:
            return self._path_length(x, node.left, current_depth + 1)
        else:
            return self._path_length(x, node.right, current_depth + 1)

    @staticmethod
    def _c_factor(n: int) -> float:
        if n <= 1:
            return 0.0
        if n == 2:
            return 1.0
        # Harmonic number approximation: 2*(ln(n-1) + 0.5772156649) - (2*(n-1)/n)
        return 2.0 * (math.log(n - 1) + 0.5772156649) - (2.0 * (n - 1) / n)

    def score(self, x: List[float]) -> float:
        """Compute anomaly score in range [0, 1]. Scores > 0.6 indicate strong anomalies."""
        if not self.trees:
            return 0.0
        avg_path = sum(self._path_length(x, t, 0) for t in self.trees) / len(self.trees)
        c = self._c_factor(self.max_samples)
        if c == 0:
            return 0.0
        # s(x, n) = 2^(-E(h(x)) / c(n))
        return math.pow(2, -avg_path / c)


class MahalanobisOutlierDetector:
    """Multivariate covariance distance detector."""

    def __init__(self):
        self.mean_vector: List[float] = []
        self.inv_covariance: List[List[float]] = []

    def fit(self, X: List[List[float]]) -> "MahalanobisOutlierDetector":
        n = len(X)
        p = len(X[0])
        self.mean_vector = [sum(X[i][j] for i in range(n)) / n for j in range(p)]

        # Covariance matrix
        cov = [[0.0] * p for _ in range(p)]
        for i in range(n):
            diff = [X[i][j] - self.mean_vector[j] for j in range(p)]
            for r in range(p):
                for c in range(p):
                    cov[r][c] += diff[r] * diff[c]

        for r in range(p):
            for c in range(p):
                cov[r][c] /= max(1, n - 1)
                if r == c:
                    cov[r][c] += 1e-4  # Regularization

        # Simple diagonal inverse approximation
        self.inv_covariance = [[0.0] * p for _ in range(p)]
        for j in range(p):
            self.inv_covariance[j][j] = 1.0 / max(1e-6, cov[j][j])

        return self

    def distance(self, x: List[float]) -> float:
        p = len(x)
        diff = [x[j] - self.mean_vector[j] for j in range(p)]
        dist_sq = sum(diff[j] * self.inv_covariance[j][j] * diff[j] for j in range(p))
        return math.sqrt(max(0.0, dist_sq))
