"""
This module implement basic function and tools
for work with binary relation
"""
from __future__ import annotations
from .relation import Relation


class BinaryRelation(Relation):
    """
    Binary relation implementation
    """
    def __init__(self, 
                 relation: set[tuple] = set(), 
                 M: set = set()):
        """
        :param relation: set with relation pairs
        :param M: set with relation elements
        """
        super().__init__(relation, M)
        
    @property
    def matrix(self) -> list[list[int]]:
        mat = [ [0 for _ in self.M] for _ in self.M]
        elems = list(self.M)
        for a, b in self.pairs:
            i = elems.index(a)
            j = elems.index(b)
            mat[i][j] = 1
        return mat

    @property
    def pairs(self) -> set[tuple]:
        """
        :return: pairs in relation
        """
        return self.relation 

    @property
    def Pr1(self) -> set[int]:
        """
        Let p = { (a_1, b_1), (a_2, b_2), ... }
        :return: first projection of relation {a_1, a_2, ...}
        """
        pr1 = set()
        for a, _ in self._relation:
            pr1.add(a)
        return pr1

    @property
    def Pr2(self) -> set[int]:
        """
        Let p = { (a_1, b_1), (a_2, b_2), ... }
        :return: second projection of relation {b_1, b_2, ...}
        """
        pr2 = set()
        for _, b in self.pairs:
            pr2.add(b)
        return pr2

    @property
    def r(self) -> BinaryRelation:
        """
        Return inverse relation
        """
        return self**(-1)

    def startswith(self, s: int) -> set[tuple]:
        """
        Return all pairs which starts with [s]
        """
        st = set()
        for a, b in self.pairs:
            if a == s:
                st.add((a, b))
        return st

    def endswith(self, e: int) -> set[tuple]:
        """
        Return all pairs which ends with [e]
        """
        ed = set()
        for a, b in self.pairs:
            if b == e:
                ed.add((a, b))
        return ed

    def __pow__(self, p: int):
        if p == -1:
            new_relation = set()
            for a, b in self.pairs:
                new_relation.add((b, a))
            return BinaryRelation(new_relation)
        elif p == 0:
            raise ValueError("Invalid power value: 0")
        elif p < 0:
            return (p**(-1))**abs(p) 
        else:
            res = self
            rel = self 
            p -= 1
            while p:
                if p % 2:
                    res *= rel
                rel *= rel
                p >>= 1
            return rel

    def __mul__(self, relation: BinaryRelation) -> BinaryRelation:
        """
        Multiplicate two relation

        (a, b) in (p1 * p2) <=>  E c: (a, c) in p1 and (c, b) in p2 
        """
        res = set()
        for a, b in self.pairs:
            for _, d in relation.startswith(b):
                res.add((a, d))
        return BinaryRelation(res)

    def __invert__(self) -> BinaryRelation:
        return self.r

    def transitive_closure(self) -> BinaryRelation:
        """
        Return transitive closure of relation p
        is the smallest relation on M that contains p and is transitive
        """
        transitive_closure_pairs = self.pairs

        for a, b in self.pairs:
            for _, c in self.startswith(b):
                if (a, c) not in self:
                    transitive_closure_pairs.add((a, c))
        
        return BinaryRelation(transitive_closure_pairs)



