"""
Test module for integral implementation
"""
from typing import Callable


def stieltjes_integral(f: Callable[[float], float],
                       g: Callable[[float], float],
                       segment: tuple[float, float],
                       dx: float = 1e-5) -> float:
    """
    Return integral of function on segment
    by Riman-Stieltjes

    :param f:           funtion
    :param g:           not-decreasing function 
    :param segment:     segment
    :param dx:          segment len

    :return:            integral value
    """
    intg = 0
    a, b = segment

    sign = -1 if a > b else 1
    if a > b:
        a, b = b, a

    while a <= b:
        dg = g(a + dx) - g(a)
        if dg < 0:
            raise TypeError("Invalid type of g function, it must be non-decreasing")
        intg += f(a) * dg
        a += dx
    return sign * intg


def riman_integral(f: Callable[[float], float], 
                   segment: tuple[float, float], 
                   dx: float = 1e-5) -> float:
    """
    Return integral of function on segment
    by Riman

    :param f:           funtion
    :param segment:     segment
    :param dx:          segment len

    :return:            integral value
    """
    return stieltjes_integral(f, lambda x: x, segment, dx) 


if __name__ == "__main__":
    from math import sin, cos, pi

    seg = (0, 1)
    print(stieltjes_integral(cos, sin, (0, pi/2)))
    print(riman_integral(lambda x: x, seg))
    print(riman_integral(sin, seg))
    print(riman_integral(cos, seg))
    print(riman_integral(lambda x: sin(cos(x)), seg))
