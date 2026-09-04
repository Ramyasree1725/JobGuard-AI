export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface RigidBodyState {
  name: string;
  position: [number, number, number];
  velocity: [number, number, number];
  orientation_quat: [number, number, number, number];
  euler_degrees: [number, number, number];
  angular_velocity: [number, number, number];
  speed: number;
}

export interface RoboticArmState {
  name: string;
  num_joints: number;
  joint_positions: number[];
  joint_limits: [number, number][];
  joint_names: string[];
  end_effector_position: [number, number, number];
  link_frames: [number, number, number][];
}

export interface SwarmAgentState {
  id: number;
  position: [number, number, number];
  velocity: [number, number, number];
  speed: number;
}

export interface TelemetryFrame {
  tick: number;
  sim_time: number;
  rigid_body: RigidBodyState;
  arm: RoboticArmState;
  swarm_count: number;
  swarm_center: [number, number, number];
  swarm_sample: SwarmAgentState[];
  imu: {
    accel: [number, number, number];
    gyro: [number, number, number];
  };
  point_cloud_sample: [number, number, number][];
  environment: {
    bounds: { min: number[]; max: number[] };
    target: number[];
    spheres: { name: string; center: number[]; radius: number }[];
    boxes: { name: string; min: number[]; max: number[] }[];
  };
}

export interface ParetoSolution {
  genes: number[];
  objectives: [number, number];
}

export interface OptimizationResult {
  experiment_id: string;
  algorithm: string;
  history: any[];
  pareto_front?: ParetoSolution[];
  discovered_formula?: string;
  best_score?: number;
}
