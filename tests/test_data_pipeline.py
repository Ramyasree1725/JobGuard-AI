"""
Unit Tests for Core Data Pipeline & Workflow Modules
"""

import unittest
from core.data_pipeline.dag_executor import DAGPipeline, TaskNode
from core.data_pipeline.schema_validator import SchemaValidator, FieldDef, StringValidator
from core.workflow.saga_coordinator import SagaCoordinator, SagaStep, SagaStatus
from core.workflow.state_machine import StateMachine, StateNode, Transition


class TestDataPipeline(unittest.TestCase):

    def test_schema_validator(self):
        schema = SchemaValidator().add_field(FieldDef(name="email", validator=StringValidator(min_len=5, regex_pattern=r"@")))
        self.assertTrue(schema.validate({"email": "test@example.com"}).is_valid)
        self.assertFalse(schema.validate({"email": "invalid"}).is_valid)

    def test_dag_pipeline_execution(self):
        pipeline = DAGPipeline("TestDAG")
        pipeline.add_node(TaskNode("t1", lambda ctx: {"a": 1}))
        pipeline.add_node(TaskNode("t2", lambda ctx: {"b": ctx["t1"]["a"] + 2}, dependencies=["t1"]))
        res = pipeline.execute()
        self.assertTrue(res.is_successful)
        self.assertEqual(res.node_outputs["t2"]["b"], 3)

    def test_saga_coordinator_forward(self):
        saga = SagaCoordinator("TestSaga")
        saga.add_step(SagaStep("step1", lambda ctx: "done1"))
        res = saga.execute()
        self.assertEqual(res.status, SagaStatus.COMPLETED)


if __name__ == "__main__":
    unittest.main()
