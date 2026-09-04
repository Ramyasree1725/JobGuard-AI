"""
Aetheris Server Engine: Configuration Settings & Environment Schema
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import os
from typing import List


class ServerConfig:
    """Master Application Configuration."""
    APP_NAME: str = "Aetheris Autonomous Research Platform"
    VERSION: str = "1.0.0"
    HOST: str = os.getenv("AETHERIS_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("AETHERIS_PORT", "8000"))
    DEBUG: bool = os.getenv("AETHERIS_DEBUG", "True").lower() == "true"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]
    
    SIMULATION_TICK_RATE_HZ: int = 60
    WEBSOCKET_BROADCAST_INTERVAL_SEC: float = 0.033 # ~30fps UI update
    DATABASE_PATH: str = os.getenv("AETHERIS_DB", "aetheris_research.db")
    STORAGE_DIR: str = os.getenv("AETHERIS_STORAGE", "./storage_data")


config = ServerConfig()
