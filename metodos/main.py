import math

from incremental.incremental import incremental_search
from bisection.bisection import bisection
from false_position.false_position import false_position
from trisection.trisection import trisection
from newton_interpolation.newton_interpolation import newton_interpolation


# =====================================================
# ROOT-FINDING FUNCTION
# =====================================================

def f(x):
    return math.log((math.sin(x))**2 + 1) - 0.5


# =====================================================
# ROOT-FINDING METHODS
# =====================================================

incremental_search(f, x0=-3, h=0.5, N=100)

bisection(f, a=0, b=1, tol=1e-7, N=100)

false_position(f, a=0, b=1, tol=1e-7, N=100)

trisection(f, a=0, b=1, tol=1e-7, N=100)


# =====================================================
# NEWTON INTERPOLATION DATA
# =====================================================

X = [-1, 0, 3, 4]
Y = [15.5, 3, 8, 1]


# =====================================================
# NEWTON INTERPOLATION METHOD
# =====================================================

newton_interpolation(X, Y)