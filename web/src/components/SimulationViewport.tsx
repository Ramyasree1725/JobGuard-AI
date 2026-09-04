import React, { useRef, useEffect } from 'react';
import { TelemetryFrame } from '../types';
import { apiClient } from '../services/api';

interface SimulationViewportProps {
  telemetry: TelemetryFrame | null;
}

export const SimulationViewport: React.FC<SimulationViewportProps> = ({ telemetry }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !telemetry) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const cx = width / 2;
    const cy = height / 2;
    const scale = 18; // pixels per meter

    // Clear viewport
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, width, height);

    // Draw Grid
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    const gridSize = 2 * scale;
    for (let x = 0; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Draw Obstacle Spheres
    if (telemetry.environment && telemetry.environment.spheres) {
      telemetry.environment.spheres.forEach((s) => {
        const sx = cx + s.center[0] * scale;
        const sy = cy - s.center[1] * scale;
        const sr = s.radius * scale;

        ctx.fillStyle = 'rgba(239, 68, 68, 0.2)';
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(sx, sy, sr, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
      });
    }

    // Draw LiDAR point cloud
    if (telemetry.point_cloud_sample) {
      ctx.fillStyle = '#38bdf8';
      telemetry.point_cloud_sample.forEach((pt) => {
        const px = cx + pt[0] * scale;
        const py = cy - pt[1] * scale;
        ctx.fillRect(px - 1.5, py - 1.5, 3, 3);
      });
    }

    // Draw Swarm Agents
    if (telemetry.swarm_sample) {
      ctx.fillStyle = '#10b981';
      telemetry.swarm_sample.forEach((agent) => {
        const ax = cx + agent.position[0] * scale;
        const ay = cy - agent.position[1] * scale;
        ctx.beginPath();
        ctx.arc(ax, ay, 3.5, 0, 2 * Math.PI);
        ctx.fill();
      });
    }

    // Draw Robotic Arm Kinematics Chain
    if (telemetry.arm && telemetry.arm.link_frames) {
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 3;
      ctx.beginPath();
      telemetry.arm.link_frames.forEach((frame, idx) => {
        const fx = cx + frame[0] * scale;
        const fy = cy - frame[1] * scale;
        if (idx === 0) ctx.moveTo(fx, fy);
        else ctx.lineTo(fx, fy);
      });
      ctx.stroke();

      // Joint Nodes
      ctx.fillStyle = '#fbbf24';
      telemetry.arm.link_frames.forEach((frame) => {
        const fx = cx + frame[0] * scale;
        const fy = cy - frame[1] * scale;
        ctx.beginPath();
        ctx.arc(fx, fy, 4.5, 0, 2 * Math.PI);
        ctx.fill();
      });
    }

    // Draw 6-DoF Drone
    if (telemetry.rigid_body) {
      const dx = cx + telemetry.rigid_body.position[0] * scale;
      const dy = cy - telemetry.rigid_body.position[1] * scale;

      ctx.fillStyle = '#06b6d4';
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(dx, dy, 7, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();

      // Velocity Vector Line
      const vx = telemetry.rigid_body.velocity[0] * scale * 0.8;
      const vy = -telemetry.rigid_body.velocity[1] * scale * 0.8;
      ctx.strokeStyle = '#06b6d4';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(dx, dy);
      ctx.lineTo(dx + vx, dy + vy);
      ctx.stroke();
    }
  }, [telemetry]);

  const handleArmReach = (x: number, y: number, z: number) => {
    apiClient.commandArmReach(x, y, z);
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      <div className="px-4 py-2.5 bg-slate-800/60 border-b border-slate-700/60 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            Real-Time 3D Physics Viewport (Canvas / WebGL Orthographic)
          </h2>
        </div>
        <div className="flex items-center space-x-4 text-xs font-mono text-slate-400">
          <span>Tick: {telemetry?.tick ?? 0}</span>
          <span>SimTime: {telemetry?.sim_time.toFixed(2) ?? '0.00'}s</span>
          <span>Swarm: {telemetry?.swarm_count ?? 0}</span>
        </div>
      </div>

      <div className="relative flex-1 min-h-[420px] bg-slate-950 flex items-center justify-center">
        <canvas
          ref={canvasRef}
          width={760}
          height={480}
          className="w-full h-full object-contain cursor-crosshair"
        />
        <div className="absolute bottom-3 left-3 bg-slate-900/80 backdrop-blur-md p-2 rounded-lg border border-slate-800 text-[11px] font-mono text-slate-300 flex gap-3">
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-cyan-400"></span> Drone (6-DoF)</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-400"></span> 6-DoF Arm</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-400"></span> Swarm Agents</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-red-400"></span> Obstacles</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-sky-400"></span> LiDAR Scans</span>
        </div>
      </div>

      <div className="p-3 bg-slate-900/90 border-t border-slate-800 flex items-center justify-between text-xs">
        <span className="text-slate-400 font-medium">Kinematics Interactive Targets:</span>
        <div className="flex gap-2">
          <button
            onClick={() => handleArmReach(0.4, 0.2, 0.3)}
            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-mono"
          >
            IK Reach Target 1
          </button>
          <button
            onClick={() => handleArmReach(-0.3, 0.4, 0.2)}
            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-mono"
          >
            IK Reach Target 2
          </button>
        </div>
      </div>
    </div>
  );
};
