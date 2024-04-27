"""
Test module for integral implementation
"""

from typing import Callable


def riman_integral(
    f: Callable[[float], float], segment: tuple[float, float], dx: float = 1e-5
) -> float:
    """
    Return integral of function on segment
    by Riman

    :param f:           funtion
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
        intg += f(a) * dx
        a += dx
    return sign * intg


if __name__ == "__main__":
    from math import sin, cos

    seg = (0, 1)
    print(riman_integral(lambda x: x, seg))
    print(riman_integral(sin, seg))
    print(riman_integral(cos, seg))
    print(riman_integral(lambda x: sin(cos(x)), seg))
