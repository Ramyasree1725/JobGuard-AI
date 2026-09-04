"""
Aetheris Knowledge Graph Engine: TransE and RotatE Embedding Models
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Dict, Sequence, Optional
from core.knowledge.graph_store import KnowledgeGraphStore


class TransEModel:
    """
    Translational Knowledge Graph Embeddings (TransE):
    Energy score: f_r(h, t) = - ||h + r - t||_{L1 or L2}
    """
    def __init__(self, num_entities: int, num_relations: int, embedding_dim: int = 50, margin: float = 1.0, seed: Optional[int] = None) -> None:
        self.num_e = num_entities
        self.num_r = num_relations
        self.dim = embedding_dim
        self.margin = margin
        self.rng = random.Random(seed)

        # Initialize entity and relation embeddings
        self.entity_embeddings = [
            self._normalize([self.rng.uniform(-0.1, 0.1) for _ in range(self.dim)])
            for _ in range(num_entities)
        ]
        self.relation_embeddings = [
            self._normalize([self.rng.uniform(-0.1, 0.1) for _ in range(self.dim)])
            for _ in range(num_relations)
        ]

    def _normalize(self, vec: List[float]) -> List[float]:
        norm = math.sqrt(sum(v * v for v in vec))
        if norm < 1e-9:
            return vec
        return [v / norm for v in vec]

    def score_triple(self, h_id: int, r_id: int, t_id: int, p_norm: int = 2) -> float:
        """Computes distance score: ||h + r - t||."""
        h = self.entity_embeddings[h_id]
        r = self.relation_embeddings[r_id]
        t = self.entity_embeddings[t_id]

        if p_norm == 1:
            return sum(abs(h[i] + r[i] - t[i]) for i in range(self.dim))
        return math.sqrt(sum((h[i] + r[i] - t[i]) ** 2 for i in range(self.dim)))

    def train_step_sgd(self, pos_triples: List[Tuple[int, int, int]], lr: float = 0.01) -> float:
        """One epoch of SGD with corrupt negative sampling and margin ranking loss."""
        total_loss = 0.0

        for h, r, t in pos_triples:
            # Corrupt head or tail
            if self.rng.random() < 0.5:
                neg_h = self.rng.randint(0, self.num_e - 1)
                neg_t = t
            else:
                neg_h = h
                neg_t = self.rng.randint(0, self.num_e - 1)

            d_pos = self.score_triple(h, r, t)
            d_neg = self.score_triple(neg_h, r, neg_t)

            loss = max(0.0, self.margin + d_pos - d_neg)
            total_loss += loss

            if loss > 0.0:
                # Gradient updates for positive triple: minimize d_pos
                for i in range(self.dim):
                    grad_pos = (self.entity_embeddings[h][i] + self.relation_embeddings[r][i] - self.entity_embeddings[t][i]) / max(1e-4, d_pos)
                    self.entity_embeddings[h][i] -= lr * grad_pos
                    self.relation_embeddings[r][i] -= lr * grad_pos
                    self.entity_embeddings[t][i] += lr * grad_pos

                    # Gradient updates for negative triple: maximize d_neg
                    grad_neg = (self.entity_embeddings[neg_h][i] + self.relation_embeddings[r][i] - self.entity_embeddings[neg_t][i]) / max(1e-4, d_neg)
                    self.entity_embeddings[neg_h][i] += lr * grad_neg
                    self.entity_embeddings[neg_t][i] -= lr * grad_neg

                # Re-normalize
                self.entity_embeddings[h] = self._normalize(self.entity_embeddings[h])
                self.entity_embeddings[t] = self._normalize(self.entity_embeddings[t])

        return total_loss / max(1, len(pos_triples))


class RotatEModel:
    """
    Complex Space Relational Rotation Embeddings (RotatE):
    Maps entities to complex vector space C^k and relations to rotations:
    t = h \circ r where r_i = exp(i * theta_{r, i})
    """
    def __init__(self, num_entities: int, num_relations: int, embedding_dim: int = 50, margin: float = 6.0, seed: Optional[int] = None) -> None:
        self.num_e = num_entities
        self.num_r = num_relations
        self.dim = embedding_dim
        self.margin = margin
        self.rng = random.Random(seed)

        # Entity complex embeddings (real and imag)
        self.entity_real = [[self.rng.uniform(-0.1, 0.1) for _ in range(self.dim)] for _ in range(num_entities)]
        self.entity_imag = [[self.rng.uniform(-0.1, 0.1) for _ in range(self.dim)] for _ in range(num_entities)]

        # Relation phase angles theta in [-pi, pi]
        self.relation_phase = [[self.rng.uniform(-math.pi, math.pi) for _ in range(self.dim)] for _ in range(num_relations)]

    def score_triple(self, h_id: int, r_id: int, t_id: int) -> float:
        """Computes distance in complex space: ||h \circ r - t||."""
        h_re = self.entity_real[h_id]
        h_im = self.entity_imag[h_id]
        t_re = self.entity_real[t_id]
        t_im = self.entity_imag[t_id]
        phase = self.relation_phase[r_id]

        total_dist_sq = 0.0
        for i in range(self.dim):
            cos_theta = math.cos(phase[i])
            sin_theta = math.sin(phase[i])
            # (h_re + i*h_im) * (cos + i*sin) = (h_re*cos - h_im*sin) + i*(h_re*sin + h_im*cos)
            rot_re = h_re[i] * cos_theta - h_im[i] * sin_theta
            rot_im = h_re[i] * sin_theta + h_im[i] * cos_theta

            diff_re = rot_re - t_re[i]
            diff_im = rot_im - t_im[i]
            total_dist_sq += diff_re * diff_re + diff_im * diff_im

        return math.sqrt(total_dist_sq)
