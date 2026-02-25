"""
This function implements the Newton-Raphson method to find the root x
of a function f.

Inputs
-----
f           : function in terms of root x
df          : derivate of function wrt. x
x0          : initial guess of root
tol         : tolerance
max_iter    : maximum number of iterations

Outputs
-----
x           : root of function f

Author: Matt Asper (matt.asper101@gmail.com)
Last Revised: 12 February 2026
"""

import numpy as np

def newton_raphson(f, df, x0, tol=1e-7, max_iter=100):
    """
    Finds the root of f(x) = 0 using Newton-Raphson method.
    """
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        # Avoid division by zero
        if dfx == 0:
            print("Derivative is zero. No solution found.")
            return None
        
        # Newton-Raphson formula
        x_new = x - fx / dfx
        
        # Check for convergence
        if abs(x_new - x) < tol:
            return x_new
        
        x = x_new
        
    print("Maximum iterations reached.")
    return x


if __name__=="__main__":

    # Example: Find the root to inflow function
    f = lambda x: x - .1 - .05 / (2 * (.1**2 + x**2)**0.5)
    df = lambda x: 1 + .05 * x / (2 * (.1**2 + x**2)**1.5)

    root = newton_raphson(f, df, .005)
    print(f"Root: {root}")
