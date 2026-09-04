"""
JobGuard Core Recommendation - Content-Based Profile & Skill Matcher
Builds candidate skill graphs, computes BM25 relevance scores,
and matches verified job openings to candidate background summaries.
"""

import math
from typing import List, Dict, Set, Tuple, Optional


class BM25Ranker:
    """Okapi BM25 ranking algorithm for job description retrieval."""

    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.doc_lens = [len(doc.split()) for doc in corpus]
        self.avg_doc_len = sum(self.doc_lens) / max(1, self.corpus_size)

        self.doc_freqs: Dict[str, int] = {}
        self.doc_tfs: List[Dict[str, int]] = []

        for doc in corpus:
            tf: Dict[str, int] = {}
            for word in doc.lower().split():
                tf[word] = tf.get(word, 0) + 1
            self.doc_tfs.append(tf)
            for word in set(tf.keys()):
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1

    def score(self, query: str) -> List[Tuple[int, float]]:
        """Scores all documents against search query."""
        scores = []
        q_words = query.lower().split()

        for doc_idx, tf in enumerate(self.doc_tfs):
            doc_len = self.doc_lens[doc_idx]
            doc_score = 0.0

            for word in q_words:
                if word in tf:
                    df = self.doc_freqs.get(word, 0)
                    idf = math.log((self.corpus_size - df + 0.5) / (df + 0.5) + 1.0)
                    freq = tf[word]
                    numerator = freq * (self.k1 + 1.0)
                    denominator = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                    doc_score += idf * (numerator / denominator)

            scores.append((doc_idx, round(doc_score, 4)))

        scores.sort(key=lambda s: s[1], reverse=True)
        return scores
