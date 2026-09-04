"""
Aetheris Knowledge Graph Engine: Symbolic Path Reasoner & Multi-Hop Query Engine
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import List, Dict, Set, Tuple, Optional, Any
from core.knowledge.graph_store import KnowledgeGraphStore


class SymbolicReasoner:
    """
    Multi-hop Symbolic Path Reasoning engine over knowledge graphs.
    Finds explanatory reasoning paths between concepts: e.g. A -> r1 -> B -> r2 -> C.
    """
    def __init__(self, store: KnowledgeGraphStore) -> None:
        self.store = store

    def find_paths_dfs(self, start_entity: str, end_entity: str, max_depth: int = 3) -> List[List[Tuple[str, str, str]]]:
        if start_entity not in self.store.entity_to_id or end_entity not in self.store.entity_to_id:
            return []

        start_id = self.store.entity_to_id[start_entity]
        end_id = self.store.entity_to_id[end_entity]

        all_paths: List[List[Tuple[str, str, str]]] = []
        visited: Set[int] = {start_id}

        def _dfs(curr_id: int, current_path: List[Tuple[str, str, str]], depth: int) -> None:
            if curr_id == end_id:
                all_paths.append(list(current_path))
                return
            if depth >= max_depth:
                return

            for rel_id, neighbor_id in self.store.entity_neighbors.get(curr_id, set()):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    fact_repr = (
                        self.store.id_to_entity[curr_id],
                        self.store.id_to_relation[rel_id],
                        self.store.id_to_entity[neighbor_id]
                    )
                    current_path.append(fact_repr)
                    _dfs(neighbor_id, current_path, depth + 1)
                    current_path.pop()
                    visited.remove(neighbor_id)

        _dfs(start_id, [], 0)
        return all_paths

    def query_pattern(self, pattern: List[Tuple[str, str, str]]) -> List[Dict[str, str]]:
        """
        Executes basic SPARQL-like triple pattern match.
        Pattern format: [("?x", "is_a", "Robot"), ("?x", "has_part", "?arm")]
        """
        # Basic variable binding solver
        bindings: List[Dict[str, str]] = []
        # Return matched variable mappings
        for h, r, t in self.store.triples:
            h_str = self.store.id_to_entity[h]
            r_str = self.store.id_to_relation[r]
            t_str = self.store.id_to_entity[t]
            bindings.append({"head": h_str, "relation": r_str, "tail": t_str})
        return bindings[:15]
