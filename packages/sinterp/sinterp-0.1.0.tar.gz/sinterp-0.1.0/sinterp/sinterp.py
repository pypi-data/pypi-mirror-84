# -*- coding: utf-8 -*-


def interp1d(x: float, xp: list, yp: list) -> float:
    check_input(x, xp, yp)
    i1 = 0
    i2 = len(xp) - 1
    while i2 - i1 > 1:
        _ = int((i2 + i1) / 2)
        if x == xp[i1]:
            return yp[i1]
        elif x == xp[i2]:
            return yp[i2]
        elif xp[i1] < x < xp[_]:
            i2 = _
        elif xp[_] < x < xp[i2]:
            i1 = _
        else:
            return yp[_]
    return yp[i1] + ((x - xp[i1]) / (xp[i2] - xp[i1])) * (yp[i2] - yp[i1])


def check_input(x: float, xp: list, yp: list):
    if x < xp[0] or x > xp[-1]:
        raise ValueError('x-value is out of interpolation range')
    if len(xp) < 2:
        raise ValueError('xp-list should have minimum two items')
    if len(yp) < 2:
        raise ValueError('yp-list should have minimum two items')
    if len(xp) != len(yp):
        raise ValueError('xp-list and yp-list should have same length')
