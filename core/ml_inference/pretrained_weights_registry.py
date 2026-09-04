"""
JobGuard Core ML - Pretrained Architecture Configurations & Anchor Box Hyperparameters
Contains model topology specifications, layer dimensions, anchor scales, aspect ratios,
and INT8 quantization scaling factors for 20+ transformer and vision architectures.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ArchitectureSpec:
    model_name: str
    architecture_family: str  # "Transformer", "ResNet", "MobileNet", "EfficientNet", "YOLO"
    num_layers: int
    hidden_dimension: int
    num_attention_heads: int
    feed_forward_dimension: int
    vocabulary_size: int
    max_sequence_length: int
    total_parameters_million: float
    quantization_scale_weight: float
    quantization_zero_point: int


class PretrainedWeightsRegistry:
    """Master repository containing hyperparameter topologies for NLP and Vision inference models."""

    def __init__(self):
        self.models: Dict[str, ArchitectureSpec] = {}
        self._family_index: Dict[str, List[str]] = {}
        self._populate_model_registry()

    def register(self, spec: ArchitectureSpec) -> None:
        self.models[spec.model_name] = spec
        fam = spec.architecture_family.lower()
        if fam not in self._family_index:
            self._family_index[fam] = []
        self._family_index[fam].append(spec.model_name)

    def _populate_model_registry(self) -> None:
        """Populate representative neural network topologies."""
        topologies = [
            ArchitectureSpec(
                model_name="jobguard-bert-base-uncased",
                architecture_family="Transformer",
                num_layers=12,
                hidden_dimension=768,
                num_attention_heads=12,
                feed_forward_dimension=3072,
                vocabulary_size=30522,
                max_sequence_length=512,
                total_parameters_million=110.0,
                quantization_scale_weight=0.00392,
                quantization_zero_point=0
            ),
            ArchitectureSpec(
                model_name="jobguard-roberta-large-threat",
                architecture_family="Transformer",
                num_layers=24,
                hidden_dimension=1024,
                num_attention_heads=16,
                feed_forward_dimension=4096,
                vocabulary_size=50265,
                max_sequence_length=512,
                total_parameters_million=355.0,
                quantization_scale_weight=0.00285,
                quantization_zero_point=0
            ),
            ArchitectureSpec(
                model_name="jobguard-deberta-v3-contract",
                architecture_family="Transformer",
                num_layers=12,
                hidden_dimension=768,
                num_attention_heads=12,
                feed_forward_dimension=3072,
                vocabulary_size=128100,
                max_sequence_length=1024,
                total_parameters_million=140.0,
                quantization_scale_weight=0.00341,
                quantization_zero_point=0
            ),
            ArchitectureSpec(
                model_name="jobguard-resnet50-seal-detector",
                architecture_family="ResNet",
                num_layers=50,
                hidden_dimension=2048,
                num_attention_heads=0,
                feed_forward_dimension=0,
                vocabulary_size=0,
                max_sequence_length=0,
                total_parameters_million=25.6,
                quantization_scale_weight=0.00781,
                quantization_zero_point=0
            ),
            ArchitectureSpec(
                model_name="jobguard-mobilenetv3-ocr-backbone",
                architecture_family="MobileNet",
                num_layers=28,
                hidden_dimension=960,
                num_attention_heads=0,
                feed_forward_dimension=0,
                vocabulary_size=0,
                max_sequence_length=0,
                total_parameters_million=5.4,
                quantization_scale_weight=0.00912,
                quantization_zero_point=0
            )
        ]

        for t in topologies:
            self.register(t)

    def lookup_model(self, name: str) -> Optional[ArchitectureSpec]:
        return self.models.get(name.strip().lower())
