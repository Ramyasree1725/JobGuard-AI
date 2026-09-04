"""
JobGuard Core Data Pipeline Architecture
Provides Directed Acyclic Graph (DAG) workflow execution, streaming window processors,
schema enforcement, resilient batch ETL transformations, and lockless ring storage buffers.
"""

from .dag_executor import DAGExecutor, TaskNode, TaskResult, TaskState
from .stream_processor import StreamProcessor, SlidingWindow, TumblingWindow, EventRecord
from .schema_validator import SchemaValidator, FieldDefinition, ValidationError
from .batch_etl import BatchETLEngine, RecordTransformStep, PartitionedDataSet
from .storage_buffer import RingBuffer, AppendOnlyWAL, MemoryMappedCache

__all__ = [
    "DAGExecutor",
    "TaskNode",
    "TaskResult",
    "TaskState",
    "StreamProcessor",
    "SlidingWindow",
    "TumblingWindow",
    "EventRecord",
    "SchemaValidator",
    "FieldDefinition",
    "ValidationError",
    "BatchETLEngine",
    "RecordTransformStep",
    "PartitionedDataSet",
    "RingBuffer",
    "AppendOnlyWAL",
    "MemoryMappedCache",
]
