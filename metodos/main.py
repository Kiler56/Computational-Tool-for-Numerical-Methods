import math

from incremental.incremental import incremental_search
from bisection.bisection import bisection
from false_position.false_position import false_position
from trisection.trisection import trisection
from newton_interpolation.newton_interpolation import newton_interpolation
from composite_trapezoidal.composite_trapezoidal import composite_trapezoidal


# =====================================================
# ROOT-FINDING FUNCTION
# =====================================================

def f(x):
    return math.log((math.sin(x))**2 + 1) - 0.5


# =====================================================
# ROOT-FINDING METHODS
# =====================================================

print("\n===== ROOT-FINDING METHODS =====\n")

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

print("\n===== NEWTON INTERPOLATION =====\n")

newton_interpolation(X, Y)


# =====================================================
# COMPOSITE TRAPEZOIDAL METHOD
# =====================================================

# Example function
def g(x):
    return x**2


# Approximate integral on [0, 2]
composite_trapezoidal(g, a=0, b=2, n=4)