"""
Aetheris Distributed Consensus: Cryptographic Merkle-DAG State Accumulator
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import hashlib
import json
from typing import List, Dict, Any, Optional, Sequence


class MerkleDAGNode:
    """Content-Addressed Node in Merkle Directed Acyclic Graph (DAG)."""
    __slots__ = ('data_payload', 'parent_hashes', 'node_hash', 'timestamp')

    def __init__(self, payload: Dict[str, Any], parent_hashes: Optional[Sequence[str]] = None, timestamp: float = 0.0) -> None:
        self.data_payload = payload
        self.parent_hashes = sorted(list(parent_hashes)) if parent_hashes is not None else []
        self.timestamp = timestamp
        self.node_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        serialized = json.dumps(self.data_payload, sort_keys=True)
        parents_str = ":".join(self.parent_hashes)
        raw = f"{serialized}|{parents_str}|{self.timestamp}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hash": self.node_hash,
            "parents": self.parent_hashes,
            "timestamp": self.timestamp,
            "payload": self.data_payload
        }


class MerkleDAGAccumulator:
    """
    Cryptographic Merkle-DAG state store ensuring verifiable lineage,
    auditability, and consensus reconciliation for distributed multi-agent operations.
    """
    def __init__(self) -> None:
        self.nodes_by_hash: Dict[str, MerkleDAGNode] = {}
        self.frontier_tips: List[str] = [] # Current leaf nodes
        self.genesis_hash: Optional[str] = None
        self._init_genesis()

    def _init_genesis(self) -> None:
        genesis = MerkleDAGNode({"event": "GENESIS_BLOCK", "system": "Aetheris-Consensus"}, timestamp=0.0)
        self.nodes_by_hash[genesis.node_hash] = genesis
        self.frontier_tips = [genesis.node_hash]
        self.genesis_hash = genesis.node_hash

    def append_state(self, payload: Dict[str, Any], timestamp: float) -> str:
        """Appends new state node referencing current frontier tips."""
        new_node = MerkleDAGNode(payload, parent_hashes=self.frontier_tips, timestamp=timestamp)
        self.nodes_by_hash[new_node.node_hash] = new_node
        self.frontier_tips = [new_node.node_hash]
        return new_node.node_hash

    def verify_node_integrity(self, node_hash: str) -> bool:
        """Cryptographically verifies that node hash matches its payload and parents."""
        node = self.nodes_by_hash.get(node_hash)
        if node is None:
            return False
        return node.node_hash == node._compute_hash()

    def generate_audit_proof(self, target_hash: str) -> List[Dict[str, Any]]:
        """Backtracks DAG lineage from target node to Genesis."""
        proof: List[Dict[str, Any]] = []
        curr = target_hash

        while curr in self.nodes_by_hash:
            node = self.nodes_by_hash[curr]
            proof.append(node.to_dict())
            if not node.parent_hashes or curr == self.genesis_hash:
                break
            curr = node.parent_hashes[0]

        return proof
