from __future__ import annotations
from typing import override


class Vector:
    def __init__(self, *values):
        self.values = values

    def __add__(self, vec: Vector) -> Vector:
        return type(self)(*[a + b for a, b in zip(self.values, vec.values)])

    @property
    def inverse(self) -> Vector:
        return (-1) * self
    
    def __sub__(self, vec: Vector) -> Vector:
        return self + vec.inverse

    @override
    def __mul__(self, vec: Vector) -> int | float | complex:
        return sum([a * b for a, b in zip(self.values, vec.values)])
    
    def __rmul__(self, other) -> Vector:
        return type(self)(*[a * other for a in self.values])

    def __repr__(self) -> str:
        return f"Vector{self.values}"
