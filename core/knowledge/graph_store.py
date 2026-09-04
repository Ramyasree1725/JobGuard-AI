"""
Aetheris Knowledge Graph Engine: Entity, Relation & Triple Storage Index
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import List, Dict, Set, Tuple, Optional, Any


class KnowledgeGraphStore:
    """
    Indexed Knowledge Graph storing multi-relational facts (head_entity, relation, tail_entity).
    Provides bidirectional adjacency lookup for rapid neighborhood retrieval and graph traversal.
    """
    def __init__(self) -> None:
        self.entity_to_id: Dict[str, int] = {}
        self.id_to_entity: Dict[int, str] = {}
        self.relation_to_id: Dict[str, int] = {}
        self.id_to_relation: Dict[int, str] = {}
        
        # Triples: (h_id, r_id, t_id)
        self.triples: List[Tuple[int, int, int]] = []
        
        # Adjacency indices
        self.head_relation_to_tails: Dict[Tuple[int, int], Set[int]] = {}
        self.tail_relation_to_heads: Dict[Tuple[int, int], Set[int]] = {}
        self.entity_neighbors: Dict[int, Set[Tuple[int, int]]] = {} # entity -> {(rel_id, target_id)}

    def get_or_add_entity(self, name: str) -> int:
        if name not in self.entity_to_id:
            idx = len(self.entity_to_id)
            self.entity_to_id[name] = idx
            self.id_to_entity[idx] = name
            self.entity_neighbors[idx] = set()
            return idx
        return self.entity_to_id[name]

    def get_or_add_relation(self, name: str) -> int:
        if name not in self.relation_to_id:
            idx = len(self.relation_to_id)
            self.relation_to_id[name] = idx
            self.id_to_relation[idx] = name
            return idx
        return self.relation_to_id[name]

    def add_fact(self, head: str, relation: str, tail: str) -> Tuple[int, int, int]:
        h_id = self.get_or_add_entity(head)
        r_id = self.get_or_add_relation(relation)
        t_id = self.get_or_add_entity(tail)

        triple = (h_id, r_id, t_id)
        self.triples.append(triple)

        hr_key = (h_id, r_id)
        if hr_key not in self.head_relation_to_tails:
            self.head_relation_to_tails[hr_key] = set()
        self.head_relation_to_tails[hr_key].add(t_id)

        tr_key = (t_id, r_id)
        if tr_key not in self.tail_relation_to_heads:
            self.tail_relation_to_heads[tr_key] = set()
        self.tail_relation_to_heads[tr_key].add(h_id)

        self.entity_neighbors[h_id].add((r_id, t_id))
        return triple

    def num_entities(self) -> int:
        return len(self.entity_to_id)

    def num_relations(self) -> int:
        return len(self.relation_to_id)

    def num_triples(self) -> int:
        return len(self.triples)

    def get_tails(self, head: str, relation: str) -> List[str]:
        if head not in self.entity_to_id or relation not in self.relation_to_id:
            return []
        h_id = self.entity_to_id[head]
        r_id = self.relation_to_id[relation]
        tail_ids = self.head_relation_to_tails.get((h_id, r_id), set())
        return [self.id_to_entity[tid] for tid in tail_ids]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_entities": self.num_entities(),
            "num_relations": self.num_relations(),
            "num_triples": self.num_triples(),
            "sample_triples": [
                {
                    "head": self.id_to_entity[h],
                    "relation": self.id_to_relation[r],
                    "tail": self.id_to_entity[t]
                }
                for (h, r, t) in self.triples[:20]
            ]
        }
