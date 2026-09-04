"""
JobGuard Core Vision - Sequence CTC Decoding & Deep OCR Recognition
Connectionist Temporal Classification (CTC) greedy and prefix beam search decoders
for transcribing text lines from feature sequences without pre-segmented characters.
"""

import math
from typing import List, Tuple, Dict, Set


class CTCDecoder:
    """Connectionist Temporal Classification (CTC) sequence decoder."""

    def __init__(self, vocab: List[str], blank_idx: int = 0):
        self.vocab = vocab
        self.blank = blank_idx

    def greedy_decode(self, probability_matrix: List[List[float]]) -> str:
        """Best-path greedy decoding: takes argmax at each time step and collapses duplicates."""
        raw_indices = [max(range(len(t_dist)), key=lambda idx: t_dist[idx]) for t_dist in probability_matrix]
        
        collapsed_indices: List[int] = []
        prev = -1

        for idx in raw_indices:
            if idx != prev:
                if idx != self.blank:
                    collapsed_indices.append(idx)
                prev = idx

        chars = [self.vocab[idx] for idx in collapsed_indices if idx < len(self.vocab)]
        return "".join(chars)

    def beam_search_decode(self, probability_matrix: List[List[float]], beam_width: int = 10) -> str:
        """Prefix Beam Search decoder accounting for probability mass over multiple alignments."""
        # Key: prefix string -> (prob_blank, prob_non_blank)
        beams: Dict[str, Tuple[float, float]] = {"": (1.0, 0.0)}

        for t_dist in probability_matrix:
            new_beams: Dict[str, Tuple[float, float]] = {}

            for prefix, (p_b, p_nb) in beams.items():
                p_total = p_b + p_nb

                # 1. Blank transition
                p_b_curr, p_nb_curr = new_beams.get(prefix, (0.0, 0.0))
                new_beams[prefix] = (p_b_curr + p_total * t_dist[self.blank], p_nb_curr)

                # 2. Character transitions
                for c_idx, char in enumerate(self.vocab):
                    if c_idx == self.blank:
                        continue

                    p_char = t_dist[c_idx]
                    new_prefix = prefix + char

                    p_b_new, p_nb_new = new_beams.get(new_prefix, (0.0, 0.0))

                    if prefix and prefix[-1] == char:
                        # Repeated char separated by blank vs same char
                        new_beams[new_prefix] = (p_b_new, p_nb_new + p_b * p_char)
                        new_beams[prefix] = (new_beams[prefix][0], new_beams[prefix][1] + p_nb * p_char)
                    else:
                        new_beams[new_prefix] = (p_b_new, p_nb_new + p_total * p_char)

            # Prune to top beam_width
            sorted_prefixes = sorted(
                new_beams.keys(),
                key=lambda pref: new_beams[pref][0] + new_beams[pref][1],
                reverse=True
            )
            beams = {pref: new_beams[pref] for pref in sorted_prefixes[:beam_width]}

        best_prefix = max(beams.keys(), key=lambda pref: beams[pref][0] + beams[pref][1])
        return best_prefix
