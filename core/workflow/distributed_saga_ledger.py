"""
JobGuard Core Workflow - Distributed Saga Ledger & Compensating Transaction Coordinator
Coordinates multi-stage distributed transactions across threat intelligence microservices,
payment verification APIs, and compliance auditing vaults with automated rollbacks.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid


class SagaStepStatus(Enum):
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"


class SagaOverallStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    ABORTED_AND_COMPENSATED = "ABORTED_AND_COMPENSATED"
    COMPENSATION_FAILED = "COMPENSATION_FAILED"


@dataclass
class SagaStep:
    step_id: str
    step_name: str
    action_fn: Callable[[Dict[str, Any]], bool]
    compensation_fn: Callable[[Dict[str, Any]], bool]
    status: SagaStepStatus = SagaStepStatus.PENDING
    execution_duration_ms: float = 0.0
    error_message: Optional[str] = None


@dataclass
class SagaExecutionRecord:
    saga_id: str
    saga_type: str
    status: SagaOverallStatus
    context_payload: Dict[str, Any]
    steps: List[SagaStep]
    started_at: float
    finished_at: Optional[float] = None


class DistributedSagaLedger:
    """Orchestrates forward transactions and compensating reverse workflows for distributed security actions."""

    def __init__(self):
        self.saga_records: Dict[str, SagaExecutionRecord] = {}

    def create_saga(self, saga_type: str, initial_context: Dict[str, Any]) -> str:
        """Initializes a new Saga transaction record."""
        saga_id = f"SAGA-{uuid.uuid4().hex[:12].upper()}"
        record = SagaExecutionRecord(
            saga_id=saga_id,
            saga_type=saga_type,
            status=SagaOverallStatus.NOT_STARTED,
            context_payload=initial_context,
            steps=[],
            started_at=time.time()
        )
        self.saga_records[saga_id] = record
        return saga_id

    def add_step(
        self,
        saga_id: str,
        step_name: str,
        action: Callable[[Dict[str, Any]], bool],
        compensation: Callable[[Dict[str, Any]], bool]
    ) -> None:
        """Registers a forward action and reverse compensating hook to a saga pipeline."""
        record = self.saga_records[saga_id]
        step = SagaStep(
            step_id=f"STEP-{len(record.steps) + 1:02d}",
            step_name=step_name,
            action_fn=action,
            compensation_fn=compensation
        )
        record.steps.append(step)

    def execute_saga(self, saga_id: str) -> SagaOverallStatus:
        """Executes all forward steps sequentially. In case of failure, executes backward compensations."""
        record = self.saga_records[saga_id]
        record.status = SagaOverallStatus.IN_PROGRESS

        completed_steps: List[SagaStep] = []
        failure_encountered = False

        for step in record.steps:
            step.status = SagaStepStatus.EXECUTING
            start = time.perf_counter()
            try:
                success = step.action_fn(record.context_payload)
                step.execution_duration_ms = (time.perf_counter() - start) * 1000.0
                if success:
                    step.status = SagaStepStatus.COMPLETED
                    completed_steps.append(step)
                else:
                    step.status = SagaStepStatus.FAILED
                    step.error_message = "Action returned false"
                    failure_encountered = True
                    break
            except Exception as ex:
                step.execution_duration_ms = (time.perf_counter() - start) * 1000.0
                step.status = SagaStepStatus.FAILED
                step.error_message = str(ex)
                failure_encountered = True
                break

        if not failure_encountered:
            record.status = SagaOverallStatus.SUCCEEDED
            record.finished_at = time.time()
            return SagaOverallStatus.SUCCEEDED

        # Backward compensation loop
        all_compensated = True
        for step in reversed(completed_steps):
            step.status = SagaStepStatus.COMPENSATING
            try:
                comp_success = step.compensation_fn(record.context_payload)
                if comp_success:
                    step.status = SagaStepStatus.COMPENSATED
                else:
                    step.status = SagaStepStatus.FAILED
                    all_compensated = False
            except Exception as ex:
                step.error_message = f"Compensation error: {str(ex)}"
                step.status = SagaStepStatus.FAILED
                all_compensated = False

        record.status = SagaOverallStatus.ABORTED_AND_COMPENSATED if all_compensated else SagaOverallStatus.COMPENSATION_FAILED
        record.finished_at = time.time()
        return record.status
