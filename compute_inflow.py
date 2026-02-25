"""
This function finds the inflow through the propeller disk by applying newton_raphson.

Inputs
-----
mu          : adv ratio [-]
lam_z       : normalized incident velocity normal to prop disk [-]
CT          : thrust coefficient
lam0        : initial guess for normalized propeller inflow [-]
tol         : tolerance
max_iter    : maximum number of iterations

Outputs
-----
lam         : normalized propeller inflow [-]

Author: Matt Asper (matt.asper101@gmail.com)
Last revised: 17 February 2026
"""

import numpy as np
import plotly.graph_objects as go
from tools.newton_raphson import newton_raphson

def compute_inflow(mu, lam_z, CT, lam0, tol=1e-7, max_iter=100):

    f = lambda lam: lam - lam_z - CT / 2 / ((mu**2 + lam**2)**0.5)
    df = lambda lam: 1 + CT * lam / (2 * (mu**2 + lam**2)**1.5)

    lam = newton_raphson(f, df, lam0)

    return lam

if __name__ == "__main__":

    alpha = 0
    alpha2 = 8
    CT = 0.008
    lam_h = float(np.sqrt(CT/2))

    # sweep foward speeds
    mu_ratio = np.linspace(0, 10, 100)
    lam = np.zeros(mu_ratio.shape)
    lam2 = np.zeros(mu_ratio.shape)
    for i in range(len(mu_ratio)):
        mu = mu_ratio[i] * lam_h
        lam_z = mu * np.tan(alpha * np.pi / 180)
        lam[i] = compute_inflow(mu, lam_z, CT, (CT/2)**0.5)
        lam2_z = mu * np.tan(alpha2 * np.pi / 180)
        lam2[i] = compute_inflow(mu, lam2_z, CT, (CT/2)**0.5)

     # Create plotly figure
    fig = go.Figure()   

    fig.add_trace(go.Scatter(
        x=mu_ratio, 
        y=lam/lam_h, 
        mode='lines', 
        name="0 deg"
    ))

    fig.add_trace(go.Scatter(
        x=mu_ratio, 
        y=lam2/lam_h, 
        mode='lines', 
        name="8 deg"
    ))

    # Add labels
    fig.update_layout(
        xaxis_title="$\mu/\lambda_h$",
        yaxis_title="$\lambda/\lambda_h$"
    )

    # Show plot
    fig.show()