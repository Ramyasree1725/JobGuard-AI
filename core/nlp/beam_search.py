"""
Aetheris NLP & Cognitive Engine: Beam Search & Nucleus Decoding
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Sequence, Optional
from core.nlp.transformer_blocks import ResearchTransformerLM


class TextGenerator:
    """Autoregressive text sampler supporting Greedy, Temperature, Top-K, and Nucleus Top-P."""
    def __init__(self, model: ResearchTransformerLM, seed: Optional[int] = None) -> None:
        self.model = model
        self.rng = random.Random(seed)

    def sample_next_token(
        self,
        logits: List[float],
        temperature: float = 0.8,
        top_k: int = 50,
        top_p: float = 0.9
    ) -> int:
        if temperature <= 0.05:
            # Greedy argmax
            return max(range(len(logits)), key=lambda idx: logits[idx])

        # Scale logits by temperature
        scaled = [v / max(0.01, temperature) for v in logits]
        max_val = max(scaled)
        probs = [math.exp(v - max_val) for v in scaled]
        sum_p = sum(probs)
        probs = [p / sum_p for p in probs]

        # Top-K filtering
        sorted_indices = sorted(range(len(probs)), key=lambda idx: probs[idx], reverse=True)
        if top_k > 0 and len(sorted_indices) > top_k:
            sorted_indices = sorted_indices[:top_k]

        # Top-P (Nucleus) filtering
        cum_prob = 0.0
        nucleus_indices: List[int] = []
        for idx in sorted_indices:
            nucleus_indices.append(idx)
            cum_prob += probs[idx]
            if cum_prob >= top_p:
                break

        # Renormalize nucleus probs
        nucleus_probs = [probs[idx] for idx in nucleus_indices]
        sum_n = sum(nucleus_probs)
        nucleus_probs = [p / sum_n for p in nucleus_probs]

        # Sample from discrete distribution
        r = self.rng.random()
        acc = 0.0
        for idx, p in zip(nucleus_indices, nucleus_probs):
            acc += p
            if r <= acc:
                return idx
        return nucleus_indices[-1]

    def generate(
        self,
        prompt_ids: Sequence[int],
        max_new_tokens: int = 20,
        temperature: float = 0.8,
        top_k: int = 50,
        top_p: float = 0.9,
        eos_token_id: Optional[int] = None
    ) -> List[int]:
        tokens = list(prompt_ids)
        for _ in range(max_new_tokens):
            logits = self.model.forward(tokens)
            next_logits = logits[-1]
            next_token = self.sample_next_token(next_logits, temperature, top_k, top_p)
            tokens.append(next_token)
            if eos_token_id is not None and next_token == eos_token_id:
                break
        return tokens
