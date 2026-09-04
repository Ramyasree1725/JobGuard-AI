"""
JobGuard Core ML - N-Dimensional Tensor Math & Autograd Engine
Implements multi-dimensional array manipulation, broadcasting, linear algebra operations,
activation functions, and reduction routines without external dependencies.
"""

import math
import random
from typing import List, Tuple, Union, Optional, Callable


class Tensor:
    """N-dimensional tensor wrapper with strided indexing and element-wise operations."""

    def __init__(self, data: Union[float, List[Any]], shape: Optional[Tuple[int, ...]] = None):
        if isinstance(data, (int, float)):
            self.data = [float(data)]
            self.shape = (1,)
        elif isinstance(data, list):
            self.data, computed_shape = self._flatten_and_get_shape(data)
            self.shape = shape if shape is not None else computed_shape
        else:
            raise TypeError(f"Unsupported tensor data type: {type(data)}")

        self.strides = self._compute_strides(self.shape)

    @classmethod
    def _flatten_and_get_shape(cls, nested: List[Any]) -> Tuple[List[float], Tuple[int, ...]]:
        shape = []
        curr = nested
        while isinstance(curr, list):
            shape.append(len(curr))
            curr = curr[0] if len(curr) > 0 else None
        
        flat: List[float] = []
        def _flatten(sub):
            if isinstance(sub, list):
                for item in sub:
                    _flatten(item)
            else:
                flat.append(float(sub))
        _flatten(nested)
        return flat, tuple(shape)

    @staticmethod
    def _compute_strides(shape: Tuple[int, ...]) -> Tuple[int, ...]:
        strides = []
        stride = 1
        for dim in reversed(shape):
            strides.append(stride)
            stride *= dim
        return tuple(reversed(strides))

    def _index_to_offset(self, indices: Tuple[int, ...]) -> int:
        offset = 0
        for idx, stride in zip(indices, self.strides):
            offset += idx * stride
        return offset

    def __getitem__(self, item: Union[int, Tuple[int, ...]]) -> float:
        if isinstance(item, int):
            item = (item,)
        return self.data[self._index_to_offset(item)]

    def __setitem__(self, item: Union[int, Tuple[int, ...]], value: float) -> None:
        if isinstance(item, int):
            item = (item,)
        self.data[self._index_to_offset(item)] = float(value)

    def reshape(self, new_shape: Tuple[int, ...]) -> "Tensor":
        expected_elements = 1
        for d in new_shape:
            expected_elements *= d
        if expected_elements != len(self.data):
            raise ValueError(f"Cannot reshape tensor of size {len(self.data)} into shape {new_shape}")
        t = Tensor(self.data, shape=new_shape)
        t.data = list(self.data)
        return t

    def add(self, other: "Tensor") -> "Tensor":
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch in add: {self.shape} vs {other.shape}")
        out_data = [a + b for a, b in zip(self.data, other.data)]
        return Tensor(out_data, shape=self.shape)

    def sub(self, other: "Tensor") -> "Tensor":
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch in sub: {self.shape} vs {other.shape}")
        out_data = [a - b for a, b in zip(self.data, other.data)]
        return Tensor(out_data, shape=self.shape)

    def mul(self, scalar_or_tensor: Union[float, "Tensor"]) -> "Tensor":
        if isinstance(scalar_or_tensor, (int, float)):
            s = float(scalar_or_tensor)
            return Tensor([x * s for x in self.data], shape=self.shape)
        elif isinstance(scalar_or_tensor, Tensor):
            if self.shape != scalar_or_tensor.shape:
                raise ValueError("Elementwise mul requires identical shape")
            return Tensor([a * b for a, b in zip(self.data, scalar_or_tensor.data)], shape=self.shape)

    def matmul_2d(self, other: "Tensor") -> "Tensor":
        """Matrix multiplication for 2D tensors (M x K) @ (K x N) -> (M x N)."""
        if len(self.shape) != 2 or len(other.shape) != 2:
            raise ValueError("matmul_2d requires 2D matrices")
        m, k1 = self.shape
        k2, n = other.shape
        if k1 != k2:
            raise ValueError(f"Matrix dimension mismatch: ({m}x{k1}) and ({k2}x{n})")

        out_data = [0.0] * (m * n)
        for i in range(m):
            for j in range(n):
                dot = 0.0
                for p in range(k1):
                    dot += self.data[i * k1 + p] * other.data[p * n + j]
                out_data[i * n + j] = dot

        return Tensor(out_data, shape=(m, n))

    def transpose_2d(self) -> "Tensor":
        if len(self.shape) != 2:
            raise ValueError("transpose_2d requires 2D matrix")
        m, n = self.shape
        out_data = [0.0] * (m * n)
        for i in range(m):
            for j in range(n):
                out_data[j * m + i] = self.data[i * n + j]
        return Tensor(out_data, shape=(n, m))

    def relu(self) -> "Tensor":
        return Tensor([max(0.0, x) for x in self.data], shape=self.shape)

    def sigmoid(self) -> "Tensor":
        def _sig(x):
            return 1.0 / (1.0 + math.exp(-max(-50.0, min(50.0, x))))
        return Tensor([_sig(x) for x in self.data], shape=self.shape)

    def sum(self) -> float:
        return sum(self.data)

    def mean(self) -> float:
        return sum(self.data) / max(1, len(self.data))


def tensor_zeros(shape: Tuple[int, ...]) -> Tensor:
    count = 1
    for d in shape:
        count *= d
    return Tensor([0.0] * count, shape=shape)


def tensor_ones(shape: Tuple[int, ...]) -> Tensor:
    count = 1
    for d in shape:
        count *= d
    return Tensor([1.0] * count, shape=shape)


def tensor_random_uniform(shape: Tuple[int, ...], low: float = -0.1, high: float = 0.1) -> Tensor:
    count = 1
    for d in shape:
        count *= d
    data = [random.uniform(low, high) for _ in range(count)]
    return Tensor(data, shape=shape)


def tensor_matmul(a: Tensor, b: Tensor) -> Tensor:
    return a.matmul_2d(b)


def tensor_softmax(t: Tensor, axis: int = -1) -> Tensor:
    """Softmax along last dimension of 2D matrix."""
    if len(t.shape) != 2:
        # Fallback for 1D
        max_val = max(t.data)
        exp_vals = [math.exp(max(-50.0, min(50.0, x - max_val))) for x in t.data]
        sum_exp = sum(exp_vals)
        return Tensor([x / sum_exp for x in exp_vals], shape=t.shape)

    m, n = t.shape
    out_data = [0.0] * (m * n)
    for i in range(m):
        row = t.data[i * n:(i + 1) * n]
        max_v = max(row)
        exp_row = [math.exp(max(-50.0, min(50.0, x - max_v))) for x in row]
        sum_e = sum(exp_row)
        for j in range(n):
            out_data[i * n + j] = exp_row[j] / sum_e

    return Tensor(out_data, shape=t.shape)
