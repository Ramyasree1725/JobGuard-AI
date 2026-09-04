"""
JobGuard Core Knowledge - Ontology & First-Order Predicate Reasoner
Implements forward/backward chaining inference over employment knowledge graphs,
subsumption reasoning, and contradiction detection for fraudulent corporate credentials.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Atom:
    predicate: str
    arguments: Tuple[str, ...]

    def __str__(self) -> str:
        args_str = ", ".join(self.arguments)
        return f"{self.predicate}({args_str})"


@dataclass
class Rule:
    rule_id: str
    head: Atom
    body: List[Atom]
    confidence: float = 1.0


class OntologyReasoner:
    """First-Order Logic Datalog-style forward chaining inference engine."""

    def __init__(self):
        self._facts: Set[Atom] = set()
        self._rules: List[Rule] = []
        self._class_hierarchy: Dict[str, Set[str]] = {}  # subclass -> superclasses
        self._load_recruitment_ontology()

    def _load_recruitment_ontology(self) -> None:
        """Initialize domain rules for corporate and recruitment authenticity."""
        # Rule 1: Free email + Corporate entity claim -> Impersonation Risk
        self.add_rule(Rule(
            rule_id="ONT-001",
            head=Atom("HighImpersonationRisk", ("?recruiter", "?company")),
            body=[
                Atom("ClaimsToRepresent", ("?recruiter", "?company")),
                Atom("UsesFreeEmailProvider", ("?recruiter", "?provider")),
                Atom("IsEstablishedEnterprise", ("?company",))
            ],
            confidence=0.95
        ))

        # Rule 2: Demands equipment check deposit -> Fraudulent Offer
        self.add_rule(Rule(
            rule_id="ONT-002",
            head=Atom("FraudulentOffer", ("?offer",)),
            body=[
                Atom("ContainsClause", ("?offer", "?clause")),
                Atom("DemandsVendorWireTransfer", ("?clause",))
            ],
            confidence=0.99
        ))

        # Rule 3: Zero upfront fees + Official HR portal + Verified domain -> Genuine Offer
        self.add_rule(Rule(
            rule_id="ONT-003",
            head=Atom("GenuineOffer", ("?offer",)),
            body=[
                Atom("HasZeroUpfrontFees", ("?offer",)),
                Atom("UsesOfficialHRPortal", ("?offer",)),
                Atom("HasVerifiedCorporateDomain", ("?offer",))
            ],
            confidence=0.99
        ))

    def add_fact(self, atom: Atom) -> None:
        self._facts.add(atom)

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def define_subclass(self, subclass: str, superclass: str) -> None:
        if subclass not in self._class_hierarchy:
            self._class_hierarchy[subclass] = set()
        self._class_hierarchy[subclass].add(superclass)

    def forward_chain(self, max_iterations: int = 20) -> Set[Atom]:
        """Derive all entailments from base facts using registered inference rules."""
        inferred_facts = set(self._facts)

        for _ in range(max_iterations):
            new_inferences = set()

            for rule in self._rules:
                # Find all variable substitution groundings satisfying rule body
                substitutions = self._find_substitutions(rule.body, inferred_facts)
                for subst in substitutions:
                    ground_head = self._apply_substitution(rule.head, subst)
                    if ground_head not in inferred_facts:
                        new_inferences.add(ground_head)

            if not new_inferences:
                break
            inferred_facts.update(new_inferences)

        self._facts = inferred_facts
        return inferred_facts

    def _find_substitutions(self, body_atoms: List[Atom], facts: Set[Atom]) -> List[Dict[str, str]]:
        if not body_atoms:
            return [{}]

        atom = body_atoms[0]
        remaining = body_atoms[1:]
        current_substs: List[Dict[str, str]] = []

        for fact in facts:
            if fact.predicate == atom.predicate and len(fact.arguments) == len(atom.arguments):
                subst: Dict[str, str] = {}
                match = True
                for a_arg, f_arg in zip(atom.arguments, fact.arguments):
                    if a_arg.startswith("?"):
                        subst[a_arg] = f_arg
                    elif a_arg != f_arg:
                        match = False
                        break
                if match:
                    current_substs.append(subst)

        if not remaining:
            return current_substs

        # Recursive join
        joined: List[Dict[str, str]] = []
        downstream = self._find_substitutions(remaining, facts)

        for s1 in current_substs:
            for s2 in downstream:
                # Check compatibility
                compatible = True
                merged = dict(s1)
                for k, v in s2.items():
                    if k in merged and merged[k] != v:
                        compatible = False
                        break
                    merged[k] = v
                if compatible:
                    joined.append(merged)

        return joined

    @staticmethod
    def _apply_substitution(atom: Atom, subst: Dict[str, str]) -> Atom:
        new_args = tuple(subst.get(arg, arg) for arg in atom.arguments)
        return Atom(atom.predicate, new_args)
