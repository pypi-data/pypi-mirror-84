#
# author: Jungtaek Kim (jtkim@postech.ac.kr)
# last updated: November 5, 2020
#

import numpy as np

from benchmarks.benchmark_base import Function


def fun_target(bx, dim_bx):
    assert len(bx.shape) == 1
    assert bx.shape[0] == dim_bx

    y = 2 * bx[0]**2 - 1.05 * bx[0]**4 + 1.0 / 6.0 * bx[0]**6 + bx[0] * bx[1] + bx[1]**2
    return y


class ThreeHumpCamel(Function):
    def __init__(self):
        dim_bx = 2
        bounds = np.array([
            [-5.0, 5.0],
            [-5.0, 5.0],
        ])
        global_minimizers = np.array([
            [0.0, 0.0],
        ])
        global_minimum = 0.0
        function = lambda bx: fun_target(bx, dim_bx)

        Function.__init__(self, dim_bx, bounds, global_minimizers, global_minimum, function)
