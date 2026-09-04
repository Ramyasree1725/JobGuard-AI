"""
Aetheris Server Engine: Vision, NLP, Knowledge Graph & Recommendation Routes
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from fastapi import APIRouter
from server.models import TextGenerationRequest, KnowledgeQueryRequest, RecommendationRequest, ConsensusStateRequest
from core.math.vectors import Vector3D
from core.vision.voxel_grid import VoxelGrid3D
from core.vision.point_cloud import PointCloud3D
from core.nlp.bpe_tokenizer import BPETokenizer
from core.nlp.transformer_blocks import ResearchTransformerLM
from core.nlp.beam_search import TextGenerator
from core.knowledge.graph_store import KnowledgeGraphStore
from core.knowledge.symbolic_query import SymbolicReasoner
from core.recommendation.linucb_bandit import LinUCBContextualBandit
from core.recommendation.two_tower import TwoTowerDenseRetriever
from core.distributed.merkle_dag import MerkleDAGAccumulator
from server.storage.db_engine import db

# Singletons for interactive API testing
vision_router = APIRouter(prefix="/api/vision", tags=["Vision & Spatial"])
nlp_router = APIRouter(prefix="/api/nlp", tags=["NLP & Transformer"])
kg_router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Graph"])
rec_router = APIRouter(prefix="/api/recommendation", tags=["Recommendation & Bandits"])
consensus_router = APIRouter(prefix="/api/consensus", tags=["Consensus & Verification"])

# Knowledge Graph initialization
kg_store = KnowledgeGraphStore()
kg_store.add_fact("AutonomousDrone", "is_a", "RoboticSystem")
kg_store.add_fact("AutonomousDrone", "has_sensor", "LiDAR3D")
kg_store.add_fact("AutonomousDrone", "has_sensor", "IMU6Axis")
kg_store.add_fact("RoboticArm", "is_a", "RoboticSystem")
kg_store.add_fact("RoboticArm", "has_subsystem", "InverseKinematicsSolver")
kg_store.add_fact("InverseKinematicsSolver", "uses_algorithm", "DampedLeastSquares")
kg_store.add_fact("RRTStarPlanner", "uses_algorithm", "AsymptoticOptimalSampling")
kg_reasoner = SymbolicReasoner(kg_store)

# Bandits & Retrievers
bandit_engine = LinUCBContextualBandit(num_arms=5, feature_dim=4, alpha=1.2)
two_tower_retriever = TwoTowerDenseRetriever(user_dim=4, item_dim=4, embedding_dim=16)

# Merkle-DAG Accumulator
dag_accumulator = MerkleDAGAccumulator()

# NLP Model
tokenizer = BPETokenizer(vocab_size=200)
tokenizer.train([
    "autonomous multi-agent robotics and kinematics optimization engine",
    "neural symbolic reasoning and knowledge graph query executor",
    "distributed state verification and merkle consensus ledger"
])
transformer_model = ResearchTransformerLM(vocab_size=len(tokenizer.vocab), d_model=32, num_layers=2, num_heads=2)
text_generator = TextGenerator(transformer_model)


# --- Vision Endpoints ---
@vision_router.get("/voxel-grid")
async def get_voxel_occupancy():
    grid = VoxelGrid3D(bounds_min=Vector3D(-5, -5, 0), bounds_max=Vector3D(5, 5, 5), voxel_size=0.5)
    # Insert sample shapes
    for x in range(-3, 4):
        grid.insert_point(Vector3D(x * 0.5, 0.0, 1.0))
        grid.insert_point(Vector3D(0.0, x * 0.5, 2.0))
    return {
        "dimensions": [grid.dim_x, grid.dim_y, grid.dim_z],
        "occupied_count": len(grid.occupied_voxels),
        "occupied_centers": [c.to_list() for c in grid.get_occupied_centers()]
    }


# --- NLP Endpoints ---
@nlp_router.post("/generate")
async def generate_text(req: TextGenerationRequest):
    prompt_ids = tokenizer.encode(req.prompt)
    output_ids = text_generator.generate(
        prompt_ids,
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p
    )
    generated_text = tokenizer.decode(output_ids)
    return {
        "prompt": req.prompt,
        "token_count": len(output_ids),
        "token_ids": output_ids,
        "generated_text": generated_text
    }


# --- Knowledge Graph Endpoints ---
@kg_router.get("/graph")
async def get_knowledge_graph():
    return kg_store.to_dict()


@kg_router.get("/reason-paths")
async def get_reasoning_paths(start: str = "AutonomousDrone", end: str = "DampedLeastSquares"):
    paths = kg_reasoner.find_paths_dfs(start, end, max_depth=4)
    return {"start": start, "end": end, "paths_found": paths}


# --- Recommendation Endpoints ---
@rec_router.post("/bandit/pull")
async def pull_bandit_arm(req: RecommendationRequest):
    chosen_arm = bandit_engine.select_arm(req.user_features)
    # Simulate reward
    reward = 1.0 if chosen_arm in [0, 2] else 0.2
    bandit_engine.update_reward(chosen_arm, req.user_features, reward)
    return {
        "selected_arm": chosen_arm,
        "simulated_reward": reward,
        "arms_state": [
            {"arm_id": a.arm_id, "pull_count": a.pull_count, "theta_norm": sum(abs(v) for v in a.theta_hat)}
            for a in bandit_engine.arms
        ]
    }


# --- Consensus Endpoints ---
@consensus_router.post("/append-state")
async def append_consensus_state(req: ConsensusStateRequest):
    import time
    node_hash = dag_accumulator.append_state(
        {"event": req.event_name, "telemetry": req.telemetry_summary},
        timestamp=time.time()
    )
    audit_proof = dag_accumulator.generate_audit_proof(node_hash)
    return {
        "status": "appended",
        "node_hash": node_hash,
        "frontier_tips": dag_accumulator.frontier_tips,
        "proof_lineage_length": len(audit_proof)
    }


@consensus_router.get("/verify-node/{node_hash}")
async def verify_consensus_node(node_hash: str):
    is_valid = dag_accumulator.verify_node_integrity(node_hash)
    return {"node_hash": node_hash, "is_valid": is_valid}
