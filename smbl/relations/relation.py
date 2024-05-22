"""
This module implements basic funciton and tools
for work with relations
"""

from __future__ import annotations
from copy import copy


class Relation:
    def __init__(self, 
                 relation: set[tuple] = set(),
                 M: set = set()):
        self._relation = relation
        if M == set():
            self._M = set()
            for s in self._relation:
                for a in s:
                    self._M.add(a)
        else:
            self._M = M

    def __contains__(self, rel: tuple) -> bool:
        """
        Check pair in relation
        """
        return rel in self._relation

    @property
    def relation(self) -> set[tuple]:
        """
        :return: relation sets
        """
        return copy(self._relation)

    @property
    def M(self):
        """
        :return: set of relation elements
        """
        return copy(self._M)

    def __or__(self, relation: Relation) -> Relation:
        """
        Union of relations
        """
        return type(self)(self._relation | relation._relation)

    def __and__(self, relation: Relation) -> Relation:
        """
        Intersection of relations
        """
        return type(self)(self._relation & relation._relation)

    def __str__(self) -> str:
        return str(self._relation)



