"""
JobGuard Core Distributed - Anti-Entropy Merkle Tree Synchronization Engine
Performs hierarchical hash comparison across distributed replica nodes to detect
and repair out-of-sync threat intelligence keys with minimal network transfer.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import hashlib


@dataclass
class MerkleNode:
    hash_value: str
    left_child: Optional["MerkleNode"] = None
    right_child: Optional["MerkleNode"] = None
    key_range_min: int = 0
    key_range_max: int = 0
    is_leaf: bool = False
    leaf_key: Optional[str] = None
    leaf_val_hash: Optional[str] = None


class AntiEntropyMerkleSync:
    """Constructs Merkle partition trees to identify differing key ranges between replicas."""

    def __init__(self, key_space_max: int = 10000):
        self.key_space_max = key_space_max
        self.key_store: Dict[str, str] = {}  # key -> value_hash

    def set_key(self, key: str, value_hash: str) -> None:
        self.key_store[key] = value_hash

    def build_tree(self) -> MerkleNode:
        """Builds binary Merkle tree over the current key-value dataset."""
        if not self.key_store:
            return MerkleNode(hash_value=hashlib.sha256(b"EMPTY").hexdigest(), is_leaf=True)

        sorted_keys = sorted(self.key_store.items(), key=lambda x: int(hashlib.md5(x[0].encode()).hexdigest()[:6], 16))
        leaf_nodes = [
            MerkleNode(
                hash_value=val_hash,
                is_leaf=True,
                leaf_key=k,
                leaf_val_hash=val_hash
            )
            for k, val_hash in sorted_keys
        ]

        current_level = leaf_nodes
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                    combined = hashlib.sha256((left.hash_value + right.hash_value).encode("utf-8")).hexdigest()
                    parent = MerkleNode(hash_value=combined, left_child=left, right_child=right)
                else:
                    parent = left
                next_level.append(parent)
            current_level = next_level

        return current_level[0]

    def find_differing_keys(self, remote_tree: MerkleNode, local_tree: Optional[MerkleNode] = None) -> List[str]:
        """Recursively traverses two Merkle trees to pinpoint exactly which keys are desynchronized."""
        if local_tree is None:
            local_tree = self.build_tree()

        differing: List[str] = []

        def _traverse(n_local: Optional[MerkleNode], n_remote: Optional[MerkleNode]):
            if not n_local or not n_remote:
                return
            if n_local.hash_value == n_remote.hash_value:
                return  # Identical subtree

            if n_local.is_leaf and n_remote.is_leaf:
                if n_local.leaf_key:
                    differing.append(n_local.leaf_key)
                return

            # Recurse children
            _traverse(n_local.left_child, n_remote.left_child)
            _traverse(n_local.right_child, n_remote.right_child)

        _traverse(local_tree, remote_tree)
        return list(set(differing))
