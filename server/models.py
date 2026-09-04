"""
Aetheris Server Engine: Data Models & API Payload Schemas
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ArmReachRequest(BaseModel):
    x: float = Field(..., description="Target X coordinate in meters")
    y: float = Field(..., description="Target Y coordinate in meters")
    z: float = Field(..., description="Target Z coordinate in meters")


class DroneTrajectoryRequest(BaseModel):
    start_x: float = 0.0
    start_y: float = 0.0
    start_z: float = 0.5
    goal_x: float = 8.0
    goal_y: float = 8.0
    goal_z: float = 4.0


class OptimizationRunRequest(BaseModel):
    algorithm: str = Field("nsga2", description="Optimization algorithm: 'nsga2', 'bayesian', 'pso', 'symbolic'")
    num_iterations: int = Field(20, ge=1, le=500)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TextGenerationRequest(BaseModel):
    prompt: str = Field("autonomous robotic research prototype", description="Input prompt string")
    max_tokens: int = Field(25, ge=1, le=200)
    temperature: float = Field(0.8, ge=0.01, le=2.0)
    top_p: float = Field(0.9, ge=0.1, le=1.0)


class KnowledgeQueryRequest(BaseModel):
    head: Optional[str] = None
    relation: Optional[str] = None
    tail: Optional[str] = None


class RecommendationRequest(BaseModel):
    user_features: List[float] = Field(default_factory=lambda: [0.5, 0.2, 0.8, 0.1])
    top_k: int = 5


class ConsensusStateRequest(BaseModel):
    event_name: str
    telemetry_summary: Dict[str, Any]
