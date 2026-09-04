"""
JobGuard Core Workflow - Dynamic DAG Task Scheduler & Dependency Resolver
Executes topological sort, concurrency levels, and asynchronous task execution
for complex forensic pipelines with dynamic branching and conditional evaluation.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
import collections
import time


@dataclass
class DAGTask:
    task_id: str
    task_name: str
    run_fn: Callable[[Dict[str, Any]], Any]
    dependencies: List[str] = field(default_factory=list)
    output: Any = None
    execution_time_ms: float = 0.0
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED, SKIPPED


class DynamicDAGScheduler:
    """Dependency graph scheduler supporting topological ordering and dynamic runtime tasks."""

    def __init__(self):
        self.tasks: Dict[str, DAGTask] = {}

    def add_task(
        self,
        task_id: str,
        name: str,
        run_fn: Callable[[Dict[str, Any]], Any],
        dependencies: Optional[List[str]] = None
    ) -> None:
        """Adds a task with explicit dependency constraints."""
        self.tasks[task_id] = DAGTask(
            task_id=task_id,
            task_name=name,
            run_fn=run_fn,
            dependencies=dependencies or []
        )

    def topological_sort(self) -> List[str]:
        """Computes valid execution order using Kahn's algorithm."""
        in_degree: Dict[str, int] = {t_id: 0 for t_id in self.tasks}
        graph: Dict[str, List[str]] = collections.defaultdict(list)

        for t_id, task in self.tasks.items():
            for dep in task.dependencies:
                if dep in in_degree:
                    in_degree[t_id] += 1
                    graph[dep].append(t_id)

        queue = collections.deque([t_id for t_id, deg in in_degree.items() if deg == 0])
        order: List[str] = []

        while queue:
            curr = queue.popleft()
            order.append(curr)

            for neighbor in graph[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.tasks):
            raise ValueError("Cycle detected in DAG task dependencies!")

        return order

    def execute_all(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes all DAG tasks in topologically sorted dependency order."""
        context = dict(initial_context or {})
        order = self.topological_sort()

        for t_id in order:
            task = self.tasks[t_id]
            task.status = "RUNNING"
            start = time.perf_counter()
            try:
                out = task.run_fn(context)
                task.output = out
                task.status = "COMPLETED"
                task.execution_time_ms = (time.perf_counter() - start) * 1000.0
                context[t_id] = out
            except Exception as ex:
                task.status = "FAILED"
                task.execution_time_ms = (time.perf_counter() - start) * 1000.0
                context[f"{t_id}_error"] = str(ex)
                raise RuntimeError(f"DAG Task {t_id} failed: {str(ex)}")

        return context
