"""
JobGuard Core NLP - Context-Free Grammar (CFG) & Shift-Reduce Syntax Parser
Parses sentence clause trees, detects deceptive passive constructions,
and extracts subject-verb-object (SVO) dependency structures from contracts.
"""

from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass, field


@dataclass
class ParseNode:
    symbol: str
    word: Optional[str] = None
    children: List["ParseNode"] = field(default_factory=list)

    def is_terminal(self) -> bool:
        return self.word is not None

    def to_string(self) -> str:
        if self.is_terminal():
            return f"({self.symbol} {self.word})"
        child_str = " ".join(c.to_string() for c in self.children)
        return f"({self.symbol} {child_str})"


class ShiftReduceParser:
    """Bottom-up Shift-Reduce parsing algorithm for formal recruitment grammar."""

    def __init__(self, grammar_rules: Optional[Dict[str, List[Tuple[str, ...]]]] = None):
        self.grammar = grammar_rules or self._default_grammar()

    @staticmethod
    def _default_grammar() -> Dict[str, List[Tuple[str, ...]]]:
        return {
            "S": [("NP", "VP")],
            "NP": [("Det", "N"), ("N",), ("Det", "Adj", "N"), ("NP", "PP")],
            "VP": [("V", "NP"), ("V",), ("V", "PP"), ("VP", "PP")],
            "PP": [("P", "NP")],
            "Det": [("the",), ("a",), ("an",), ("our",), ("this",)],
            "N": [("candidate",), ("company",), ("check",), ("fee",), ("deposit",), ("equipment",), ("offer",)],
            "V": [("deposit",), ("wire",), ("send",), ("pay",), ("receive",), ("sign",), ("review",)],
            "P": [("to",), ("for",), ("from",), ("with",), ("by",), ("at",)],
            "Adj": [("refundable",), ("cashier",), ("immediate",), ("approved",)]
        }

    def parse_tokens(self, tokens: List[Tuple[str, str]]) -> Optional[ParseNode]:
        """Parse list of (word, POS_tag) tuples into a ParseTree."""
        stack: List[ParseNode] = []
        input_queue = list(tokens)

        while input_queue or len(stack) > 1:
            # Try reduce
            reduced = False
            for lhs, rhs_list in self.grammar.items():
                for rhs in rhs_list:
                    k = len(rhs)
                    if len(stack) >= k:
                        match = True
                        for i in range(k):
                            if stack[-k + i].symbol != rhs[i]:
                                match = False
                                break
                        if match:
                            children = [stack.pop() for _ in range(k)][::-1]
                            parent = ParseNode(symbol=lhs, children=children)
                            stack.append(parent)
                            reduced = True
                            break
                if reduced:
                    break

            if not reduced:
                if input_queue:
                    word, tag = input_queue.pop(0)
                    leaf = ParseNode(symbol=tag, word=word)
                    stack.append(leaf)
                else:
                    break

        return stack[0] if len(stack) == 1 and stack[0].symbol == "S" else (stack[0] if stack else None)
