"""
This function computes the distance travelled via specified duration (dt) and velocity (V)

Inputs
-----
dt      :   duration [time]
V       :   n-dimensional numpy array of velocity data [length/time]

Outputs
-----
X       :   n-dimensional numpy array of displacement data [length]

Author: Matt Asper
Last Revised: 23 December 2025
"""
import numpy as np

def compute_distance(dt, V):

    X = dt * V

    return X