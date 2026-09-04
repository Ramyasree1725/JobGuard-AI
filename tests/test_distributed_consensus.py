"""
Unit Tests: Aetheris Distributed Merkle-DAG & Raft Consensus
"""
import pytest
from core.distributed.merkle_dag import MerkleDAGAccumulator, MerkleDAGNode
from core.distributed.raft_fsm import RaftNodeFSM


def test_merkle_dag_integrity():
    dag = MerkleDAGAccumulator()
    h1 = dag.append_state({"action": "STEP_1"}, timestamp=1.0)
    h2 = dag.append_state({"action": "STEP_2"}, timestamp=2.0)
    
    assert dag.verify_node_integrity(h1) is True
    assert dag.verify_node_integrity(h2) is True
    
    proof = dag.generate_audit_proof(h2)
    assert len(proof) >= 2


def test_raft_node_state_transitions():
    node = RaftNodeFSM("node-1", ["node-2", "node-3"])
    assert node.state == RaftNodeFSM.FOLLOWER
    # Trigger election
    vote_req = node._start_election()
    assert node.state == RaftNodeFSM.CANDIDATE
    assert vote_req["term"] == 1
