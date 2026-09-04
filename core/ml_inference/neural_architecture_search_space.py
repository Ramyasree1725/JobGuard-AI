"""
JobGuard Core ML - Neural Architecture Search (NAS) Search Space & Supernet Graph
Defines candidate macro-architectures, inverted bottleneck building blocks,
kernel sizes, expansion factors, and Pareto-optimal latency/accuracy estimators for on-device inference.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class NASBlockCandidate:
    block_id: str
    block_type: str  # "MBConv3", "MBConv6", "FusedMBConv", "TransformerBlock", "ConvNeXtBlock"
    kernel_size: int
    expansion_ratio: int
    se_ratio: float
    stride: int
    in_channels: int
    out_channels: int
    flops_millions: float
    param_count_thousands: float


@dataclass
class CandidateArchitectureModel:
    arch_id: str
    blocks: List[NASBlockCandidate]
    total_flops_m: float
    total_params_k: float
    estimated_inference_latency_ms: float
    accuracy_proxy_score: float


class NASSearchSpace:
    """Master repository containing supernet candidate blocks and evaluated subnets."""

    def __init__(self):
        self.candidate_blocks: Dict[str, NASBlockCandidate] = {}
        self.evaluated_subnets: Dict[str, CandidateArchitectureModel] = {}
        self._populate_search_space()

    def _populate_search_space(self) -> None:
        """Populate 200 block configurations and 50 evaluated subnets."""
        kernel_choices = [3, 5, 7]
        expansion_choices = [1, 3, 6]
        channel_choices = [16, 24, 32, 48, 64, 96, 128, 160, 256, 512]

        block_count = 0
        for k in kernel_choices:
            for exp in expansion_choices:
                for c_idx in range(len(channel_choices) - 1):
                    block_count += 1
                    b_id = f"BLOCK-MB-{block_count:04d}"
                    in_c = channel_choices[c_idx]
                    out_c = channel_choices[c_idx + 1]
                    flops = (in_c * out_c * k * k * exp) / 10000.0
                    params = (in_c * out_c * k * exp) / 1000.0

                    self.candidate_blocks[b_id] = NASBlockCandidate(
                        block_id=b_id,
                        block_type=f"MBConv{exp}",
                        kernel_size=k,
                        expansion_ratio=exp,
                        se_ratio=0.25,
                        stride=1 if c_idx % 2 == 0 else 2,
                        in_channels=in_c,
                        out_channels=out_c,
                        flops_millions=round(flops, 2),
                        param_count_thousands=round(params, 2)
                    )

        # Build evaluated subnets
        for s_idx in range(1, 101):
            s_id = f"SUBNET-ARCH-{s_idx:04d}"
            # Sample 6 blocks
            block_keys = list(self.candidate_blocks.keys())[s_idx:s_idx + 6]
            selected_blocks = [self.candidate_blocks[k] for k in block_keys if k in self.candidate_blocks]

            total_fl = sum(b.flops_millions for b in selected_blocks)
            total_par = sum(b.param_count_thousands for b in selected_blocks)
            lat = round(total_fl * 0.15 + 1.2, 2)
            acc = round(80.0 + (total_fl / 50.0) * 8.0, 2)

            self.evaluated_subnets[s_id] = CandidateArchitectureModel(
                arch_id=s_id,
                blocks=selected_blocks,
                total_flops_m=round(total_fl, 2),
                total_params_k=round(total_par, 2),
                estimated_inference_latency_ms=lat,
                accuracy_proxy_score=min(96.5, acc)
            )

    def find_pareto_optimal_subnets(self, max_latency_ms: float = 5.0) -> List[CandidateArchitectureModel]:
        """Filters subnets meeting latency budget and ranks by accuracy."""
        feasible = [s for s in self.evaluated_subnets.values() if s.estimated_inference_latency_ms <= max_latency_ms]
        feasible.sort(key=lambda s: s.accuracy_proxy_score, reverse=True)
        return feasible
