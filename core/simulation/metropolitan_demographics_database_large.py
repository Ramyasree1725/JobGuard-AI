"""
JobGuard Core Simulation - Metropolitan Demographics Large Database
Contains global tech hub demographics, cost-of-living indices, and salary baselines.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class MetroDemographicLargeItem:
    metro_code: str
    city_name: str
    country_code: str
    latitude: float
    longitude: float
    population_millions: float
    cost_of_living_index: float
    purchasing_power_parity_factor: float
    software_engineer_median_salary_usd: float
    data_scientist_median_salary_usd: float
    tech_workforce_count: int
    primary_language: str
    utc_offset_hours: float


def build_metro_large_catalog() -> Dict[str, MetroDemographicLargeItem]:
    catalog: Dict[str, MetroDemographicLargeItem] = {}
    
    # 1
    catalog["METRO-LG-0001"] = MetroDemographicLargeItem(
        metro_code="METRO-LG-0001",
        city_name="San Francisco Bay Area",
        country_code="US",
        latitude=37.7749,
        longitude=-122.4194,
        population_millions=4.7,
        cost_of_living_index=185.0,
        purchasing_power_parity_factor=1.0,
        software_engineer_median_salary_usd=175000.0,
        data_scientist_median_salary_usd=168000.0,
        tech_workforce_count=380000,
        primary_language="English",
        utc_offset_hours=-8.0
    )
    # 2
    catalog["METRO-LG-0002"] = MetroDemographicLargeItem(
        metro_code="METRO-LG-0002",
        city_name="Greater New York Area",
        country_code="US",
        latitude=40.7128,
        longitude=-74.0060,
        population_millions=19.8,
        cost_of_living_index=100.0,
        purchasing_power_parity_factor=1.0,
        software_engineer_median_salary_usd=155000.0,
        data_scientist_median_salary_usd=150000.0,
        tech_workforce_count=340000,
        primary_language="English",
        utc_offset_hours=-5.0
    )
    # 3
    catalog["METRO-LG-0003"] = MetroDemographicLargeItem(
        metro_code="METRO-LG-0003",
        city_name="Bengaluru Metropolitan Region",
        country_code="IN",
        latitude=12.9716,
        longitude=77.5946,
        population_millions=13.2,
        cost_of_living_index=28.5,
        purchasing_power_parity_factor=0.28,
        software_engineer_median_salary_usd=28000.0,
        data_scientist_median_salary_usd=30000.0,
        tech_workforce_count=1250000,
        primary_language="English / Kannada",
        utc_offset_hours=5.5
    )
    # 4
    catalog["METRO-LG-0004"] = MetroDemographicLargeItem(
        metro_code="METRO-LG-0004",
        city_name="Greater London Area",
        country_code="GB",
        latitude=51.5074,
        longitude=-0.1278,
        population_millions=9.5,
        cost_of_living_index=92.0,
        purchasing_power_parity_factor=0.85,
        software_engineer_median_salary_usd=98000.0,
        data_scientist_median_salary_usd=102000.0,
        tech_workforce_count=480000,
        primary_language="English",
        utc_offset_hours=0.0
    )
    # 5
    catalog["METRO-LG-0005"] = MetroDemographicLargeItem(
        metro_code="METRO-LG-0005",
        city_name="Berlin Metropolitan Region",
        country_code="DE",
        latitude=52.5200,
        longitude=13.4050,
        population_millions=3.8,
        cost_of_living_index=74.0,
        purchasing_power_parity_factor=0.80,
        software_engineer_median_salary_usd=85000.0,
        data_scientist_median_salary_usd=88000.0,
        tech_workforce_count=190000,
        primary_language="German / English",
        utc_offset_hours=1.0
    )

    return catalog


class MetroLargeManager:
    def __init__(self):
        self.catalog = build_metro_large_catalog()

    def get_by_code(self, code: str) -> Optional[MetroDemographicLargeItem]:
        return self.catalog.get(code)
