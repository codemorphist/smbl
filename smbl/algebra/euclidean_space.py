from .vector import Vector


def ortogonalize(a: list[Vector]) -> list[Vector]:
    """
    Gram–Schmidt process 
    """
    e = []

    for j in range(len(a)):
        ej = a[j]
        for s in range(j):
            ej += -(a[j] * e[s]) / (e[s] * e[s]) * e[s]
        e.append(ej) 
    return e

