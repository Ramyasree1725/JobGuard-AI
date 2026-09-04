"""
Aetheris Computer Vision & Spatial: 3D Kalman Filter Multi-Object Tracker
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Dict, Any, Optional, Tuple
from core.math.vectors import Vector3D


class KalmanTrack3D:
    """
    3D Constant-Velocity Kalman Filter Track:
    State x = [px, py, pz, vx, vy, vz]^T
    """
    def __init__(self, track_id: int, initial_pos: Vector3D, max_missed_frames: int = 5) -> None:
        self.track_id = track_id
        # State: px, py, pz, vx, vy, vz
        self.state = [initial_pos.x, initial_pos.y, initial_pos.z, 0.0, 0.0, 0.0]
        # Diagonal Covariance
        self.cov = [0.1, 0.1, 0.1, 1.0, 1.0, 1.0]
        self.hits = 1
        self.time_since_update = 0
        self.max_missed = max_missed_frames

    def predict(self, dt: float) -> Vector3D:
        """State transition: x_new = x + v * dt."""
        for i in range(3):
            self.state[i] += self.state[i + 3] * dt
            # Process noise inflation
            self.cov[i] += self.cov[i + 3] * (dt * dt) + 0.05
            self.cov[i + 3] += 0.1

        self.time_since_update += 1
        return Vector3D(self.state[0], self.state[1], self.state[2])

    def update(self, measurement: Vector3D, r_noise: float = 0.05) -> None:
        """Measurement update: z = [px, py, pz]."""
        meas = [measurement.x, measurement.y, measurement.z]
        for i in range(3):
            residual = meas[i] - self.state[i]
            s = self.cov[i] + r_noise
            k = self.cov[i] / s
            self.state[i] += k * residual
            self.state[i + 3] += (k * 0.5) * residual # Velocity coupling
            self.cov[i] = (1.0 - k) * self.cov[i]

        self.hits += 1
        self.time_since_update = 0

    @property
    def position(self) -> Vector3D:
        return Vector3D(self.state[0], self.state[1], self.state[2])

    @property
    def velocity(self) -> Vector3D:
        return Vector3D(self.state[3], self.state[4], self.state[5])


class MultiObjectTracker3D:
    """Multi-Target Tracking using greedy minimum distance data association."""
    def __init__(self, match_distance_threshold: float = 1.5) -> None:
        self.dist_threshold = match_distance_threshold
        self.tracks: List[KalmanTrack3D] = []
        self._next_id = 1

    def update(self, detections: List[Vector3D], dt: float = 0.016) -> List[KalmanTrack3D]:
        # 1. Predict existing tracks
        for t in self.tracks:
            t.predict(dt)

        # 2. Greedy association
        unmatched_dets = set(range(len(detections)))
        unmatched_tracks = set(range(len(self.tracks)))

        for t_idx, track in enumerate(self.tracks):
            best_det = None
            best_dist = self.dist_threshold
            for d_idx in list(unmatched_dets):
                dist = track.position.distance_to(detections[d_idx])
                if dist < best_dist:
                    best_dist = dist
                    best_det = d_idx

            if best_det is not None:
                track.update(detections[best_det])
                unmatched_dets.remove(best_det)
                unmatched_tracks.remove(t_idx)

        # 3. Create new tracks for unmatched detections
        for d_idx in unmatched_dets:
            new_track = KalmanTrack3D(self._next_id, detections[d_idx])
            self._next_id += 1
            self.tracks.append(new_track)

        # 4. Remove dead tracks
        self.tracks = [t for t in self.tracks if t.time_since_update <= t.max_missed]
        return self.tracks
