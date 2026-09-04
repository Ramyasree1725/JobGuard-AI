"""
JobGuard Core NLP - Linear-Chain Conditional Random Field (CRF) for NER
Extracts recruiter names, compensation ranges, and company entities using Viterbi decoding.
"""

import math
from typing import List, Dict, Tuple, Optional, Set


class LinearChainCRF:
    """Linear-chain CRF for sequence labeling with Viterbi decoding."""

    def __init__(self, states: List[str]):
        self.states = states
        self.num_states = len(states)
        self.state_to_idx = {s: i for i, s in enumerate(states)}
        
        # Transition matrix: transitions[i][j] is score of transitioning from state i to state j
        self.transitions = [[0.0] * self.num_states for _ in range(self.num_states)]
        self.start_transitions = [0.0] * self.num_states
        self.end_transitions = [0.0] * self.num_states

    def viterbi_decode(self, emission_scores: List[List[float]]) -> Tuple[List[str], float]:
        """Find optimal state sequence using dynamic programming Viterbi algorithm."""
        seq_len = len(emission_scores)
        if seq_len == 0:
            return [], 0.0

        # viterbi_table[t][s] = max score of path ending at state s at time t
        viterbi_table = [[-float("inf")] * self.num_states for _ in range(seq_len)]
        backpointers = [[0] * self.num_states for _ in range(seq_len)]

        # Initialize t = 0
        for s in range(self.num_states):
            viterbi_table[0][s] = self.start_transitions[s] + emission_scores[0][s]

        # Forward trellis recursion
        for t in range(1, seq_len):
            for s in range(self.num_states):
                best_prev = 0
                best_score = -float("inf")
                for prev_s in range(self.num_states):
                    score = viterbi_table[t - 1][prev_s] + self.transitions[prev_s][s] + emission_scores[t][s]
                    if score > best_score:
                        best_score = score
                        best_prev = prev_s
                viterbi_table[t][s] = best_score
                backpointers[t][s] = best_prev

        # End transitions
        best_last_state = 0
        best_total_score = -float("inf")
        for s in range(self.num_states):
            final_score = viterbi_table[-1][s] + self.end_transitions[s]
            if final_score > best_total_score:
                best_total_score = final_score
                best_last_state = s

        # Backtrack optimal path
        path = [best_last_state]
        for t in range(seq_len - 1, 0, -1):
            path.append(backpointers[t][path[-1]])
        path.reverse()

        return [self.states[idx] for idx in path], round(best_total_score, 4)
