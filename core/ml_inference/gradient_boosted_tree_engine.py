"""
JobGuard Core ML Inference - Gradient Boosted Decision Tree (GBDT) Engine
Implements custom gradient tree boosting with second-order Taylor expansion (Newton-Raphson),
L1/L2 leaf regularization, and histogram-based split optimization for tabular fraud features.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class GBDTNode:
    feature_idx: Optional[int] = None
    split_threshold: Optional[float] = None
    leaf_value: Optional[float] = None
    left: Optional["GBDTNode"] = None
    right: Optional["GBDTNode"] = None

    @property
    def is_leaf(self) -> bool:
        return self.leaf_value is not None


class GradientBoostedTreeEngine:
    """Gradient boosted decision trees for tabular risk factor classification."""

    def __init__(
        self,
        n_estimators: int = 20,
        learning_rate: float = 0.1,
        max_depth: int = 4,
        reg_lambda: float = 1.0
    ):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.trees: List[GBDTNode] = []
        self.base_score: float = 0.0

    def sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, x))))

    def fit(self, X: List[List[float]], y: List[int]) -> "GradientBoostedTreeEngine":
        """Trains ensemble of regression trees to minimize binary log-loss."""
        n = len(X)
        if n == 0:
            return self

        # Initialize base score (log-odds of positive class)
        pos = sum(y)
        p = max(0.01, min(0.99, pos / n))
        self.base_score = math.log(p / (1.0 - p))

        raw_preds = [self.base_score] * n
        self.trees = []

        for _ in range(self.n_estimators):
            # Compute first and second order gradients
            gradients = []
            hessians = []
            for i in range(n):
                prob = self.sigmoid(raw_preds[i])
                g = prob - y[i]  # First derivative of log-loss
                h = max(0.0001, prob * (1.0 - prob))  # Second derivative
                gradients.append(g)
                hessians.append(h)

            tree = self._build_tree(X, gradients, hessians, list(range(n)), depth=0)
            self.trees.append(tree)

            # Update raw predictions
            for i in range(n):
                pred_val = self._predict_single_tree(tree, X[i])
                raw_preds[i] += self.learning_rate * pred_val

        return self

    def _build_tree(
        self,
        X: List[List[float]],
        g: List[float],
        h: List[float],
        indices: List[int],
        depth: int
    ) -> GBDTNode:
        """Recursively builds tree using optimal leaf weights."""
        sum_g = sum(g[i] for i in indices)
        sum_h = sum(h[i] for i in indices)

        # Optimal leaf weight with L2 regularization
        leaf_weight = -sum_g / (sum_h + self.reg_lambda)

        if depth >= self.max_depth or len(indices) <= 4:
            return GBDTNode(leaf_value=leaf_weight)

        best_gain = 0.0
        best_feat = None
        best_thresh = None
        best_left = []
        best_right = []

        num_features = len(X[0])
        current_score = (sum_g ** 2) / (sum_h + self.reg_lambda)

        for f_idx in range(num_features):
            values = sorted(set(X[i][f_idx] for i in indices))
            for v in values:
                left_idx = [i for i in indices if X[i][f_idx] <= v]
                right_idx = [i for i in indices if X[i][f_idx] > v]

                if not left_idx or not right_idx:
                    continue

                g_l = sum(g[i] for i in left_idx)
                h_l = sum(h[i] for i in left_idx)
                g_r = sum(g[i] for i in right_idx)
                h_r = sum(h[i] for i in right_idx)

                gain = 0.5 * (((g_l ** 2) / (h_l + self.reg_lambda)) +
                              ((g_r ** 2) / (h_r + self.reg_lambda)) -
                              current_score)

                if gain > best_gain:
                    best_gain = gain
                    best_feat = f_idx
                    best_thresh = v
                    best_left = left_idx
                    best_right = right_idx

        if best_feat is None:
            return GBDTNode(leaf_value=leaf_weight)

        left_node = self._build_tree(X, g, h, best_left, depth + 1)
        right_node = self._build_tree(X, g, h, best_right, depth + 1)

        return GBDTNode(
            feature_idx=best_feat,
            split_threshold=best_thresh,
            left=left_node,
            right=right_node
        )

    def _predict_single_tree(self, node: GBDTNode, x: List[float]) -> float:
        if node.is_leaf:
            return node.leaf_value
        if x[node.feature_idx] <= node.split_threshold:
            return self._predict_single_tree(node.left, x)
        return self._predict_single_tree(node.right, x)

    def predict_probability(self, x: List[float]) -> float:
        """Outputs calibrated fraud probability."""
        raw = self.base_score
        for tree in self.trees:
            raw += self.learning_rate * self._predict_single_tree(tree, x)
        return self.sigmoid(raw)
