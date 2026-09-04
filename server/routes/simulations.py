"""
Aetheris Server Engine: Simulation Control REST Endpoints
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from core.math.vectors import Vector3D
from server.models import ArmReachRequest, DroneTrajectoryRequest
from server.workers.scheduler import sim_worker

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])


@router.get("/status")
async def get_simulation_status():
    """Returns current state and telemetry snapshot of the research simulation."""
    return {
        "is_running": sim_worker.is_running,
        "tick_count": sim_worker.sim_engine.tick_count,
        "sim_time": sim_worker.sim_engine.sim_time,
        "telemetry": sim_worker.sim_engine.get_latest_telemetry()
    }


@router.post("/start")
async def start_simulation():
    """Starts the real-time 60Hz physics and multi-agent simulation loop."""
    await sim_worker.start()
    return {"status": "started", "fps": sim_worker.sim_engine.fps}


@router.post("/stop")
async def stop_simulation():
    """Pauses the real-time simulation loop."""
    await sim_worker.stop()
    return {"status": "stopped"}


@router.post("/step")
async def step_single_tick():
    """Manually steps the simulation by 1 tick."""
    telemetry = sim_worker.sim_engine.step()
    return {"status": "stepped", "telemetry": telemetry}


@router.post("/arm/reach")
async def command_arm_reach(req: ArmReachRequest):
    """Calculates Inverse Kinematics and commands the 6-DoF robotic arm."""
    target = Vector3D(req.x, req.y, req.z)
    success, joint_angles = sim_worker.sim_engine.plan_arm_reach(target)
    return {
        "success": success,
        "target": target.to_list(),
        "joint_angles": joint_angles,
        "end_effector": sim_worker.sim_engine.arm.end_effector_position().to_list()
    }


@router.post("/drone/plan-trajectory")
async def plan_drone_trajectory(req: DroneTrajectoryRequest):
    """Plans an optimal collision-free RRT* trajectory for the 6-DoF drone."""
    start = Vector3D(req.start_x, req.start_y, req.start_z)
    goal = Vector3D(req.goal_x, req.goal_y, req.goal_z)
    success = sim_worker.sim_engine.plan_drone_trajectory(start, goal)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to find collision-free path with RRT*")
    return {
        "success": True,
        "duration": sim_worker.sim_engine.active_trajectory.total_duration if sim_worker.sim_engine.active_trajectory else 0.0,
        "start": start.to_list(),
        "goal": goal.to_list()
    }
