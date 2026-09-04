"""
Aetheris Server Engine: Persistent Storage & Experiment History Catalog
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import sqlite3
import json
import time
from typing import List, Dict, Any, Optional
from server.config import config


class ExperimentDatabase:
    """
    SQLite-backed Experiment Logging, Checkpointing, and Telemetry Archival Engine.
    """
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path if db_path is not None else config.DATABASE_PATH
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT UNIQUE NOT NULL,
                    algorithm TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    status TEXT NOT NULL,
                    metrics_json TEXT,
                    checkpoint_json TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consensus_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    block_hash TEXT UNIQUE NOT NULL,
                    timestamp REAL NOT NULL,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
            """)
            conn.commit()

    def record_experiment(self, exp_id: str, algorithm: str, status: str = "RUNNING", metrics: Optional[Dict[str, Any]] = None) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO experiments (experiment_id, algorithm, created_at, status, metrics_json)
                VALUES (?, ?, ?, ?, ?)
            """, (exp_id, algorithm, time.time(), status, json.dumps(metrics or {})))
            conn.commit()

    def list_experiments(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM experiments ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "experiment_id": r["experiment_id"],
                    "algorithm": r["algorithm"],
                    "created_at": r["created_at"],
                    "status": r["status"],
                    "metrics": json.loads(r["metrics_json"] or "{}")
                }
                for r in rows
            ]


db = ExperimentDatabase()
