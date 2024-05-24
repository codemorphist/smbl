from __future__ import annotations
from .vector import Vector


class Matrix:
    def __init__(self, elems: list[Vector]):
        self.elems = elems
