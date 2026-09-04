"""
JobGuard Core Vision - Typography Glyph Metrics & Kerning Pair Forensics Table
Contains standard font bounding box metrics, ascender/descender ratios, and kerning offset tables
for detecting font tampering and inconsistent letterhead typesetting in fraudulent PDFs.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class GlyphMetricEntry:
    character: str
    advance_width_em: float
    left_side_bearing_em: float
    right_side_bearing_em: float
    glyph_bounding_box: Tuple[float, float, float, float]  # (xMin, yMin, xMax, yMax)


@dataclass
class FontMetricsProfile:
    font_family_name: str
    is_serif: bool
    units_per_em: int
    ascender_units: int
    descender_units: int
    line_gap_units: int
    glyph_metrics: Dict[str, GlyphMetricEntry] = field(default_factory=dict)
    kerning_pairs: Dict[Tuple[str, str], float] = field(default_factory=dict)


class GlyphFontMetricsTable:
    """Master repository containing font typography baselines for PDF layout forensics."""

    def __init__(self):
        self.font_profiles: Dict[str, FontMetricsProfile] = {}
        self._populate_font_profiles()

    def register(self, profile: FontMetricsProfile) -> None:
        self.font_profiles[profile.font_family_name.lower()] = profile

    def _populate_font_profiles(self) -> None:
        """Populate typography metrics for standard enterprise business fonts."""
        # 1. Arial Profile
        arial = FontMetricsProfile(
            font_family_name="Arial",
            is_serif=False,
            units_per_em=2048,
            ascender_units=1854,
            descender_units=-434,
            line_gap_units=67
        )
        # Sample characters
        chars = [
            ("A", 0.667, 0.010, 0.010, (0.0, 0.0, 0.65, 0.72)),
            ("B", 0.667, 0.080, 0.040, (0.08, 0.0, 0.62, 0.72)),
            ("C", 0.722, 0.060, 0.040, (0.06, -0.01, 0.68, 0.73)),
            ("D", 0.722, 0.080, 0.040, (0.08, 0.0, 0.68, 0.72)),
            ("E", 0.667, 0.080, 0.050, (0.08, 0.0, 0.61, 0.72)),
            ("a", 0.556, 0.050, 0.040, (0.05, -0.01, 0.51, 0.53)),
            ("b", 0.611, 0.080, 0.040, (0.08, -0.01, 0.57, 0.72)),
            ("c", 0.500, 0.050, 0.040, (0.05, -0.01, 0.46, 0.53)),
            ("d", 0.611, 0.050, 0.040, (0.05, -0.01, 0.57, 0.72)),
            ("e", 0.556, 0.050, 0.040, (0.05, -0.01, 0.51, 0.53))
        ]
        for c, adv, lsb, rsb, bbox in chars:
            arial.glyph_metrics[c] = GlyphMetricEntry(c, adv, lsb, rsb, bbox)

        arial.kerning_pairs[("A", "V")] = -0.074
        arial.kerning_pairs[("T", "o")] = -0.055
        arial.kerning_pairs[("W", "a")] = -0.037

        self.register(arial)

        # 2. Times New Roman Profile
        tnr = FontMetricsProfile(
            font_family_name="Times New Roman",
            is_serif=True,
            units_per_em=2048,
            ascender_units=1825,
            descender_units=-443,
            line_gap_units=87
        )
        self.register(tnr)

    def verify_typesetting_consistency(self, font_name: str, char_pairs: List[Tuple[str, str, float]]) -> Tuple[bool, float]:
        """Verify observed inter-character spacing against canonical kerning table."""
        profile = self.font_profiles.get(font_name.lower())
        if not profile or not profile.kerning_pairs:
            return True, 0.0

        anomalies = 0
        for c1, c2, observed_spacing in char_pairs:
            expected_kerning = profile.kerning_pairs.get((c1, c2), 0.0)
            if abs(observed_spacing - expected_kerning) > 0.08:
                anomalies += 1

        anomaly_rate = anomalies / max(1, len(char_pairs))
        return anomaly_rate < 0.2, round(anomaly_rate * 100.0, 1)
