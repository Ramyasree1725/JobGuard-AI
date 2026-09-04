"""
JobGuard Core ML - TF-IDF Vectorizer & Text Feature Extraction Pipeline
Tokenizes, computes term frequency-inverse document frequencies, n-grams,
and statistical text complexity features for scam classification.
"""

import math
import re
from typing import List, Dict, Set, Optional, Tuple, Any
from .tensor_engine import Tensor


class TFIDFVectorizer:
    """Pure-Python TF-IDF Vectorizer with n-gram support and L2 normalization."""

    def __init__(self, max_features: int = 1000, ngram_range: Tuple[int, int] = (1, 2), min_df: int = 1):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.vocabulary: Dict[str, int] = {}
        self.idf_weights: List[float] = []
        self._doc_count = 0

    def _tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        words = cleaned.split()
        tokens = []
        
        min_n, max_n = self.ngram_range
        for n in range(min_n, max_n + 1):
            for i in range(len(words) - n + 1):
                tokens.append(" ".join(words[i:i + n]))
                
        return tokens

    def fit(self, documents: List[str]) -> "TFIDFVectorizer":
        """Compute vocabulary and IDF values from training corpus."""
        self._doc_count = len(documents)
        df_counts: Dict[str, int] = {}

        for doc in documents:
            tokens = set(self._tokenize(doc))
            for t in tokens:
                df_counts[t] = df_counts.get(t, 0) + 1

        # Filter by min_df and sort by document frequency
        valid_terms = [t for t, count in df_counts.items() if count >= self.min_df]
        valid_terms.sort(key=lambda t: df_counts[t], reverse=True)
        
        top_terms = valid_terms[:self.max_features]
        self.vocabulary = {term: idx for idx, term in enumerate(top_terms)}
        
        # Smooth IDF: ln((1 + N) / (1 + df)) + 1
        self.idf_weights = [
            math.log((1.0 + self._doc_count) / (1.0 + df_counts[term])) + 1.0
            for term in top_terms
        ]
        return self

    def transform(self, documents: List[str]) -> Tensor:
        """Transform text documents into normalized TF-IDF feature matrix."""
        if not self.vocabulary:
            raise ValueError("Vectorizer must be fitted before calling transform()")

        num_docs = len(documents)
        num_feats = len(self.vocabulary)
        matrix_data = [0.0] * (num_docs * num_feats)

        for doc_idx, doc in enumerate(documents):
            tokens = self._tokenize(doc)
            tf: Dict[str, int] = {}
            for t in tokens:
                if t in self.vocabulary:
                    tf[t] = tf.get(t, 0) + 1

            doc_len = max(1, len(tokens))
            row_sum_sq = 0.0

            # Compute TF * IDF
            for term, count in tf.items():
                col_idx = self.vocabulary[term]
                tf_val = count / doc_len
                tfidf = tf_val * self.idf_weights[col_idx]
                matrix_data[doc_idx * num_feats + col_idx] = tfidf
                row_sum_sq += tfidf ** 2

            # L2 Normalization
            norm = math.sqrt(row_sum_sq) if row_sum_sq > 0 else 1.0
            for col_idx in range(num_feats):
                matrix_data[doc_idx * num_feats + col_idx] /= norm

        return Tensor(matrix_data, shape=(num_docs, num_feats))


class TextFeatureExtractor:
    """Extracts dense statistical and lexical features from recruitment texts."""

    @staticmethod
    def extract_features(text: str) -> Dict[str, float]:
        char_count = len(text)
        words = text.split()
        word_count = max(1, len(words))
        
        uppercase_chars = sum(1 for c in text if c.isupper())
        digits = sum(1 for c in text if c.isdigit())
        exclamation_marks = text.count("!")
        question_marks = text.count("?")
        dollar_signs = text.count("$") + text.count("₹") + text.count("€")

        avg_word_length = sum(len(w) for w in words) / word_count
        all_caps_words = sum(1 for w in words if len(w) > 1 and w.isupper())

        return {
            "char_count": float(char_count),
            "word_count": float(word_count),
            "uppercase_ratio": round(uppercase_chars / max(1, char_count), 4),
            "digit_ratio": round(digits / max(1, char_count), 4),
            "exclamation_count": float(exclamation_marks),
            "question_count": float(question_marks),
            "currency_symbol_count": float(dollar_signs),
            "avg_word_length": round(avg_word_length, 2),
            "all_caps_word_ratio": round(all_caps_words / word_count, 4)
        }


class ScalerNormalizer:
    """Standard z-score scaler for dense numerical features."""

    def __init__(self):
        self.means: List[float] = []
        self.stds: List[float] = []

    def fit(self, data_rows: List[List[float]]) -> "ScalerNormalizer":
        if not data_rows:
            return self
        num_cols = len(data_rows[0])
        num_rows = len(data_rows)

        self.means = [0.0] * num_cols
        self.stds = [1.0] * num_cols

        for col in range(num_cols):
            vals = [row[col] for row in data_rows]
            m = sum(vals) / num_rows
            var = sum((v - m) ** 2 for v in vals) / max(1, num_rows - 1)
            self.means[col] = m
            self.stds[col] = max(1e-8, math.sqrt(var))

        return self

    def transform(self, data_rows: List[List[float]]) -> List[List[float]]:
        out = []
        for row in data_rows:
            norm_row = [(val - m) / s for val, m, s in zip(row, self.means, self.stds)]
            out.append(norm_row)
        return out
