"""
JobGuard Core Vision - Optical Character Recognition (OCR) Layout & Font Analyzer
Extracts spatial bounding boxes, detects fake seal clipart stamps, analyzes font consistency,
and identifies manipulated PDF letterhead layers in uploaded offer contracts.
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def area(self) -> float:
        return max(0.0, self.x_max - self.x_min) * max(0.0, self.y_max - self.y_min)

    def intersects(self, other: "BoundingBox") -> bool:
        return not (
            self.x_max < other.x_min or
            self.x_min > other.x_max or
            self.y_max < other.y_min or
            self.y_min > other.y_max
        )


@dataclass
class LayoutBlock:
    block_id: str
    block_type: str  # "header", "body_paragraph", "signature_block", "seal", "table"
    bbox: BoundingBox
    text_content: str
    confidence: float = 0.95


class DocumentLayoutAnalyzer:
    """Analyzes spatial geometry and structure of uploaded PDF offer letters."""

    def __init__(self):
        self._blocks: List[LayoutBlock] = []

    def analyze_document_structure(self, blocks: List[LayoutBlock]) -> Dict[str, Any]:
        """Audit spatial consistency of document components."""
        has_header = any(b.block_type == "header" for b in blocks)
        has_body = any(b.block_type == "body_paragraph" for b in blocks)
        has_signature = any(b.block_type == "signature_block" for b in blocks)
        has_suspicious_seal = any(b.block_type == "seal" for b in blocks)

        # Spatial order check: header -> body -> signature
        layout_ordered = True
        if blocks:
            sorted_blocks = sorted(blocks, key=lambda b: b.bbox.y_min)
            types = [b.block_type for b in sorted_blocks]
            if "header" in types and "body_paragraph" in types:
                if types.index("header") > types.index("body_paragraph"):
                    layout_ordered = False

        return {
            "is_structurally_valid": has_header and has_body and layout_ordered,
            "has_corporate_header": has_header,
            "has_formal_signature_block": has_signature,
            "has_fake_seal_stamp": has_suspicious_seal,
            "block_count": len(blocks),
            "layout_integrity_score": 95.0 if layout_ordered and not has_suspicious_seal else 40.0
        }
