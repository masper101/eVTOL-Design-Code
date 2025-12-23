"""
This function exercises Ambiance's Atmosphere module to find atmospheric quanties and 
returns them to the 'atmos' object.

Inputs
-----
alt         :   geometric height above sea level [m]

Outputs
-----
atmos           :   dictionary of atmospheric quantities
atmos["rho"]    :   air density [kg/m^3]
atmos["P0"]     :   static pressure [Pa]
atmos["T0"]     :   static temperature [K]
atmos["mu"]     :   dynamic viscosity [kg/(m*s)]
atmos["a"]      :   speed of sound [m/s]

Assumptions
-----
If length of alt > 1, then the atmospheric model will return the average value of 100 interpolated
values of the respective atmospheric quantity. 
"""

from ambiance import Atmosphere
import numpy as np

def get_atmos(alt):

    atmos = dict()  # initialize atmospheric dictionary

    if len(alt) > 1:
        alt_interp = np.linspace(min(alt), max(alt), 100)
        atmos_interp = Atmosphere(alt_interp)

    atmos["rho"] = np.average(Atmosphere(alt).density)
    atmos["P0"] = np.average(Atmosphere(alt).pressure)
    atmos["T0"] = np.average(Atmosphere(alt).temperature)
    atmos["mu"] = np.average(Atmosphere(alt).dynamic_viscosity)
    atmos["a"] = np.average(Atmosphere(alt).speed_of_sound)

    return atmos