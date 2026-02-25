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


def run_propellerTest():

    # initialize propeller
    Np      = {"name": "Np",    "value": 4,         "units": "-"}  # number of propellers
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
    alpha = 0  # prop tilt [deg]
    V = 0  # flight speed [m/s]
    prop.run_propLoading("MT", T, rho, a, alpha, 0)
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
        # DL      = {"name": "DL",    "value": Vsweep[i],       "units": "Pa"}  # disk loading [Pa]

        # prop_specs = {
        #     "Np"        :   Np,  
        #     "Mtip"      :   Mtip,  
        #     "sigma"     :   sigma,  
        #     "DL"        :   DL,   
        # }

        # prop = Propeller(**prop_specs)

        # run condition
        prop.run_propLoading("MT", T, rho, a, alpha, Vsweep[i])

        FM[i] = prop.perf["FM"]["value"] 
        P[i] = prop.perf["P"]["value"]
        Pi[i] = prop.perf["Pi"]["value"]
        P0[i] = prop.perf["P0"]["value"]
        Pf[i] = prop.perf["Pf"]["value"]
        mu[i] = prop.perf["mu"]["value"]
        lam[i] = prop.perf["lam"]["value"]
        # CT[i] = Vsweep[i] / (rho * (prop.perf["RPM"]["value"] * np.pi / 30 * prop.params["R"]["value"])**2)     

    plot_multiple_lines([Vsweep, Vsweep, Vsweep, Vsweep], [P, Pi, P0, Pf], ["total", "induced", "profile", "propulsive"], "Power [W]", "Flight Speed [m/s]")


if __name__=="__main__":

    run_propellerTest()