"""
JobGuard Core Knowledge - Semantic Triples Store & Resource Description Framework (RDF)
Provides subject-predicate-object semantic representation, SPARQL-like pattern matching,
blank node allocation, and namespace prefix management for fraud intelligence graphs.
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Iterator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class URI:
    val: str

    def __str__(self) -> str:
        return f"<{self.val}>"


@dataclass(frozen=True)
class Literal:
    val: str
    datatype: Optional[str] = None
    lang: Optional[str] = None

    def __str__(self) -> str:
        if self.lang:
            return f'"{self.val}"@{self.lang}'
        if self.datatype:
            return f'"{self.val}"^^{self.datatype}'
        return f'"{self.val}"'


@dataclass(frozen=True)
class BNode:
    val: str

    def __str__(self) -> str:
        return f"_:{self.val}"


RDFNode = Any  # Union[URI, Literal, BNode, str]


@dataclass(frozen=True)
class Triple:
    subject: str
    predicate: str
    object: str

    def __str__(self) -> str:
        return f"{self.subject} {self.predicate} {self.object} ."


class SemanticTripleStore:
    """Indexed Subject-Predicate-Object (SPO) Hexastore representation for fast graph queries."""

    def __init__(self):
        # 6 indices for comprehensive SPARQL query resolution
        self._spo: Dict[str, Dict[str, Set[str]]] = {}
        self._pos: Dict[str, Dict[str, Set[str]]] = {}
        self._osp: Dict[str, Dict[str, Set[str]]] = {}
        self._prefixes: Dict[str, str] = {}
        self._triples_count = 0
        self._init_standard_prefixes()

    def _init_standard_prefixes(self) -> None:
        self._prefixes["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self._prefixes["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
        self._prefixes["owl"] = "http://www.w3.org/2002/07/owl#"
        self._prefixes["xsd"] = "http://www.w3.org/2001/XMLSchema#"
        self._prefixes["jg"] = "https://jobguard.ai/ontology#"
        self._prefixes["threat"] = "https://jobguard.ai/threat#"

    def bind_prefix(self, prefix: str, uri_base: str) -> None:
        self._prefixes[prefix] = uri_base

    def expand_qname(self, qname: str) -> str:
        if ":" in qname and not qname.startswith("http://") and not qname.startswith("https://"):
            prefix, local = qname.split(":", 1)
            if prefix in self._prefixes:
                return f"{self._prefixes[prefix]}{local}"
        return qname

    def add_triple(self, s: str, p: str, o: str) -> bool:
        s_exp = self.expand_qname(s)
        p_exp = self.expand_qname(p)
        o_exp = self.expand_qname(o)

        # Update SPO
        if s_exp not in self._spo:
            self._spo[s_exp] = {}
        if p_exp not in self._spo[s_exp]:
            self._spo[s_exp][p_exp] = set()
        if o_exp in self._spo[s_exp][p_exp]:
            return False  # Already exists
        self._spo[s_exp][p_exp].add(o_exp)

        # Update POS
        if p_exp not in self._pos:
            self._pos[p_exp] = {}
        if o_exp not in self._pos[p_exp]:
            self._pos[p_exp][o_exp] = set()
        self._pos[p_exp][o_exp].add(s_exp)

        # Update OSP
        if o_exp not in self._osp:
            self._osp[o_exp] = {}
        if s_exp not in self._osp[o_exp]:
            self._osp[o_exp][s_exp] = set()
        self._osp[o_exp][s_exp].add(p_exp)

        self._triples_count += 1
        return True

    def remove_triple(self, s: str, p: str, o: str) -> bool:
        s_exp = self.expand_qname(s)
        p_exp = self.expand_qname(p)
        o_exp = self.expand_qname(o)

        if s_exp in self._spo and p_exp in self._spo[s_exp] and o_exp in self._spo[s_exp][p_exp]:
            self._spo[s_exp][p_exp].remove(o_exp)
            if not self._spo[s_exp][p_exp]:
                del self._spo[s_exp][p_exp]
            if not self._spo[s_exp]:
                del self._spo[s_exp]

            self._pos[p_exp][o_exp].remove(s_exp)
            if not self._pos[p_exp][o_exp]:
                del self._pos[p_exp][o_exp]
            if not self._pos[p_exp]:
                del self._pos[p_exp]

            self._osp[o_exp][s_exp].remove(p_exp)
            if not self._osp[o_exp][s_exp]:
                del self._osp[o_exp][s_exp]
            if not self._osp[o_exp]:
                del self._osp[o_exp]

            self._triples_count -= 1
            return True
        return False

    def query_pattern(
        self,
        s: Optional[str] = None,
        p: Optional[str] = None,
        o: Optional[str] = None
    ) -> Iterator[Triple]:
        """Pattern matching using optimized hexastore index lookup."""
        s_exp = self.expand_qname(s) if s else None
        p_exp = self.expand_qname(p) if p else None
        o_exp = self.expand_qname(o) if o else None

        # Case 1: (S, P, O) bound
        if s_exp and p_exp and o_exp:
            if s_exp in self._spo and p_exp in self._spo[s_exp] and o_exp in self._spo[s_exp][p_exp]:
                yield Triple(s_exp, p_exp, o_exp)

        # Case 2: (S, P, ?)
        elif s_exp and p_exp:
            if s_exp in self._spo and p_exp in self._spo[s_exp]:
                for obj in self._spo[s_exp][p_exp]:
                    yield Triple(s_exp, p_exp, obj)

        # Case 3: (S, ?, O)
        elif s_exp and o_exp:
            if o_exp in self._osp and s_exp in self._osp[o_exp]:
                for pred in self._osp[o_exp][s_exp]:
                    yield Triple(s_exp, pred, o_exp)

        # Case 4: (?, P, O)
        elif p_exp and o_exp:
            if p_exp in self._pos and o_exp in self._pos[p_exp]:
                for subj in self._pos[p_exp][o_exp]:
                    yield Triple(subj, p_exp, o_exp)

        # Case 5: (S, ?, ?)
        elif s_exp:
            if s_exp in self._spo:
                for pred, objs in self._spo[s_exp].items():
                    for obj in objs:
                        yield Triple(s_exp, pred, obj)

        # Case 6: (?, P, ?)
        elif p_exp:
            if p_exp in self._pos:
                for obj, subjs in self._pos[p_exp].items():
                    for subj in subjs:
                        yield Triple(subj, p_exp, obj)

        # Case 7: (?, ?, O)
        elif o_exp:
            if o_exp in self._osp:
                for subj, preds in self._osp[o_exp].items():
                    for pred in preds:
                        yield Triple(subj, pred, o_exp)

        # Case 8: (?, ?, ?) - All triples
        else:
            for subj, preds in self._spo.items():
                for pred, objs in preds.items():
                    for obj in objs:
                        yield Triple(subj, pred, obj)

    def size(self) -> int:
        return self._triples_count
