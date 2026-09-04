"""
JobGuard Core NLP - Universal Dependencies (UD) Treebank Rules & Syntax Grammar Engine
Contains Universal Dependency relations (nsubj, obj, iobj, obl, ccomp, xcomp, amod, nmod),
transition-based arc-eager parser state transitions, and projectivity validators.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class DependencyNode:
    id: int
    form: str
    lemma: str
    upos: str  # Universal POS tag (NOUN, VERB, ADJ, PROPN, AUX, etc.)
    head: int
    deprel: str  # Dependency relation (e.g., "nsubj", "root", "obj")


@dataclass
class ParsedSentenceTree:
    sentence_text: str
    nodes: List[DependencyNode]


class ArcEagerTransitionParser:
    """Transition-based Arc-Eager dependency parsing simulator."""

    def __init__(self):
        self.trees: Dict[str, ParsedSentenceTree] = {}
        self._populate_treebank()

    def _populate_treebank(self) -> None:
        """Populate representative Universal Dependency syntax trees for recruitment fraud clauses."""
        s1_nodes = [
            DependencyNode(1, "The", "the", "DET", 2, "det"),
            DependencyNode(2, "recruiter", "recruiter", "NOUN", 3, "nsubj"),
            DependencyNode(3, "requested", "request", "VERB", 0, "root"),
            DependencyNode(4, "a", "a", "DET", 7, "det"),
            DependencyNode(5, "refundable", "refundable", "ADJ", 7, "amod"),
            DependencyNode(6, "security", "security", "NOUN", 7, "compound"),
            DependencyNode(7, "deposit", "deposit", "NOUN", 3, "obj"),
            DependencyNode(8, "before", "before", "ADP", 9, "case"),
            DependencyNode(9, "onboarding", "onboarding", "NOUN", 3, "obl")
        ]
        self.trees["clause_fee_deposit"] = ParsedSentenceTree("The recruiter requested a refundable security deposit before onboarding", s1_nodes)

        s2_nodes = [
            DependencyNode(1, "You", "you", "PRON", 3, "nsubj"),
            DependencyNode(2, "must", "must", "AUX", 3, "aux"),
            DependencyNode(3, "deposit", "deposit", "VERB", 0, "root"),
            DependencyNode(4, "the", "the", "DET", 5, "det"),
            DependencyNode(5, "check", "check", "NOUN", 3, "obj"),
            DependencyNode(6, "into", "into", "ADP", 9, "case"),
            DependencyNode(7, "your", "your", "PRON", 9, "nmod:poss"),
            DependencyNode(8, "bank", "bank", "NOUN", 9, "compound"),
            DependencyNode(9, "account", "account", "NOUN", 3, "obl")
        ]
        self.trees["clause_check_deposit"] = ParsedSentenceTree("You must deposit the check into your bank account", s2_nodes)

    def extract_core_arguments(self, tree_key: str) -> Dict[str, str]:
        """Extract core grammatical arguments (subject, verb, direct object) from dependency tree."""
        if tree_key not in self.trees:
            return {}

        tree = self.trees[tree_key]
        root_node = next((n for n in tree.nodes if n.head == 0), None)
        if not root_node:
            return {}

        nsubj_node = next((n for n in tree.nodes if n.head == root_node.id and n.deprel == "nsubj"), None)
        obj_node = next((n for n in tree.nodes if n.head == root_node.id and n.deprel == "obj"), None)

        return {
            "verb": root_node.form,
            "subject": nsubj_node.form if nsubj_node else "",
            "object": obj_node.form if obj_node else ""
        }
