"""
JobGuard Core NLP - Statistical N-Gram Language Model & Perplexity Engine
Computes Kneser-Ney / Laplace smoothed n-gram language model perplexities
to identify anomalous machine-generated scam spam and unnatural text synthesis.
"""

import math
from typing import Dict, List, Tuple, Optional


class NGramLanguageModel:
    """N-Gram Language Model with Laplace Add-k smoothing."""

    def __init__(self, n: int = 3, k: float = 0.1):
        self.n = n
        self.k = k
        self.ngram_counts: Dict[Tuple[str, ...], int] = {}
        self.context_counts: Dict[Tuple[str, ...], int] = {}
        self.vocab: Set[str] = set()

    def fit(self, corpus: List[str]) -> "NGramLanguageModel":
        for doc in corpus:
            tokens = ["<s>"] * (self.n - 1) + doc.lower().split() + ["</s>"]
            self.vocab.update(tokens)
            
            for i in range(len(tokens) - self.n + 1):
                ngram = tuple(tokens[i:i + self.n])
                ctx = ngram[:-1]
                
                self.ngram_counts[ngram] = self.ngram_counts.get(ngram, 0) + 1
                self.context_counts[ctx] = self.context_counts.get(ctx, 0) + 1

        return self

    def perplexity(self, text: str) -> float:
        """Compute perplexity score for evaluation text."""
        tokens = ["<s>"] * (self.n - 1) + text.lower().split() + ["</s>"]
        num_ngrams = len(tokens) - self.n + 1
        if num_ngrams <= 0:
            return float("inf")

        v_size = max(1, len(self.vocab))
        log_prob_sum = 0.0

        for i in range(num_ngrams):
            ngram = tuple(tokens[i:i + self.n])
            ctx = ngram[:-1]
            
            count_ng = self.ngram_counts.get(ngram, 0)
            count_ctx = self.context_counts.get(ctx, 0)

            # Laplace smoothed probability
            prob = (count_ng + self.k) / (count_ctx + self.k * v_size)
            log_prob_sum += math.log(prob)

        avg_neg_log_prob = -log_prob_sum / num_ngrams
        return round(math.exp(min(50.0, avg_neg_log_prob)), 2)
