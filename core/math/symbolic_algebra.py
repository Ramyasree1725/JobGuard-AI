"""
JobGuard Core Math - Symbolic Algebra & Automatic Differentiation
Builds symbolic expression trees (AST), evaluates symbolic derivatives,
and performs algebraic simplifications for threat optimization models.
"""

from typing import Union, Dict, Optional


class Expr:
    """Base symbolic algebraic expression node."""
    def eval(self, env: Dict[str, float]) -> float:
        raise NotImplementedError

    def diff(self, var: str) -> "Expr":
        raise NotImplementedError

    def __add__(self, other: Union["Expr", float]) -> "Expr":
        other_node = Const(other) if isinstance(other, (int, float)) else other
        return Add(self, other_node)

    def __mul__(self, other: Union["Expr", float]) -> "Expr":
        other_node = Const(other) if isinstance(other, (int, float)) else other
        return Mul(self, other_node)


class Const(Expr):
    def __init__(self, val: float):
        self.val = float(val)

    def eval(self, env: Dict[str, float]) -> float:
        return self.val

    def diff(self, var: str) -> Expr:
        return Const(0.0)

    def __repr__(self) -> str:
        return f"{self.val}"


class Var(Expr):
    def __init__(self, name: str):
        self.name = name

    def eval(self, env: Dict[str, float]) -> float:
        if self.name not in env:
            raise KeyError(f"Variable '{self.name}' not provided in evaluation environment")
        return env[self.name]

    def diff(self, var: str) -> Expr:
        return Const(1.0) if self.name == var else Const(0.0)

    def __repr__(self) -> str:
        return self.name


class Add(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def eval(self, env: Dict[str, float]) -> float:
        return self.left.eval(env) + self.right.eval(env)

    def diff(self, var: str) -> Expr:
        return Add(self.left.diff(var), self.right.diff(var))

    def __repr__(self) -> str:
        return f"({self.left} + {self.right})"


class Mul(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def eval(self, env: Dict[str, float]) -> float:
        return self.left.eval(env) * self.right.eval(env)

    def diff(self, var: str) -> Expr:
        # Product rule: (f*g)' = f'*g + f*g'
        return Add(Mul(self.left.diff(var), self.right), Mul(self.left, self.right.diff(var)))

    def __repr__(self) -> str:
        return f"({self.left} * {self.right})"
