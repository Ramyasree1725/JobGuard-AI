"""
JobGuard Core Data Pipeline - DAG Task Scheduling & Dependency Engine
Coordinates multi-stage data processing graphs with topological ordering,
concurrency pools, intermediate state caching, and fault-tolerant retry policies.
"""

import time
import enum
import threading
from typing import Dict, List, Set, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed


class TaskState(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class TaskResult:
    task_id: str
    state: TaskState
    output: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    retry_count: int = 0


@dataclass
class TaskNode:
    task_id: str
    fn: Callable[..., Any]
    dependencies: Set[str] = field(default_factory=set)
    timeout_seconds: float = 30.0
    max_retries: int = 2
    retry_backoff_sec: float = 0.5
    ignore_failure: bool = False
    context_keys_in: List[str] = field(default_factory=list)
    context_key_out: Optional[str] = None


class DAGExecutor:
    """High-throughput multi-threaded DAG task execution engine."""

    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self._nodes: Dict[str, TaskNode] = {}
        self._results: Dict[str, TaskResult] = {}
        self._lock = threading.Lock()

    def add_task(self, node: TaskNode) -> "DAGExecutor":
        """Register a task node into the DAG graph."""
        with self._lock:
            self._nodes[node.task_id] = node
        return self

    def _validate_and_topological_sort(self) -> List[str]:
        """Verify graph is acyclic and return topological execution sequence."""
        in_degree: Dict[str, int] = {t_id: 0 for t_id in self._nodes}
        adj_list: Dict[str, List[str]] = {t_id: [] for t_id in self._nodes}

        for t_id, node in self._nodes.items():
            for dep in node.dependencies:
                if dep not in self._nodes:
                    raise ValueError(f"Task '{t_id}' depends on non-existent task '{dep}'")
                adj_list[dep].append(t_id)
                in_degree[t_id] += 1

        queue = [t_id for t_id, deg in in_degree.items() if deg == 0]
        sorted_order = []

        while queue:
            curr = queue.pop(0)
            sorted_order.append(curr)
            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(self._nodes):
            raise ValueError("Cycle detected in DAG task graph! Cannot schedule execution.")

        return sorted_order

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, TaskResult]:
        """Execute all DAG tasks honoring dependency constraints and concurrency pools."""
        self._validate_and_topological_sort()
        
        context = dict(initial_context or {})
        completed_tasks: Set[str] = set()
        failed_tasks: Set[str] = set()
        results: Dict[str, TaskResult] = {}
        
        # Track pending task dependencies
        pending_dependencies: Dict[str, Set[str]] = {
            t_id: set(node.dependencies) for t_id, node in self._nodes.items()
        }

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            active_futures = {}

            while len(completed_tasks) + len(failed_tasks) < len(self._nodes):
                # Submit tasks whose dependencies are satisfied
                ready_tasks = [
                    t_id for t_id, deps in pending_dependencies.items()
                    if len(deps) == 0 and t_id not in active_futures and t_id not in completed_tasks and t_id not in failed_tasks
                ]

                for t_id in ready_tasks:
                    node = self._nodes[t_id]
                    # Check if any dependency failed and cannot be ignored
                    dep_failed = any(dep in failed_tasks and not self._nodes[dep].ignore_failure for dep in node.dependencies)
                    if dep_failed:
                        failed_tasks.add(t_id)
                        results[t_id] = TaskResult(
                            task_id=t_id,
                            state=TaskState.SKIPPED,
                            error="Skipped due to upstream dependency failure"
                        )
                        continue

                    # Prepare arguments
                    args = [context.get(k) for k in node.context_keys_in]
                    future = executor.submit(self._run_task_with_retry, node, args)
                    active_futures[future] = t_id

                if not active_futures:
                    break

                # Wait for any active task to finish
                for future in as_completed(active_futures):
                    t_id = active_futures.pop(future)
                    task_result = future.result()
                    results[t_id] = task_result

                    if task_result.state == TaskState.COMPLETED:
                        completed_tasks.add(t_id)
                        if self._nodes[t_id].context_key_out and task_result.output is not None:
                            context[self._nodes[t_id].context_key_out] = task_result.output
                    else:
                        failed_tasks.add(t_id)

                    # Update downstream pending dependencies
                    for other_id in pending_dependencies:
                        pending_dependencies[other_id].discard(t_id)

                    # Break to evaluate new ready tasks
                    break

        self._results = results
        return results

    def _run_task_with_retry(self, node: TaskNode, args: List[Any]) -> TaskResult:
        """Execute single task function with exponential backoff retry logic."""
        start_time = time.monotonic()
        retry_count = 0
        last_error = None

        for attempt in range(node.max_retries + 1):
            try:
                out = node.fn(*args) if args else node.fn()
                elapsed = (time.monotonic() - start_time) * 1000.0
                return TaskResult(
                    task_id=node.task_id,
                    state=TaskState.COMPLETED,
                    output=out,
                    execution_time_ms=round(elapsed, 2),
                    retry_count=retry_count
                )
            except Exception as e:
                last_error = str(e)
                retry_count += 1
                if attempt < node.max_retries:
                    time.sleep(node.retry_backoff_sec * (2 ** attempt))

        elapsed = (time.monotonic() - start_time) * 1000.0
        return TaskResult(
            task_id=node.task_id,
            state=TaskState.FAILED,
            error=last_error,
            execution_time_ms=round(elapsed, 2),
            retry_count=retry_count
        )
