"""
Aetheris Robotics & Simulation: Synthetic Sensors (LiDAR, 6-Axis IMU, Depth Scanner)
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Dict, Any, Optional, Sequence
from core.math.vectors import Vector3D
from core.math.quaternions import Quaternion
from core.math.geometry import Ray3D, Sphere3D, AABB3D


class SyntheticLiDAR3D:
    """
    360-degree 3D Synthetic LiDAR Scanner with angular beam discretization,
    range noise, dropouts, and point cloud emission.
    """
    def __init__(
        self,
        num_horizontal_beams: int = 64,
        num_vertical_channels: int = 16,
        fov_vertical_deg: Tuple[float, float] = (-15.0, 15.0),
        max_range: float = 30.0,
        noise_std_dev: float = 0.02,
        seed: Optional[int] = None
    ) -> None:
        self.num_h = num_horizontal_beams
        self.num_v = num_vertical_channels
        self.fov_v_min = math.radians(fov_vertical_deg[0])
        self.fov_v_max = math.radians(fov_vertical_deg[1])
        self.max_range = float(max_range)
        self.noise_sigma = float(noise_std_dev)
        self.rng = random.Random(seed)

    def scan(
        self,
        sensor_position: Vector3D,
        sensor_orientation: Quaternion,
        spheres: Sequence[Sphere3D],
        aabbs: Sequence[AABB3D]
    ) -> List[Vector3D]:
        """Performs full 3D LiDAR sweep scan and returns detected 3D point cloud."""
        point_cloud: List[Vector3D] = []

        for v_idx in range(self.num_v):
            pitch = self.fov_v_min + (self.fov_v_max - self.fov_v_min) * (v_idx / max(1, self.num_v - 1))
            cos_p = math.cos(pitch)
            sin_p = math.sin(pitch)

            for h_idx in range(self.num_h):
                yaw = (2.0 * math.pi * h_idx) / float(self.num_h)
                
                # Local beam direction
                local_dir = Vector3D(cos_p * math.cos(yaw), cos_p * math.sin(yaw), sin_p)
                world_dir = sensor_orientation.rotate_vector(local_dir).normalize()
                
                ray = Ray3D(sensor_position, world_dir)
                closest_t = self.max_range

                # Intersect spheres
                for sphere in spheres:
                    t = ray.intersect_sphere(sphere)
                    if t is not None and t < closest_t:
                        closest_t = t

                # Intersect AABBs
                for aabb in aabbs:
                    t = ray.intersect_aabb(aabb)
                    if t is not None and t < closest_t:
                        closest_t = t

                if closest_t < self.max_range:
                    # Add Gaussian range noise
                    noisy_dist = max(0.1, closest_t + self.rng.gauss(0.0, self.noise_sigma))
                    hit_point = sensor_position + world_dir * noisy_dist
                    point_cloud.append(hit_point)

        return point_cloud


class SyntheticIMU6Axis:
    """
    6-Axis Inertial Measurement Unit (IMU): 3-axis Accelerometer + 3-axis Gyroscope.
    Simulates real-world sensor bias, random walk drift, and white Gaussian noise.
    """
    def __init__(
        self,
        accel_noise_std: float = 0.05,
        gyro_noise_std: float = 0.005,
        gyro_bias_drift_rate: float = 1e-4,
        seed: Optional[int] = None
    ) -> None:
        self.accel_noise = float(accel_noise_std)
        self.gyro_noise = float(gyro_noise_std)
        self.bias_drift = float(gyro_bias_drift_rate)
        self.rng = random.Random(seed)

        self.gyro_bias = Vector3D(0.001, -0.002, 0.001)

    def read(
        self,
        true_acceleration_world: Vector3D,
        true_angular_vel_body: Vector3D,
        orientation: Quaternion,
        dt: float,
        gravity: float = 9.81
    ) -> Tuple[Vector3D, Vector3D]:
        """
        Returns (measured_accel_body, measured_gyro_body).
        Accelerometer measures specific force: a_meas = R^T * (a_world + [0, 0, g]) + noise
        """
        gravity_vec = Vector3D(0.0, 0.0, gravity)
        specific_force_world = true_acceleration_world + gravity_vec
        
        # Transform to body frame: q^-1 * f
        specific_force_body = orientation.inverse().rotate_vector(specific_force_world)
        
        accel_measured = Vector3D(
            specific_force_body.x + self.rng.gauss(0.0, self.accel_noise),
            specific_force_body.y + self.rng.gauss(0.0, self.accel_noise),
            specific_force_body.z + self.rng.gauss(0.0, self.accel_noise)
        )

        # Update gyro bias random walk
        self.gyro_bias = Vector3D(
            self.gyro_bias.x + self.rng.gauss(0.0, self.bias_drift * math.sqrt(dt)),
            self.gyro_bias.y + self.rng.gauss(0.0, self.bias_drift * math.sqrt(dt)),
            self.gyro_bias.z + self.rng.gauss(0.0, self.bias_drift * math.sqrt(dt))
        )

        gyro_measured = Vector3D(
            true_angular_vel_body.x + self.gyro_bias.x + self.rng.gauss(0.0, self.gyro_noise),
            true_angular_vel_body.y + self.gyro_bias.y + self.rng.gauss(0.0, self.gyro_noise),
            true_angular_vel_body.z + self.gyro_bias.z + self.rng.gauss(0.0, self.gyro_noise)
        )

        return accel_measured, gyro_measured
