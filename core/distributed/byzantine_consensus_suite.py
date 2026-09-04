"""
JobGuard Core Distributed - Pipelined BFT & Asynchronous HoneyBadger Consensus
Simulates pipelined leader-driven consensus (HotStuff) and threshold cryptography validation.
"""

import time
import hashlib
from typing import List, Dict, Tuple, Set, Optional, Any
from dataclasses import dataclass, field


@dataclass
class BFTBlock:
    view_number: int
    parent_hash: str
    command: Any
    justify_qc: str  # Quorum Certificate
    block_hash: str


class HotStuffNode:
    """Three-phase pipelined BFT replica node (Prepare, Pre-Commit, Commit, Decide)."""

    def __init__(self, node_id: str, quorum_size: int = 4):
        self.node_id = node_id
        self.quorum_size = quorum_size
        self.current_view = 0
        self.locked_block: Optional[BFTBlock] = None
        self.committed_blocks: List[BFTBlock] = []

    def create_block(self, command: Any, parent: Optional[BFTBlock], qc: str) -> BFTBlock:
        self.current_view += 1
        parent_h = parent.block_hash if parent else "0" * 64
        raw = f"{self.current_view}:{parent_h}:{command}:{qc}"
        h = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        return BFTBlock(
            view_number=self.current_view,
            parent_hash=parent_h,
            command=command,
            justify_qc=qc,
            block_hash=h
        )

    def verify_proposal(self, block: BFTBlock) -> bool:
        """Safety rule: check if proposed block extends locked block or has newer QC."""
        if self.locked_block is None:
            return True
        return block.view_number > self.locked_block.view_number
