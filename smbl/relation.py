from __future__ import annotations


class Relation2:
    def __init__(self, relation: set[tuple[int, int]]):
        self.relation = relation

    def __contains__(self, pair: tuple):
        return pair in self.relation

    def M(self) -> set[int]:
        m = set()
        for a, b in self.relation:
            m.add(a)
            m.add(b)
        return m

    def Pr1(self) -> set[int]:
        pr1 = set()
        for a, _ in self.relation:
            pr1.add(a)
        return pr1

    def Pr2(self) -> set[int]:
        pr2 = set()
        for _, b in self.relation:
            pr2.add(b)
        return pr2

    def startwith(self, s: int) -> set[tuple]:
        st = set()
        for a, b in self.relation:
            if a == s:
                st.add((a, b))
        return st

    def endwith(self, e: int) -> set[tuple]:
        ed = set()
        for a, b in self.relation:
            if b == e:
                ed.add((a, b))
        return ed

    def __pow__(self, p: int):
        if p < 0:
            return (p**(-1))**abs(p) 
        elif p == 0:
            raise ValueError("Invalid power value: 0")
        elif p == -1:
            new_relation = set()
            for a, b in self.relation:
                new_relation.add((b, a))
            return Relation2(new_relation)
        else:
            res = self
            rel = self 
            while p:
                if p % 2:
                    res *= rel
                rel *= rel
                p >>= 1
            return res

    def __mul__(self, relation: Relation2) -> Relation2:
        res = set()
        for a, b in self.relation:
            for _, d in relation.startwith(b):
                res.add((a, d))
        return Relation2(res)

    def __str__(self) -> str:
        return str(self.relation)



