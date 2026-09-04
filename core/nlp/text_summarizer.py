"""
JobGuard Core NLP - Extractive Text Summarization (TextRank & LexRank)
Graph-based sentence ranking algorithm using sentence cosine similarity and PageRank.
"""

import math
from typing import List, Dict, Tuple, Set


class TextRankSummarizer:
    """Extractive summarization using TextRank graph ranking on sentence embeddings."""

    @staticmethod
    def _sentence_similarity(s1: str, s2: str) -> float:
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        if not words1 or not words2:
            return 0.0
        overlap = len(words1.intersection(words2))
        return overlap / (math.log(len(words1) + 1) + math.log(len(words2) + 1))

    @classmethod
    def summarize(cls, text: str, num_sentences: int = 3) -> List[str]:
        """Extract top N representative sentences from text."""
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 10]
        n = len(sentences)
        if n <= num_sentences:
            return sentences

        # Build similarity matrix
        sim_matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                score = cls._sentence_similarity(sentences[i], sentences[j])
                sim_matrix[i][j] = score
                sim_matrix[j][i] = score

        # PageRank power iteration
        pr = [1.0 / n] * n
        d = 0.85

        for _ in range(30):
            next_pr = [(1.0 - d) / n] * n
            for i in range(n):
                sum_w = sum(sim_matrix[i])
                if sum_w > 0:
                    for j in range(n):
                        next_pr[j] += d * pr[i] * (sim_matrix[i][j] / sum_w)
            pr = next_pr

        # Rank sentences
        ranked_indices = sorted(range(n), key=lambda idx: pr[idx], reverse=True)
        top_indices = sorted(ranked_indices[:num_sentences])

        return [sentences[idx] for idx in top_indices]
