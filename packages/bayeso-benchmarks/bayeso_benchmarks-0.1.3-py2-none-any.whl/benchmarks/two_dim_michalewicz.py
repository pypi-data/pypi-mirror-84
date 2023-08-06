#
# author: Jungtaek Kim (jtkim@postech.ac.kr)
# last updated: November 5, 2020
#

import numpy as np

from benchmarks.benchmark_base import Function


def fun_target(bx, dim_bx):
    assert len(bx.shape) == 1
    assert bx.shape[0] == dim_bx

    y = 0.0

    for ind in range(0, dim_bx):
        y += np.sin(bx[ind]) * np.sin(((ind + 1.0) * bx[ind]**2) / np.pi)**(2.0 * 10.0)
    y *= -1.0

    return y


class Michalewicz(Function):
    def __init__(self):
        dim_bx = 2
        bounds = np.array([
            [0.0, np.pi],
            [0.0, np.pi],
        ])
        global_minimizers = np.array([
            [2.20279089, 1.57063923],
        ])
        global_minimum = -1.801302197
        function = lambda bx: fun_target(bx, dim_bx)

        Function.__init__(self, dim_bx, bounds, global_minimizers, global_minimum, function)
