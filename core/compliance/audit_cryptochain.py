"""
JobGuard Core Compliance - Tamper-Evident Audit Log Cryptochain
Maintains a sequential, hash-chained Merkle DAG of all risk assessments,
enabling verifiable audit proofs for legal and law enforcement proceedings.
"""

import hashlib
import time
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class AuditRecord:
    record_id: str
    action: str
    user_id: str
    risk_score: float
    verdict: str
    timestamp: float
    metadata_hash: str


@dataclass
class MerkleProof:
    leaf_hash: str
    root_hash: str
    audit_path: List[Tuple[str, str]]  # (hash, 'left'|'right')


@dataclass
class AuditBlock:
    block_index: int
    timestamp: float
    previous_block_hash: str
    merkle_root: str
    records: List[AuditRecord]
    block_hash: str


class AuditCryptoChain:
    """Immutable hash-chained append-only log ledger for candidate compliance."""

    def __init__(self):
        self.chain: List[AuditBlock] = []
        self._uncommitted_records: List[AuditRecord] = []
        self._genesis_block()

    def _genesis_block(self) -> None:
        genesis = AuditBlock(
            block_index=0,
            timestamp=1700000000.0,
            previous_block_hash="0" * 64,
            merkle_root="0" * 64,
            records=[],
            block_hash=hashlib.sha256(b"jobguard-compliance-genesis-block-2026").hexdigest()
        )
        self.chain.append(genesis)

    def record_assessment(self, action: str, user_id: str, risk_score: float, verdict: str, raw_payload: Dict[str, Any]) -> str:
        """Record an immutable assessment event; returns unique record ID."""
        payload_json = json.dumps(raw_payload, sort_keys=True)
        meta_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        rec_id = f"REC-{len(self.chain)}-{len(self._uncommitted_records)+1:04d}-{meta_hash[:8]}"

        rec = AuditRecord(
            record_id=rec_id,
            action=action,
            user_id=user_id,
            risk_score=risk_score,
            verdict=verdict,
            timestamp=time.time(),
            metadata_hash=meta_hash
        )
        self._uncommitted_records.append(rec)

        if len(self._uncommitted_records) >= 10:
            self.commit_block()

        return rec_id

    def commit_block(self) -> Optional[AuditBlock]:
        """Seal current uncommitted records into a new cryptographically chained block."""
        if not self._uncommitted_records:
            return None

        prev_block = self.chain[-1]
        records = list(self._uncommitted_records)
        self._uncommitted_records.clear()

        # Compute Merkle Root
        merkle_root = self._compute_merkle_root(records)
        now = time.time()
        idx = prev_block.block_index + 1

        # Block Hash: SHA-256(index + timestamp + prev_hash + merkle_root)
        header = f"{idx}:{now}:{prev_block.block_hash}:{merkle_root}".encode("utf-8")
        block_hash = hashlib.sha256(header).hexdigest()

        block = AuditBlock(
            block_index=idx,
            timestamp=now,
            previous_block_hash=prev_block.block_hash,
            merkle_root=merkle_root,
            records=records,
            block_hash=block_hash
        )
        self.chain.append(block)
        return block

    def verify_chain_integrity(self) -> Tuple[bool, List[str]]:
        """Verify hash continuity and Merkle roots across the entire chain."""
        errors: List[str] = []
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.previous_block_hash != prev.block_hash:
                errors.append(f"Block {curr.block_index} previous_block_hash mismatch!")

            header = f"{curr.block_index}:{curr.timestamp}:{curr.previous_block_hash}:{curr.merkle_root}".encode("utf-8")
            expected_hash = hashlib.sha256(header).hexdigest()
            if curr.block_hash != expected_hash:
                errors.append(f"Block {curr.block_index} block_hash tampering detected!")

            computed_root = self._compute_merkle_root(curr.records)
            if curr.merkle_root != computed_root:
                errors.append(f"Block {curr.block_index} Merkle root mismatch!")

        return len(errors) == 0, errors

    @classmethod
    def _compute_merkle_root(cls, records: List[AuditRecord]) -> str:
        if not records:
            return "0" * 64
        hashes = [cls._hash_record(r) for r in records]
        
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_level = []
            for j in range(0, len(hashes), 2):
                combined = hashes[j] + hashes[j + 1]
                new_level.append(hashlib.sha256(combined.encode("utf-8")).hexdigest())
            hashes = new_level
            
        return hashes[0]

    @staticmethod
    def _hash_record(r: AuditRecord) -> str:
        raw = f"{r.record_id}:{r.action}:{r.user_id}:{r.risk_score}:{r.verdict}:{r.timestamp}:{r.metadata_hash}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
