"""
This function sweeps propeller operating conditions and plots performance data to visualize trends and validate model.

Inputs
-----

Outputs
-----

Author: Matt Asper (matt.asper101@gmail.com)
Last revised: 24 February 2026
"""

import numpy as np
from ambiance import Atmosphere
from tools.Plotting import plot_multiple_lines
from Propeller import Propeller
import plotly.graph_objects as go

def run_propellerTest():

    # initialize propeller
    Np      = {"name": "Np",    "value": 5,         "units": "-"}  # number of propellers
    Mtip    = {"name": "Mtip",  "value": 0.2,       "units": "-"}  # tip mach
    sigma   = {"name": "sigma", "value": 0.12,      "units": "-"}  # solidity 
    DL      = {"name": "DL",    "value": 50,       "units": "Pa"}  # disk loading [Pa]

    prop_specs = {
        "Np"        :   Np,  
        "Mtip"      :   Mtip,  
        "sigma"     :   sigma,  
        "DL"        :   DL,   
    }
    
    prop = Propeller(**prop_specs)

    # run condition
    alt = 10  # hover alt [m]
    atmos = Atmosphere(alt)  # atmospheric data
    rho = float(atmos.density)  # air density
    T = .3 / 0.15 * 9.81  # required total propeller thrust [N]
    a = float(atmos.speed_of_sound)  # speed of sound in air [m/s]
    V = 0  # flight speed [m/s]
    prop.run_propLoading(0, "MT", T, rho, a)
    prop.display_params()


    # sweep V and store params
    Vsweep = np.linspace(0, 15, 100)
    FM = np.zeros(Vsweep.shape)
    # CT = np.zeros(Vsweep.shape)
    P = np.zeros(Vsweep.shape)
    Pi = np.zeros(Vsweep.shape)
    P0 = np.zeros(Vsweep.shape)
    Pf = np.zeros(Vsweep.shape)
    mu = np.zeros(Vsweep.shape)
    lam = np.zeros(Vsweep.shape)
    for i in range(len(Vsweep)):

        # run condition
        prop.run_propLoading(Vsweep[i], "MT", T, rho, a)

        FM[i] = prop.perf["FM"]["value"] 
        P[i] = prop.perf["P"]["value"]
        Pi[i] = prop.perf["Pi"]["value"]
        P0[i] = prop.perf["P0"]["value"]
        Pf[i] = prop.perf["Pf"]["value"]
        mu[i] = prop.perf["mu"]["value"]
        lam[i] = prop.perf["lam"]["value"]

    prop.optimize_speeds("MT", T, rho, a)


    #print best range speed perf
    print(f"\nPrinting best endurance speed performance...\n")
    prop.display_params()

    #create a reference line for P/V
    P_V = prop.perf["P_Vbr"]["value"] / prop.perf["V_br"]["value"]
    P_ref = P_V * Vsweep 

    fig = plot_multiple_lines([Vsweep, Vsweep, Vsweep, Vsweep, Vsweep], 
                        [P, Pi, P0, Pf, P_ref], 
                        ["total", "induced", "profile", "propulsive","reference"], 
                        "Power [W]", "Flight Speed [m/s]")
    
    #TODO: remove this after updating plotting
    fig.add_trace(
        go.Scatter(
            x=[prop.perf["V_br"]["value"]],
            y=[prop.perf["P_Vbr"]["value"]],
            mode='markers', # Display only as a marker
            name='P_Vbr', # Name for the legend
            marker=dict(
                color='red',  # Customize the marker color
                size=15,      # Customize the marker size
                symbol='star' # Customize the marker symbol (e.g., 'circle', 'diamond', 'star')
            )
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[prop.perf["V_be"]["value"]],
            y=[prop.perf["P_Vbe"]["value"]],
            mode='markers', # Display only as a marker
            name='P_Vbe', # Name for the legend
            marker=dict(
                color='green',  # Customize the marker color
                size=15,      # Customize the marker size
                symbol='diamond' # Customize the marker symbol (e.g., 'circle', 'diamond', 'star')
            )
        )
    )
    fig.show()


if __name__=="__main__":

    run_propellerTest()