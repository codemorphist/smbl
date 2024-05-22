"""
This module implements tools for check
basic properties of binary relations
"""
from .binary_relation import BinaryRelation

# -- BASIC PROPERTIES --

def reflexive(relation: BinaryRelation) -> bool:
    """
    Check relation is reflexive

    A a in M: (a, a) in p
    """
    for a in relation.M:
        if (a, a) not in relation:
            return False
    return True


def irreflexive(relation: BinaryRelation) -> bool:
    """
    Check relation is irreflexive

    A a in M: (a, a) not in p
    """
    for a in relation.M:
        if (a, a) in relation:
            return False
    return True


def symmetric(relation: BinaryRelation) -> bool:
    """
    Check relation is symmetric 

    A a,b: (a, b) in p => (b, a) in p 
    """
    for a, b in relation.pairs:
        if (b, a) not in relation:
            return False
    return True


def asymmetric(relation: BinaryRelation) -> bool:
    """
    Check relation is asymmetric 

    A a,b: (a, b) in p => (b, a) not in p 
    """
    for a, b in relation.pairs:
        if (b, a) in relation:
            return False
    return True


def antisymmetric(relation: BinaryRelation) -> bool:
    """
    Check relation is antisymmetric 

    A a,b: (a, b) in p and (b, a) in p => a = b 
    """
    for a, b in relation.pairs:
        if a != b and (b, a) in relation:
            return False
    return True


def transitive(relation: BinaryRelation) -> bool:
    """
    Check relation is transitive

    A a,b,c: (a, b) in p and (b, c) in p => (a, c) in p
    """
    for a, b in relation.pairs:
        for _, c in relation.startswith(b):
            if (a, c) not in relation:
                return False
    return True


def antitransitive(relation: BinaryRelation) -> bool:
    """
    Check relation is transitive

    A a,b,c: (a, b) in p and (b, c) in p => (a, c) not in p
    """
    for a, b in relation.pairs:
            for _, c in relation.startswith(b):
                if (a, c) in relation:
                    return False
    return True


def connected(relation: BinaryRelation) -> bool:
    """
    Check relation is connected

    A a,b: a != b => (a, b) in p or (b, a) in p
    """
    for a, b in zip(relation.M, relation.M):
        if a == b:
            continue
        if (a, b) not in relation and (b, a) not in relation:
            return False
    return True


def strongly_connected(relation: BinaryRelation) -> bool:
    """
    Check relation is connected

    A a,b: (a, b) in p or (b, a) in p
    """
    for a, b in zip(relation.M, relation.M):
        if (a, b) not in relation and (b, a) not in relation:
            return False
    return True

# -- COMBINATION OF PROPERTIES --

def equivalence(relation: BinaryRelation) -> bool:
    for prop in (reflexive, symmetric, transitive):
        if not prop(relation):
            return False
    return True


def partial_order(relation: BinaryRelation) -> bool:
    for prop in (reflexive, symmetric, transitive):
        if not prop(relation):
            return False
    return True

def strict_partial_order(relation: BinaryRelation) -> bool:
    for prop in (irreflexive, asymmetric, transitive):
        if not prop(relation):
            return False
    return True


def total_order(relation: BinaryRelation) -> bool:
    for prop in (reflexive, antisymmetric, transitive, connected):
        if not prop(relation):
            return False
    return True


def strict_total_order(relation: BinaryRelation) -> bool:
    for prop in (irreflexive, asymmetric, transitive, connected):
        if not prop(relation):
            return False
    return True
