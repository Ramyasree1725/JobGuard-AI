import React from 'react';
import { TelemetryFrame } from '../types';

interface TelemetryDashboardProps {
  telemetry: TelemetryFrame | null;
}

export const TelemetryDashboard: React.FC<TelemetryDashboardProps> = ({ telemetry }) => {
  if (!telemetry) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-center text-slate-400 font-mono text-xs">
        Awaiting telemetry connection...
      </div>
    );
  }

  const { rigid_body, arm, imu } = telemetry;

  return (
    <div className="space-y-4">
      {/* State Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Rigid Body 6-DoF */}
        <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="text-xs font-semibold uppercase text-cyan-400 font-mono">6-DoF Rigid Body</h3>
            <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-300 font-mono">
              v={rigid_body.speed.toFixed(2)} m/s
            </span>
          </div>
          <div className="mt-3 space-y-2 text-xs font-mono text-slate-300">
            <div className="flex justify-between">
              <span className="text-slate-500">Pos (X,Y,Z):</span>
              <span>[{rigid_body.position.map((v) => v.toFixed(2)).join(', ')}]</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Euler (Y,P,R):</span>
              <span>[{rigid_body.euler_degrees.map((v) => v.toFixed(1) + '°').join(', ')}]</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">AngVel (rad/s):</span>
              <span>[{rigid_body.angular_velocity.map((v) => v.toFixed(2)).join(', ')}]</span>
            </div>
          </div>
        </div>

        {/* 6-DoF Arm Manipulator */}
        <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="text-xs font-semibold uppercase text-amber-400 font-mono">Robotic Arm (6-DoF)</h3>
            <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 font-mono">
              6 Links
            </span>
          </div>
          <div className="mt-3 space-y-2 text-xs font-mono text-slate-300">
            <div className="flex justify-between">
              <span className="text-slate-500">End-Effector:</span>
              <span>[{arm.end_effector_position.map((v) => v.toFixed(2)).join(', ')}]</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Joints (q1..q6):</span>
              <span className="text-[11px]">[{arm.joint_positions.slice(0, 3).map((v) => v.toFixed(2)).join(', ')}...]</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Status:</span>
              <span className="text-emerald-400 font-semibold">Active IK Tracking</span>
            </div>
          </div>
        </div>

        {/* 6-Axis IMU Sensor */}
        <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="text-xs font-semibold uppercase text-purple-400 font-mono">6-Axis IMU Telemetry</h3>
            <span className="text-[10px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 font-mono">
              60 Hz Filtered
            </span>
          </div>
          <div className="mt-3 space-y-2 text-xs font-mono text-slate-300">
            <div className="flex justify-between">
              <span className="text-slate-500">Accel (m/s²):</span>
              <span>[{imu.accel.map((v) => v.toFixed(2)).join(', ')}]</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Gyro (rad/s):</span>
              <span>[{imu.gyro.map((v) => v.toFixed(3)).join(', ')}]</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">LiDAR Hits:</span>
              <span className="text-sky-400 font-semibold">{telemetry.point_cloud_sample.length} pts</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
