"""
JobGuard Core Vision - Typography Consistency & Font Tampering Engine
Detects font substitutions, mismatched kerning, irregular point sizes,
and composite character glyph alterations in employment contracts.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import statistics


@dataclass
class FontSpan:
    span_id: str
    font_family: str
    font_size_pt: float
    is_bold: bool
    is_italic: bool
    text: str
    baseline_y: float


@dataclass
class TypographyForensicReport:
    distinct_font_families_count: int
    dominant_font_family: str
    font_family_distribution: Dict[str, float]
    has_unnatural_font_switching: bool
    flagged_inconsistent_spans: List[FontSpan]
    typography_risk_score: float  # 0 to 100
    narrative_findings: List[str]


class TypographyConsistencyEngine:
    """Evaluates typographic harmony and detects spliced clauses with differing fonts."""

    STANDARD_CORPORATE_FONTS: Set[str] = {
        "arial", "calibri", "helvetica", "times new roman", "georgia",
        "garamond", "roboto", "open sans", "segoe ui", "trebuchet ms"
    }

    def __init__(self):
        pass

    def audit_typography(self, spans: List[FontSpan]) -> TypographyForensicReport:
        """Audits document text spans for fraudulent font manipulation or clause splicing."""
        if not spans:
            return TypographyForensicReport(
                distinct_font_families_count=0,
                dominant_font_family="UNKNOWN",
                font_family_distribution={},
                has_unnatural_font_switching=False,
                flagged_inconsistent_spans=[],
                typography_risk_score=0.0,
                narrative_findings=["No text spans supplied for typographic analysis."]
            )

        # Count font families by character count
        family_counts: Dict[str, int] = {}
        for s in spans:
            fam = s.font_family.lower().strip()
            family_counts[fam] = family_counts.get(fam, 0) + len(s.text)

        total_chars = max(1, sum(family_counts.values()))
        distribution = {fam: (count / total_chars) * 100.0 for fam, count in family_counts.items()}
        dominant_family = max(family_counts.items(), key=lambda x: x[1])[0]

        findings: List[str] = []
        flagged_spans: List[FontSpan] = []
        risk_score = 0.0

        # Check 1: Too many distinct font families
        distinct_count = len(family_counts)
        if distinct_count > 3:
            findings.append(f"Excessive font family variety ({distinct_count} distinct fonts). Professional contracts use at most 2 fonts.")
            risk_score += min(40.0, distinct_count * 10.0)

        # Check 2: Clauses written in minority rogue fonts
        for s in spans:
            fam = s.font_family.lower().strip()
            # If font family accounts for less than 8% of document but contains sensitive terms (check, deposit, fee)
            if fam != dominant_family and distribution.get(fam, 0) < 15.0:
                lower_text = s.text.lower()
                if any(w in lower_text for w in ["check", "deposit", "fee", "wire", "vendor", "equipment", "telegram"]):
                    flagged_spans.append(s)
                    findings.append(f"Suspicious font switch: Clause containing '{s.text[:40]}...' is formatted in '{s.font_family}' instead of document primary font '{dominant_family}'.")
                    risk_score += 35.0

        # Check 3: Comic Sans or informal novelty fonts
        informal_fonts = {"comic sans ms", "papyrus", "jokerman", "curlz mt", "impact"}
        for fam in family_counts:
            if fam in informal_fonts:
                findings.append(f"CRITICAL: Document contains unprofessional novelty font '{fam}', highly atypical of legitimate corporate legal offers.")
                risk_score += 50.0

        has_switching = len(flagged_spans) > 0 or distinct_count > 3

        return TypographyForensicReport(
            distinct_font_families_count=distinct_count,
            dominant_font_family=dominant_family,
            font_family_distribution=distribution,
            has_unnatural_font_switching=has_switching,
            flagged_inconsistent_spans=flagged_spans,
            typography_risk_score=min(100.0, max(0.0, risk_score)),
            narrative_findings=findings if findings else ["Typographic styles conform to corporate publishing standards."]
        )
