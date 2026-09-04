"""
JobGuard Core Explainability - Surrogate Decision Trees & Rule Distillation
Extracts human-readable IF-THEN explanation rules from complex ensemble models
to provide clear justification for scam detections.
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class AttributionRule:
    rule_id: str
    conditions: List[str]  # e.g., ["free_email > 0.5", "upfront_fee > 0.0"]
    predicted_risk_tier: str
    confidence: float
    support_count: int


class TreeNode:
    def __init__(self, feature_idx: Optional[int] = None, threshold: Optional[float] = None, value: Optional[float] = None):
        self.feature_idx = feature_idx
        self.threshold = threshold
        self.value = value  # Leaf prediction
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

    def is_leaf(self) -> bool:
        return self.value is not None


class SurrogateTreeExplainer:
    """Trains a shallow interpretable decision tree surrogate on black-box model predictions."""

    def __init__(self, max_depth: int = 4, min_samples_split: int = 4):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root: Optional[TreeNode] = None
        self.feature_names: List[str] = []

    def fit(self, X: List[List[float]], y: List[float], feature_names: Optional[List[str]] = None) -> "SurrogateTreeExplainer":
        self.feature_names = feature_names or [f"f_{i}" for i in range(len(X[0])) if X]
        self.root = self._build_tree(X, y, depth=0)
        return self

    def _variance(self, targets: List[float]) -> float:
        if len(targets) <= 1:
            return 0.0
        m = sum(targets) / len(targets)
        return sum((v - m) ** 2 for v in targets) / len(targets)

    def _build_tree(self, X: List[List[float]], y: List[float], depth: int) -> TreeNode:
        num_samples = len(y)
        if num_samples == 0:
            return TreeNode(value=0.0)

        mean_val = sum(y) / num_samples
        if depth >= self.max_depth or num_samples < self.min_samples_split:
            return TreeNode(value=mean_val)

        best_feat = None
        best_thresh = None
        best_reduction = 0.0
        current_var = self._variance(y)

        num_feats = len(X[0])
        for feat in range(num_feats):
            vals = set(row[feat] for row in X)
            for thresh in vals:
                left_y = [y[i] for i in range(num_samples) if X[i][feat] <= thresh]
                right_y = [y[i] for i in range(num_samples) if X[i][feat] > thresh]
                
                if not left_y or not right_y:
                    continue

                var_reduction = current_var - (
                    (len(left_y) / num_samples) * self._variance(left_y) +
                    (len(right_y) / num_samples) * self._variance(right_y)
                )

                if var_reduction > best_reduction:
                    best_reduction = var_reduction
                    best_feat = feat
                    best_thresh = thresh

        if best_feat is None or best_reduction <= 1e-6:
            return TreeNode(value=mean_val)

        left_X = [X[i] for i in range(num_samples) if X[i][best_feat] <= best_thresh]
        left_y = [y[i] for i in range(num_samples) if X[i][best_feat] <= best_thresh]
        right_X = [X[i] for i in range(num_samples) if X[i][best_feat] > best_thresh]
        right_y = [y[i] for i in range(num_samples) if X[i][best_feat] > best_thresh]

        node = TreeNode(feature_idx=best_feat, threshold=best_thresh)
        node.left = self._build_tree(left_X, left_y, depth + 1)
        node.right = self._build_tree(right_X, right_y, depth + 1)
        return node

    def extract_rules(self) -> List[AttributionRule]:
        """Traverse tree to generate readable decision rules."""
        rules: List[AttributionRule] = []
        rule_counter = 0

        def _traverse(node: Optional[TreeNode], conditions: List[str]):
            nonlocal rule_counter
            if not node:
                return
            if node.is_leaf():
                rule_counter += 1
                val = node.value or 0.0
                tier = "CRITICAL SCAM" if val >= 60 else "SUSPICIOUS" if val >= 25 else "SAFE"
                rules.append(AttributionRule(
                    rule_id=f"RULE-{rule_counter:03d}",
                    conditions=list(conditions),
                    predicted_risk_tier=tier,
                    confidence=round(val, 1),
                    support_count=1
                ))
                return

            feat_name = self.feature_names[node.feature_idx] if node.feature_idx < len(self.feature_names) else f"f_{node.feature_idx}"
            _traverse(node.left, conditions + [f"{feat_name} <= {node.threshold:.2f}"])
            _traverse(node.right, conditions + [f"{feat_name} > {node.threshold:.2f}"])

        _traverse(self.root, [])
        return rules
