import math

from incremental.incremental import incremental_search
from bisection.bisection import bisection
from false_position.false_position import false_position
from trisection.trisection import trisection


# 🔸 You can replace this function with any other one
def f(x):
    return math.log((math.sin(x))**2 + 1) - 0.5


# 🔸 Tests (you can change parameters without modifying methods)
incremental_search(f, x0=-3, h=0.5, N=100)

bisection(f, a=0, b=1, tol=1e-7, N=100)

false_position(f, a=0, b=1, tol=1e-7, N=100)

trisection(f, a=0, b=1, tol=1e-7, N=100)