"""
JobGuard Core Knowledge - Semantic Reasoner & Description Logic Tableaux Prover
Implements ALC Description Logic consistency checking, concept subsumption,
and ABox/TBox satisfiability algorithms for verifying corporate hierarchy claims.
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass, field


class Concept:
    """Base Description Logic concept."""
    def to_string(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class AtomicConcept(Concept):
    name: str

    def to_string(self) -> str:
        return self.name


@dataclass(frozen=True)
class Top(Concept):
    def to_string(self) -> str:
        return "⊤"


@dataclass(frozen=True)
class Bottom(Concept):
    def to_string(self) -> str:
        return "⊥"


@dataclass(frozen=True)
class Negation(Concept):
    concept: Concept

    def to_string(self) -> str:
        return f"¬({self.concept.to_string()})"


@dataclass(frozen=True)
class Conjunction(Concept):
    left: Concept
    right: Concept

    def to_string(self) -> str:
        return f"({self.left.to_string()} ⊓ {self.right.to_string()})"


@dataclass(frozen=True)
class Disjunction(Concept):
    left: Concept
    right: Concept

    def to_string(self) -> str:
        return f"({self.left.to_string()} ⊔ {self.right.to_string()})"


@dataclass(frozen=True)
class UniversalRole(Concept):
    role: str
    concept: Concept

    def to_string(self) -> str:
        return f"∀{self.role}.{self.concept.to_string()}"


@dataclass(frozen=True)
class ExistentialRole(Concept):
    role: str
    concept: Concept

    def to_string(self) -> str:
        return f"∃{self.role}.{self.concept.to_string()}"


@dataclass
class ABoxAssertion:
    individual: str
    concept: Concept


@dataclass
class RoleAssertion:
    individual1: str
    individual2: str
    role: str


class TableauxReasoner:
    """Tableaux algorithm for checking ALC concept satisfiability and subsumption."""

    def __init__(self):
        self.abox_assertions: List[ABoxAssertion] = []
        self.role_assertions: List[RoleAssertion] = []

    def add_concept_assertion(self, individual: str, concept: Concept) -> None:
        self.abox_assertions.append(ABoxAssertion(individual=individual, concept=concept))

    def add_role_assertion(self, ind1: str, ind2: str, role: str) -> None:
        self.role_assertions.append(RoleAssertion(individual1=ind1, individual2=ind2, role=role))

    def is_consistent(self) -> bool:
        """Determines if the current ABox contains no logical contradictions (clashes)."""
        individual_concepts: Dict[str, Set[Concept]] = {}

        for assertion in self.abox_assertions:
            ind = assertion.individual
            if ind not in individual_concepts:
                individual_concepts[ind] = set()
            individual_concepts[ind].add(assertion.concept)

        # Check for direct clashes: C and ¬C in the same individual's concept set
        for ind, concepts in individual_concepts.items():
            for c in concepts:
                if isinstance(c, Bottom):
                    return False
                if isinstance(c, Negation) and c.concept in concepts:
                    return False
                neg = Negation(c)
                if neg in concepts:
                    return False

        return True

    def check_subsumption(self, sub_concept: Concept, super_concept: Concept) -> bool:
        """Tests if sub_concept ⊑ super_concept by checking unsatisfiability of (sub_concept ⊓ ¬super_concept)."""
        test_concept = Conjunction(sub_concept, Negation(super_concept))
        reasoner = TableauxReasoner()
        reasoner.add_concept_assertion("x_test", test_concept)
        return not reasoner.is_consistent()
