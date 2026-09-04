"""
JobGuard Core Simulation - Global Tech Hub Geospatial Network & Cost-of-Living Graph
Simulates geographic talent migration flows, regional salary adjustment coefficients,
and international remote hiring density matrices across 20+ major metropolitan tech centers.
"""

import math
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TechCityNode:
    city_id: str
    city_name: str
    country_code: str
    latitude: float
    longitude: float
    cost_of_living_index: float  # NYC = 100.0 baseline
    tech_talent_pool_density: int
    median_software_salary_usd: float
    time_zone_utc_offset: float


class GlobalTechCityNetwork:
    """Geospatial network modeling cross-border recruitment and compensation calibration."""

    def __init__(self):
        self.cities: Dict[str, TechCityNode] = {}
        self._populate_cities()

    def register(self, node: TechCityNode) -> None:
        self.cities[node.city_id] = node

    def _populate_cities(self) -> None:
        """Populate global metropolitan tech hubs."""
        hubs = [
            TechCityNode("CITY-SF", "San Francisco / Silicon Valley", "US", 37.7749, -122.4194, 185.0, 350000, 165000.0, -8.0),
            TechCityNode("CITY-NYC", "New York City", "US", 40.7128, -74.0060, 100.0, 320000, 150000.0, -5.0),
            TechCityNode("CITY-SEA", "Seattle", "US", 47.6062, -122.3321, 115.0, 210000, 155000.0, -8.0),
            TechCityNode("CITY-BLR", "Bengaluru", "IN", 12.9716, 77.5946, 28.5, 1200000, 28000.0, 5.5),
            TechCityNode("CITY-HYD", "Hyderabad", "IN", 17.3850, 78.4867, 26.0, 850000, 24000.0, 5.5),
            TechCityNode("CITY-LON", "London", "GB", 51.5074, -0.1278, 92.0, 450000, 95000.0, 0.0),
            TechCityNode("CITY-BER", "Berlin", "DE", 52.5200, 13.4050, 74.0, 180000, 82000.0, 1.0),
            TechCityNode("CITY-SIN", "Singapore", "SG", 1.3521, 103.8198, 98.0, 140000, 90000.0, 8.0),
            TechCityNode("CITY-TOR", "Toronto", "CA", 43.6532, -79.3832, 78.0, 280000, 88000.0, -5.0),
            TechCityNode("CITY-SYD", "Sydney", "AU", -33.8688, 151.2093, 89.0, 190000, 95000.0, 10.0)
        ]

        for h in hubs:
            self.register(h)

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Great-circle distance between two geographical points in kilometers."""
        r = 6371.0  # Earth radius in km
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        return round(r * c, 2)
