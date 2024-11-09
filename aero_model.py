"""
This function predicts the aerodynamic loading on a rotor

Author: Matthew Asper
Created: 8 Novemeber 2024

Inputs:
c:      blade chord (m)
DL:     disk loading (N/m2)
N:      number of rotors
nb:     number of blades per rotor
omega:  rotor speed (rad/s)
R:      rotor radius (m)
rho:    air density (kg/m^3)

Outputs:
CP:     power coefficient
CT:     thrust coefficient
FM:     figure of merit

"""
import numpy as np

def rotor_loading(DL=2, N=4, R=.05, omega=100*2*np.pi/60, rho=1.225, nb=4, c=.02):

    # tip speed
    Vtip    = omega * R

    CT      = DL / rho / Vtip**2

    # rotor solidity
    sigma   = nb * c / np.pi / R

    # blade loading
    BL      = CT / sigma

    # average lift coefficient across rotor blade
    Cl_bar  = 6 * BL

    # lift curve slope (/rad)
    cla     = 5.73

    # average angle of attack (rad)
    AoA_bar = Cl_bar / cla

    # mean drag coefficient
    Cd_bar  = 0.0087 - 0.035 * AoA_bar + 0.4 * AoA_bar**2



    return

if __name__=="__main__":
    rotor_loading()