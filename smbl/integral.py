"""
Test module for integral implementation
"""
from typing import Callable, Any


def integral(f: Callable[[float], float], 
             segment: tuple[float, float],
             ep: float = 1e-5) -> float:
    """
    Return integral of function on segment
    by Riman
   
    :param f: funtion
    :param segment: segment
    :param ep: epsilon accuracy value
    :return: integral value
    """
    intg = 0
    a, b = segment

    sign = -1 if a > b else 1
    if a > b:
        a, b = b, a

    while a <= b:
        intg += f(a) * ep
        a += ep
    return sign * intg


if __name__ == "__main__":
    from math import sin, cos

    seg = (0, 1)
    print(integral(lambda x: x, seg))
    print(integral(sin, seg))
    print(integral(cos, seg))
    print(integral(lambda x: sin(cos(x)), seg))


