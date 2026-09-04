"""
JobGuard Core Vision - Document Layout & Geometric Structure Analyzer
Analyzes spatial bounding boxes, paragraph margins, header/footer symmetries,
and signature box placement to detect forged or templated employment offer letters.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def width(self) -> float:
        return max(0.0, self.x_max - self.x_min)

    @property
    def height(self) -> float:
        return max(0.0, self.y_max - self.y_min)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x_min + self.x_max) / 2.0, (self.y_min + self.y_max) / 2.0)


@dataclass
class DocumentBlock:
    block_id: str
    block_type: str  # 'HEADER', 'LOGO', 'BODY_PARAGRAPH', 'TABLE', 'SIGNATURE_LINE', 'FOOTER'
    box: BoundingBox
    confidence: float
    text_content: str


@dataclass
class LayoutForensicReport:
    total_blocks_analyzed: int
    is_standard_corporate_layout: bool
    margin_uniformity_score: float  # 0 to 100
    alignment_skew_degrees: float
    detected_layout_anomalies: List[str]
    layout_risk_score: float  # 0 to 100


class DocumentLayoutAnalyzer:
    """Analyzes geometric layout, block alignments, and white space distributions."""

    def __init__(self):
        pass

    def compute_margin_uniformity(self, blocks: List[DocumentBlock], page_width: float = 612.0) -> float:
        """Evaluates whether left margins of body paragraphs are uniformly aligned."""
        body_blocks = [b for b in blocks if b.block_type == "BODY_PARAGRAPH"]
        if len(body_blocks) < 2:
            return 95.0

        left_margins = [b.box.x_min for b in body_blocks]
        mean_left = sum(left_margins) / len(left_margins)
        variance = sum((x - mean_left) ** 2 for x in left_margins) / len(left_margins)
        std_dev = math.sqrt(variance)

        # Variance > 15 points indicates haphazard copy-pasting
        score = max(0.0, 100.0 - (std_dev * 4.0))
        return min(100.0, score)

    def detect_overlapping_blocks(self, blocks: List[DocumentBlock]) -> List[Tuple[str, str]]:
        """Finds abnormal overlapping text or graphic elements indicating digital splicing."""
        overlaps: List[Tuple[str, str]] = []
        n = len(blocks)
        for i in range(n):
            for j in range(i + 1, n):
                b1, b2 = blocks[i].box, blocks[j].box
                
                # Check bounding box intersection
                x_overlap = max(0.0, min(b1.x_max, b2.x_max) - max(b1.x_min, b2.x_min))
                y_overlap = max(0.0, min(b1.y_max, b2.y_max) - max(b1.y_min, b2.y_min))
                intersection = x_overlap * y_overlap

                if intersection > 10.0 and blocks[i].block_type != "BACKGROUND":
                    overlaps.append((blocks[i].block_id, blocks[j].block_id))

        return overlaps

    def analyze_document_layout(
        self,
        blocks: List[DocumentBlock],
        page_width: float = 612.0,
        page_height: float = 792.0
    ) -> LayoutForensicReport:
        """Runs geometric forensics on document block hierarchy."""
        anomalies: List[str] = []
        risk_score = 0.0

        # 1. Margin uniformity
        uniformity = self.compute_margin_uniformity(blocks, page_width)
        if uniformity < 60.0:
            anomalies.append(f"Inconsistent paragraph indentation (Uniformity: {uniformity:.1f}%). Suggests spliced text blocks.")
            risk_score += 25.0

        # 2. Overlapping element detection
        overlaps = self.detect_overlapping_blocks(blocks)
        if overlaps:
            anomalies.append(f"Detected {len(overlaps)} overlapping bounding boxes; possible digital watermark or signature overlay tampering.")
            risk_score += 35.0

        # 3. Logo and Header presence check
        has_header_or_logo = any(b.block_type in ("HEADER", "LOGO") for b in blocks)
        if not has_header_or_logo:
            anomalies.append("Missing formal corporate letterhead or brand header block.")
            risk_score += 20.0

        # 4. Signature line placement check
        sig_blocks = [b for b in blocks if b.block_type == "SIGNATURE_LINE"]
        if not sig_blocks:
            anomalies.append("No formal executive signature block or signatory title detected.")
            risk_score += 15.0
        else:
            for s in sig_blocks:
                # Signature too high on page
                if s.box.y_min < page_height * 0.3:
                    anomalies.append("Abnormal signature block placement in upper half of page.")
                    risk_score += 30.0

        # Calculate layout standard
        is_standard = (risk_score < 40.0)

        return LayoutForensicReport(
            total_blocks_analyzed=len(blocks),
            is_standard_corporate_layout=is_standard,
            margin_uniformity_score=uniformity,
            alignment_skew_degrees=0.0,
            detected_layout_anomalies=anomalies if anomalies else ["Document exhibits professional corporate typography and aligned geometry."],
            layout_risk_score=min(100.0, max(0.0, risk_score))
        )
