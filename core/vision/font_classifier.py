"""
JobGuard Core Vision - Typography & Font Consistency Classifier
Detects font substitutions, inconsistent kerning, and amateur editing artifacts in offer letters.
"""

from typing import List, Dict, Any, Tuple


class FontConsistencyAuditor:
    """Audits typography hierarchy and flags amateur font mixing."""

    STANDARD_CORPORATE_FONTS = {"Arial", "Calibri", "Helvetica", "Times New Roman", "Garamond", "Georgia", "Roboto"}
    SUSPICIOUS_FONTS = {"Comic Sans MS", "Papyrus", "Impact", "Curlz MT", "Brush Script MT"}

    @classmethod
    def audit_font_hierarchy(cls, observed_fonts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Examines list of observed font runs in document."""
        font_names = set(f.get("font_name", "") for f in observed_fonts)
        anomalies = []
        risk_penalty = 0.0

        for f in font_names:
            if f in cls.SUSPICIOUS_FONTS:
                risk_penalty += 35.0
                anomalies.append(f"Inappropriate casual/decorative typeface used in formal legal offer: '{f}'")

        if len(font_names) > 5:
            risk_penalty += 25.0
            anomalies.append(f"Excessive font variety ({len(font_names)} distinct typefaces detected in single document)")

        return {
            "is_consistent": len(anomalies) == 0,
            "distinct_font_count": len(font_names),
            "risk_penalty": min(100.0, risk_penalty),
            "anomalies": anomalies
        }
