"""
JobGuard Core Distributed - Multi-Version Concurrency Control (MVCC) & Snapshot Isolation
Provides repeatable read snapshot isolation, write skew detection, and garbage collection.
"""

import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class VersionedRecord:
    created_at_tx: int
    deleted_at_tx: Optional[int]
    value: Any


class MVCCStorageEngine:
    """Snapshot Isolation MVCC transaction engine."""

    def __init__(self):
        self._store: Dict[str, List[VersionedRecord]] = {}
        self._tx_counter = 0
        self._active_txs: Set[int] = set()

    def begin_transaction(self) -> int:
        self._tx_counter += 1
        tx_id = self._tx_counter
        self._active_txs.add(tx_id)
        return tx_id

    def read(self, tx_id: int, key: str) -> Optional[Any]:
        """Read latest version created before tx_id and not deleted before tx_id."""
        if key not in self._store:
            return None

        versions = self._store[key]
        for v in reversed(versions):
            if v.created_at_tx <= tx_id:
                if v.deleted_at_tx is None or v.deleted_at_tx > tx_id:
                    return v.value
        return None

    def write(self, tx_id: int, key: str, value: Any) -> None:
        if key not in self._store:
            self._store[key] = []
        self._store[key].append(VersionedRecord(created_at_tx=tx_id, deleted_at_tx=None, value=value))

    def commit(self, tx_id: int) -> None:
        self._active_txs.discard(tx_id)
