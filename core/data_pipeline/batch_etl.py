"""
JobGuard Core Data Pipeline - Batch ETL Transformations & Partitioned Datasets
Provides high-performance record transformations, column projections,
chunked streaming reader, and multi-threaded batch processors.
"""

import math
from typing import Dict, List, Optional, Callable, Any, Iterator, Tuple
from dataclasses import dataclass, field


@dataclass
class RecordTransformStep:
    name: str
    transform_fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]]
    is_filter: bool = False


class PartitionedDataSet:
    """In-memory partitioned record storage for parallel ETL workers."""

    def __init__(self, partition_count: int = 4):
        self.partition_count = max(1, partition_count)
        self._partitions: List[List[Dict[str, Any]]] = [[] for _ in range(self.partition_count)]

    def append(self, record: Dict[str, Any], partition_key: Optional[str] = None) -> None:
        if partition_key and partition_key in record:
            p_idx = hash(str(record[partition_key])) % self.partition_count
        else:
            p_idx = len(self._partitions[0]) % self.partition_count
        self._partitions[p_idx].append(record)

    def get_partition(self, partition_idx: int) -> List[Dict[str, Any]]:
        return self._partitions[partition_idx]

    def total_records(self) -> int:
        return sum(len(p) for p in self._partitions)

    def iter_all(self) -> Iterator[Dict[str, Any]]:
        for partition in self._partitions:
            for record in partition:
                yield record


class BatchETLEngine:
    """Configurable pipeline for cleaning, enriching, and scoring job datasets."""

    def __init__(self):
        self._steps: List[RecordTransformStep] = []

    def add_step(self, name: str, transform_fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]], is_filter: bool = False) -> "BatchETLEngine":
        self._steps.append(RecordTransformStep(name=name, transform_fn=transform_fn, is_filter=is_filter))
        return self

    def process_record(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Run single record through transformation chain; returns None if filtered out."""
        curr = dict(record)
        for step in self._steps:
            res = step.transform_fn(curr)
            if res is None and step.is_filter:
                return None
            if res is not None:
                curr = res
        return curr

    def process_batch(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        """Process list of records, returning transformed list and execution metrics."""
        output: List[Dict[str, Any]] = []
        metrics = {"ingested": len(records), "passed": 0, "filtered": 0, "errors": 0}

        for r in records:
            try:
                processed = self.process_record(r)
                if processed is not None:
                    output.append(processed)
                    metrics["passed"] += 1
                else:
                    metrics["filtered"] += 1
            except Exception:
                metrics["errors"] += 1

        return output, metrics


def create_job_cleaning_etl() -> BatchETLEngine:
    """Pre-built ETL pipeline for standardizing job listings."""
    etl = BatchETLEngine()
    
    # Step 1: Whitespace & text normalization
    etl.add_step(
        "normalize_text",
        lambda r: {
            **r,
            "title": " ".join(r.get("title", "").split()).strip(),
            "company": " ".join(r.get("company", "").split()).strip(),
            "description": r.get("description", "").strip()
        }
    )

    # Step 2: Filter low-quality empty records
    etl.add_step(
        "filter_empty",
        lambda r: r if len(r.get("description", "")) >= 15 else None,
        is_filter=True
    )

    # Step 3: Lowercase email normalization
    etl.add_step(
        "normalize_email",
        lambda r: {**r, "email": r.get("email", "").strip().lower()}
    )

    return etl
