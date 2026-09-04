"""
JobGuard Core Simulation - Global Metropolitan Demographics Master Registry
Contains 450 metropolitan tech talent hub profiles, localized cost-of-living indices,
purchasing power parity factors, and salary distributions.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class MasterMetropolitanProfile:
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


class GlobalMetropolitanDemographicsMasterRegistry:
    """Master repository of 450 metropolitan economic demographic profiles."""

    def __init__(self):
        self.cities: Dict[str, MasterMetropolitanProfile] = {}
        self._populate_all_cities()

    def register(self, c: MasterMetropolitanProfile) -> None:
        self.cities[c.metro_code] = c

    def _populate_all_cities(self) -> None:
        """Populate 450 metropolitan profiles."""
        # Metro 1
        self.register(MasterMetropolitanProfile(
            metro_code="MST-METRO-001",
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
        ))

        # Metro 2
        self.register(MasterMetropolitanProfile(
            metro_code="MST-METRO-002",
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
        ))

        # Metro 3
        self.register(MasterMetropolitanProfile(
            metro_code="MST-METRO-003",
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
        ))

        # Generate Metros 4 through 450
        country_pool = ["US", "GB", "IN", "DE", "FR", "CA", "AU", "SG", "IE", "NL", "SE", "CH", "JP", "NZ", "IL"]
        for i in range(4, 451):
            c_iso = country_pool[i % len(country_pool)]
            mcode = f"MST-METRO-{i:04d}"
            name = f"Metropolitan Region {i:04d} ({c_iso})"
            lat = round(10.0 + (i % 60) * 0.8, 4)
            lon = round(-120.0 + (i % 180) * 1.2, 4)
            pop = round(1.0 + (i % 15) * 0.5, 1)
            coli = round(40.0 + (i % 80) * 1.5, 1)
            ppp = round(0.3 + (i % 10) * 0.07, 2)
            swe_sal = round(30000.0 + (i * 350), 0)
            ds_sal = round(swe_sal * 1.05, 0)
            workforce = 50000 + (i * 2000)
            offset = float((i % 24) - 11)

            self.register(MasterMetropolitanProfile(
                metro_code=mcode,
                city_name=name,
                country_code=c_iso,
                latitude=lat,
                longitude=lon,
                population_millions=pop,
                cost_of_living_index=coli,
                purchasing_power_parity_factor=ppp,
                software_engineer_median_salary_usd=swe_sal,
                data_scientist_median_salary_usd=ds_sal,
                tech_workforce_count=workforce,
                primary_language="English",
                utc_offset_hours=offset
            ))

    def get_metro(self, metro_code: str) -> Optional[MasterMetropolitanProfile]:
        return self.cities.get(metro_code.strip().upper())
