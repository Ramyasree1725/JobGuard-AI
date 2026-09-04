"""
JobGuard Core NLP - Dependency Parsing & Relation Extraction
Extracts grammatical dependency arcs (nsubj, dobj, prep, pobj)
from legal clauses to detect conditional fee entrapment.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class DependencyArc:
    head_idx: int
    dependent_idx: int
    relation: str  # "nsubj", "dobj", "pobj", "prep", "amod"


@dataclass
class DependencyTree:
    tokens: List[str]
    arcs: List[DependencyArc]

    def get_object_of_verb(self, verb: str) -> List[str]:
        """Find direct objects governed by target verb."""
        verb_indices = [i for i, t in enumerate(self.tokens) if t.lower() == verb.lower()]
        objects = []
        for arc in self.arcs:
            if arc.head_idx in verb_indices and arc.relation in ("dobj", "pobj"):
                objects.append(self.tokens[arc.dependent_idx])
        return objects


class DependencyParser:
    """Heuristic rule-based dependency parser for legal contract sentences."""

    @staticmethod
    def parse_sentence(tokens: List[str], pos_tags: List[str]) -> DependencyTree:
        arcs: List[DependencyArc] = []
        root_idx = 0

        # Find first verb as root
        for i, tag in enumerate(pos_tags):
            if tag.startswith("V"):
                root_idx = i
                break

        for i, (tok, tag) in enumerate(zip(tokens, pos_tags)):
            if i == root_idx:
                continue
            if tag.startswith("N"):
                if i < root_idx:
                    arcs.append(DependencyArc(head_idx=root_idx, dependent_idx=i, relation="nsubj"))
                else:
                    arcs.append(DependencyArc(head_idx=root_idx, dependent_idx=i, relation="dobj"))
            elif tag == "P" or tag == "IN":
                arcs.append(DependencyArc(head_idx=root_idx, dependent_idx=i, relation="prep"))

        return DependencyTree(tokens=tokens, arcs=arcs)
