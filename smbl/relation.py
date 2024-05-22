from __future__ import annotations
from copy import copy


class Relation2:
    def __init__(self, 
                 relation: set[tuple[int, int]] = set(), 
                 M: set[int] = set()):
        """
        :param relation: set with relation pairs
        :param M: set with relation elements
        """
        self._relation = relation
        if M == set():
            m = set()
            for a, b in self._relation:
                m.add(a)
                m.add(b)
            self._M = m 
        else:
            self._M = M

    def __contains__(self, pair: tuple[int, int]) -> bool:
        """
        Check pair in relation
        """
        return pair in self._relation

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
    def M(self):
        return copy(self._M)

    @property
    def pairs(self) -> set[tuple[int, int]]:
        """
        :return: pairs in relation
        """
        return copy(self._relation)

    @property
    def Pr1(self) -> set[int]:
        pr1 = set()
        for a, _ in self._relation:
            pr1.add(a)
        return pr1

    @property
    def Pr2(self) -> set[int]:
        pr2 = set()
        for _, b in self.pairs:
            pr2.add(b)
        return pr2

    @property
    def r(self) -> Relation2:
        """
        Return inverse relation
        """
        return self**(-1)

    def startswith(self, s: int) -> set[tuple[int, int]]:
        """
        Return all pairs which starts with [s]
        """
        st = set()
        for a, b in self.pairs:
            if a == s:
                st.add((a, b))
        return st

    def endswith(self, e: int) -> set[tuple[int, int]]:
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
            return Relation2(new_relation)
        elif p == 0:
            raise ValueError("Invalid power value: 0")
        elif p == -1:
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

    def __mul__(self, relation: Relation2) -> Relation2:
        """
        Multiplicate two relation

        (a, b) in (p1 * p2) <=>  E c: (a, c) in p1 and (c, b) in p2 
        """
        res = set()
        for a, b in self.pairs:
            for _, d in relation.startswith(b):
                res.add((a, d))
        return Relation2(res)

    def __str__(self) -> str:
        return str(self.pairs)


def reflexive(relation: Relation2) -> bool:
    """
    Check relation is reflexive

    A a in M: (a, a) in p
    """
    for a in relation.M:
        if (a, a) not in relation:
            return False
    return True


def irreflexive(relation: Relation2) -> bool:
    """
    Check relation is irreflexive

    A a in M: (a, a) not in p
    """
    for a in relation.M:
        if (a, a) in relation:
            return False
    return True


def symmetric(relation: Relation2) -> bool:
    """
    Check relation is symmetric 

    A a,b: (a, b) in p => (b, a) in p 
    """
    for a, b in relation.pairs:
        if (b, a) not in relation:
            return False
    return True


def asymmetric(relation: Relation2) -> bool:
    """
    Check relation is asymmetric 

    A a,b: (a, b) in p => (b, a) not in p 
    """
    for a, b in relation.pairs:
        if (b, a) in relation:
            return False
    return True


def antisymmetric(relation: Relation2) -> bool:
    """
    Check relation is antisymmetric 

    A a,b: (a, b) in p and (b, a) in p => a = b 
    """
    for a, b in relation.pairs:
        if a != b and (b, a) in relation:
            return False
    return True


def transitive(relation: Relation2) -> bool:
    """
    Check relation is transitive

    A a,b,c: (a, b) in p and (b, c) in p => (a, c) in p
    """
    for a, b in relation.pairs:
        for _, c in relation.startswith(b):
            if (a, c) not in relation:
                return False
    return True


def antitransitive(relation: Relation2) -> bool:
    """
    Check relation is transitive

    A a,b,c: (a, b) in p and (b, c) in p => (a, c) not in p
    """
    for a, b in relation.pairs:
            for _, c in relation.startswith(b):
                if (a, c) in relation:
                    return False
    return True


def connected(relation: Relation2) -> bool:
    """
    Check relation is connected

    A a,b: (a, b) in p or (b, a) in p
    """
    for pair in zip(relation.M, relation.M):
        if pair not in relation:
            return False
    return True


def transitive_closure(relation: Relation2) -> Relation2:
    """
    Return transitive closure of relation p
    is the smallest relation on M that contains p and is transitive
    """
    transitive_closure_pairs = copy(relation.pairs)

    for a, b in relation.pairs:
        for _, c in relation.startswith(b):
            if (a, c) not in relation:
                transitive_closure_pairs.add((a, c))
    
    return Relation2(transitive_closure_pairs)

