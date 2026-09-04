"""
JobGuard Core Simulation - Global City Economic Demographics & Tech Employment Data
Contains 300 detailed metropolitan node records, localized purchasing power parities (PPP),
median tech salaries, talent pool counts, and pairwise geospatial distances.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class GlobalMetropolitanProfile:
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


class CityEconomicDemographicsCatalog:
    """Master repository containing 300 global city economic profiles."""

    def __init__(self):
        self.cities: Dict[str, GlobalMetropolitanProfile] = {}
        self._country_index: Dict[str, List[str]] = {}
        self._populate_all_cities()

    def register(self, city: GlobalMetropolitanProfile) -> None:
        self.cities[city.metro_code] = city
        c = city.country_code.upper()
        if c not in self._country_index:
            self._country_index[c] = []
        self._country_index[c].append(city.metro_code)

    def _populate_all_cities(self) -> None:
        """Populate 300 metropolitan economic demographic records."""
        base_cities = [
            GlobalMetropolitanProfile("METRO-US-SFO", "San Francisco-Oakland-San Jose", "US", 37.7749, -122.4194, 4.7, 185.0, 1.00, 175000.0, 168000.0, 380000, "English", -8.0),
            GlobalMetropolitanProfile("METRO-US-NYC", "New York-Newark-Jersey City", "US", 40.7128, -74.0060, 19.8, 100.0, 1.00, 155000.0, 150000.0, 340000, "English", -5.0),
            GlobalMetropolitanProfile("METRO-US-SEA", "Seattle-Tacoma-Bellevue", "US", 47.6062, -122.3321, 4.0, 118.0, 1.00, 162000.0, 158000.0, 220000, "English", -8.0),
            GlobalMetropolitanProfile("METRO-US-AUS", "Austin-Round Rock-Georgetown", "US", 30.2672, -97.7431, 2.3, 78.0, 1.00, 142000.0, 138000.0, 140000, "English", -6.0),
            GlobalMetropolitanProfile("METRO-IN-BLR", "Bengaluru Urban Metropolitan", "IN", 12.9716, 77.5946, 13.2, 28.5, 0.28, 28000.0, 30000.0, 1250000, "English / Kannada", 5.5),
            GlobalMetropolitanProfile("METRO-IN-HYD", "Hyderabad Metropolitan Region", "IN", 17.3850, 78.4867, 10.5, 26.0, 0.28, 24000.0, 26000.0, 850000, "English / Telugu", 5.5),
            GlobalMetropolitanProfile("METRO-IN-PUN", "Pune Metropolitan Region", "IN", 18.5204, 73.8567, 7.4, 25.5, 0.28, 22000.0, 24000.0, 550000, "English / Marathi", 5.5),
            GlobalMetropolitanProfile("METRO-GB-LON", "Greater London Area", "GB", 51.5074, -0.1278, 9.5, 92.0, 0.85, 98000.0, 102000.0, 480000, "English", 0.0),
            GlobalMetropolitanProfile("METRO-DE-BER", "Berlin Metropolitan Region", "DE", 52.5200, 13.4050, 3.8, 74.0, 0.80, 85000.0, 88000.0, 190000, "German / English", 1.0),
            GlobalMetropolitanProfile("METRO-SG-SIN", "Singapore Central Region", "SG", 1.3521, 103.8198, 5.9, 98.0, 0.72, 92000.0, 95000.0, 150000, "English / Mandarin", 8.0)
        ]

        for bc in base_cities:
            self.register(bc)

        # Generate remaining 290 metropolitan demographic profiles
        country_list = ["US", "GB", "IN", "DE", "FR", "CA", "AU", "SG", "IE", "NL", "SE", "CH", "JP", "NZ", "IL"]
        for i in range(11, 301):
            c_iso = country_list[i % len(country_list)]
            mcode = f"METRO-{c_iso}-{i:04d}"
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

            self.register(GlobalMetropolitanProfile(
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

    def get_metro(self, metro_code: str) -> Optional[GlobalMetropolitanProfile]:
        return self.cities.get(metro_code.strip().upper())
