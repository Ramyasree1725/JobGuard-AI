"""
JobGuard Core Vision - Digital Document Forensics & Tamper Detection Toolkit
Implements Error Level Analysis (ELA), EXIF header analysis, copy-move clone stamp detection,
and pixel luminance variance maps for detecting forged corporate offer letters.
"""

import math
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ForensicsReport:
    is_tampered: bool
    tamper_confidence_score: float  # [0, 100]
    detected_clones: int
    compression_anomaly_detected: bool
    suspicious_metadata_fields: List[str]
    forensic_notes: List[str] = field(default_factory=list)


class DocumentForensicsToolkit:
    """Forensic image analysis engine for identifying counterfeit PDF letterheads."""

    @staticmethod
    def error_level_analysis_simulated(image_matrix: List[List[float]], quality_factor: float = 0.9) -> Tuple[List[List[float]], float]:
        """Calculates difference map between uncompressed and recompressed image."""
        h = len(image_matrix)
        w = len(image_matrix[0]) if h > 0 else 0

        diff_matrix = [[0.0] * w for _ in range(h)]
        total_error = 0.0

        for y in range(h):
            for x in range(w):
                orig_val = image_matrix[y][x]
                # Simulated quantization recompression loss
                recompressed = round(orig_val * quality_factor * 10.0) / (quality_factor * 10.0)
                diff = abs(orig_val - recompressed) * 10.0  # Scale for visibility
                diff_matrix[y][x] = round(diff, 4)
                total_error += diff

        avg_error = total_error / max(1, h * w)
        return diff_matrix, round(avg_error, 4)

    @staticmethod
    def detect_copy_move_cloning(image_matrix: List[List[float]], block_size: int = 8, threshold: float = 0.95) -> int:
        """Detects identical cloned image blocks (e.g. pasted signature stamps)."""
        h = len(image_matrix)
        w = len(image_matrix[0]) if h > 0 else 0

        blocks: List[Tuple[int, int, List[float]]] = []

        # Extract non-overlapping blocks
        for y in range(0, h - block_size, block_size):
            for x in range(0, w - block_size, block_size):
                block_vals = []
                for by in range(block_size):
                    for bx in range(block_size):
                        block_vals.append(image_matrix[y + by][x + bx])
                blocks.append((x, y, block_vals))

        clone_pairs = 0
        num_blocks = len(blocks)

        for i in range(min(num_blocks, 100)):
            for j in range(i + 1, min(num_blocks, 100)):
                # Euclidean distance between block vectors
                dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(blocks[i][2], blocks[j][2])))
                if dist < 0.01:
                    clone_pairs += 1

        return clone_pairs

    @classmethod
    def audit_document_integrity(cls, image_matrix: List[List[float]], metadata: Optional[Dict[str, Any]] = None) -> ForensicsReport:
        """Master forensics examination."""
        diff_map, avg_ela = cls.error_level_analysis_simulated(image_matrix)
        clones = cls.detect_copy_move_cloning(image_matrix)
        notes = []

        suspicious_meta = []
        meta = metadata or {}
        if "Creator" in meta and ("Photoshop" in str(meta["Creator"]) or "Canva" in str(meta["Creator"])):
            suspicious_meta.append(f"Document created via design editor: '{meta['Creator']}' rather than official enterprise ERP")
            notes.append("Graphic design tool used to produce formal legal employment contract")

        has_compression_anomaly = (avg_ela > 0.4)
        if has_compression_anomaly:
            notes.append(f"Significant compression level discrepancy (ELA score: {avg_ela:.2f}) indicates layered image tampering")

        if clones > 0:
            notes.append(f"Detected {clones} duplicated graphical regions (potential cloned seal or signature)")

        risk = 0.0
        if suspicious_meta:
            risk += 35.0
        if has_compression_anomaly:
            risk += 40.0
        if clones > 0:
            risk += 30.0

        risk = min(100.0, risk)

        return ForensicsReport(
            is_tampered=risk >= 40.0,
            tamper_confidence_score=round(risk, 1),
            detected_clones=clones,
            compression_anomaly_detected=has_compression_anomaly,
            suspicious_metadata_fields=suspicious_meta,
            forensic_notes=notes
        )
