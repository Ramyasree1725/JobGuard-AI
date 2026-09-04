"""
Aetheris Optimization & Neural-Symbolic: Abstract Syntax Tree (AST) Genetic Expressions
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Dict, Any, Optional, Union


class ASTNode:
    """Base Node in Symbolic Expression Abstract Syntax Tree."""
    def evaluate(self, variables: Dict[str, float]) -> float:
        raise NotImplementedError

    def to_expression_string(self) -> str:
        raise NotImplementedError

    def clone(self) -> ASTNode:
        raise NotImplementedError

    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if hasattr(self, 'children'):
            for child in getattr(self, 'children'):
                nodes.extend(child.get_all_nodes())
        return nodes

    def depth(self) -> int:
        if not hasattr(self, 'children') or not getattr(self, 'children'):
            return 1
        return 1 + max(child.depth() for child in getattr(self, 'children'))


class ConstantNode(ASTNode):
    __slots__ = ('value',)

    def __init__(self, value: float) -> None:
        self.value = float(value)

    def evaluate(self, variables: Dict[str, float]) -> float:
        return self.value

    def to_expression_string(self) -> str:
        return f"{self.value:.3f}"

    def clone(self) -> ASTNode:
        return ConstantNode(self.value)


class VariableNode(ASTNode):
    __slots__ = ('var_name',)

    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def evaluate(self, variables: Dict[str, float]) -> float:
        return variables.get(self.var_name, 0.0)

    def to_expression_string(self) -> str:
        return self.var_name

    def clone(self) -> ASTNode:
        return VariableNode(self.var_name)


class BinaryOpNode(ASTNode):
    __slots__ = ('op', 'children')

    def __init__(self, op: str, left: ASTNode, right: ASTNode) -> None:
        self.op = op
        self.children = [left, right]

    @property
    def left(self) -> ASTNode:
        return self.children[0]

    @left.setter
    def left(self, val: ASTNode) -> None:
        self.children[0] = val

    @property
    def right(self) -> ASTNode:
        return self.children[1]

    @right.setter
    def right(self, val: ASTNode) -> None:
        self.children[1] = val

    def evaluate(self, variables: Dict[str, float]) -> float:
        lv = self.left.evaluate(variables)
        rv = self.right.evaluate(variables)
        try:
            if self.op == '+':
                return lv + rv
            elif self.op == '-':
                return lv - rv
            elif self.op == '*':
                return lv * rv
            elif self.op == '/':
                return lv / rv if abs(rv) > 1e-9 else 1.0 # Protected division
            elif self.op == '^':
                if lv <= 0.0:
                    return 0.0
                return math.pow(lv, max(-4.0, min(4.0, rv)))
        except (OverflowError, ValueError, ZeroDivisionError):
            return 0.0
        return 0.0

    def to_expression_string(self) -> str:
        return f"({self.left.to_expression_string()} {self.op} {self.right.to_expression_string()})"

    def clone(self) -> ASTNode:
        return BinaryOpNode(self.op, self.left.clone(), self.right.clone())


class UnaryOpNode(ASTNode):
    __slots__ = ('op', 'children')

    def __init__(self, op: str, child: ASTNode) -> None:
        self.op = op
        self.children = [child]

    @property
    def child(self) -> ASTNode:
        return self.children[0]

    @child.setter
    def child(self, val: ASTNode) -> None:
        self.children[0] = val

    def evaluate(self, variables: Dict[str, float]) -> float:
        cv = self.child.evaluate(variables)
        try:
            if self.op == 'sin':
                return math.sin(cv)
            elif self.op == 'cos':
                return math.cos(cv)
            elif self.op == 'exp':
                return math.exp(max(-10.0, min(10.0, cv)))
            elif self.op == 'log':
                return math.log(max(1e-6, abs(cv)))
            elif self.op == 'sqrt':
                return math.sqrt(abs(cv))
        except (OverflowError, ValueError):
            return 0.0
        return 0.0

    def to_expression_string(self) -> str:
        return f"{self.op}({self.child.to_expression_string()})"

    def clone(self) -> ASTNode:
        return UnaryOpNode(self.op, self.child.clone())


class TreeGenerator:
    """Random Symbolic AST Tree Builder using Ramped Half-and-Half method."""
    BINARY_OPS = ['+', '-', '*', '/']
    UNARY_OPS = ['sin', 'cos', 'exp', 'log', 'sqrt']

    @classmethod
    def generate_random_tree(
        cls,
        variables: List[str],
        max_depth: int = 4,
        method: str = "grow",
        rng: Optional[random.Random] = None
    ) -> ASTNode:
        r = rng if rng is not None else random
        if max_depth <= 1 or (method == "grow" and r.random() < 0.3):
            # Terminal node
            if r.random() < 0.6:
                return VariableNode(r.choice(variables))
            else:
                return ConstantNode(round(r.uniform(-3.0, 3.0), 2))

        # Non-terminal node
        if r.random() < 0.7:
            op = r.choice(cls.BINARY_OPS)
            left = cls.generate_random_tree(variables, max_depth - 1, method, r)
            right = cls.generate_random_tree(variables, max_depth - 1, method, r)
            return BinaryOpNode(op, left, right)
        else:
            op = r.choice(cls.UNARY_OPS)
            child = cls.generate_random_tree(variables, max_depth - 1, method, r)
            return UnaryOpNode(op, child)
