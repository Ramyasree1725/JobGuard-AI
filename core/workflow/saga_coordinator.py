"""
JobGuard Core Workflow - Distributed Saga Transaction Coordinator
Executes multi-step asynchronous business transactions with automatic
compensating actions (rollback) upon downstream step failures.
"""

import time
import enum
from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field


class SagaStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    FAILED = "FAILED"


@dataclass
class SagaStep:
    name: str
    action_fn: Callable[[Dict[str, Any]], Any]
    compensate_fn: Optional[Callable[[Dict[str, Any], Any], None]] = None
    timeout_sec: float = 10.0


@dataclass
class SagaExecutionResult:
    saga_id: str
    status: SagaStatus
    completed_steps: List[str]
    compensated_steps: List[str]
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    context: Dict[str, Any] = field(default_factory=dict)


class SagaCoordinator:
    """Orchestrates sequential transactions and backward compensation on fault."""

    def __init__(self, saga_name: str):
        self.saga_name = saga_name
        self._steps: List[SagaStep] = []

    def add_step(self, step: SagaStep) -> "SagaCoordinator":
        self._steps.append(step)
        return self

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> SagaExecutionResult:
        """Run all saga steps forward; if any step raises an exception, execute backward compensation."""
        start_time = time.monotonic()
        saga_id = f"SAGA-{self.saga_name}-{int(time.time()*1000)}"
        context = dict(initial_context or {})
        
        executed_steps: List[Tuple[SagaStep, Any]] = []
        completed_step_names: List[str] = []
        compensated_step_names: List[str] = []
        error_msg = None
        status = SagaStatus.RUNNING

        # Forward execution phase
        for step in self._steps:
            try:
                output = step.action_fn(context)
                context[f"{step.name}_output"] = output
                executed_steps.append((step, output))
                completed_step_names.append(step.name)
            except Exception as ex:
                error_msg = f"Step '{step.name}' failed: {str(ex)}"
                status = SagaStatus.COMPENSATING
                break

        # Backward compensation phase if failure occurred
        if status == SagaStatus.COMPENSATING:
            for step, step_output in reversed(executed_steps):
                if step.compensate_fn:
                    try:
                        step.compensate_fn(context, step_output)
                        compensated_step_names.append(step.name)
                    except Exception as comp_ex:
                        error_msg += f" | Compensation failed for '{step.name}': {str(comp_ex)}"

            status = SagaStatus.COMPENSATED if len(compensated_step_names) == len(executed_steps) else SagaStatus.FAILED
        else:
            status = SagaStatus.COMPLETED

        elapsed = (time.monotonic() - start_time) * 1000.0

        return SagaExecutionResult(
            saga_id=saga_id,
            status=status,
            completed_steps=completed_step_names,
            compensated_steps=compensated_step_names,
            error_message=error_msg,
            execution_time_ms=round(elapsed, 2),
            context=context
        )
