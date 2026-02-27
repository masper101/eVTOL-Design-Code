"""
This module creates a propeller(s) object to
1) store propeller properties
2) estimate performance data via a varitey of analytical methods


Author: Matt Asper (matt.asper101@gmail.com)
Last Revised: 24 December 2025
"""
import numpy as np
from add_dictEntry import add_dictEntry
from ambiance import Atmosphere
import plotly.graph_objects as go
from compute_inflow import compute_inflow
from tools.Plotting import plot_multiple_lines
from scipy.optimize import minimize_scalar

class Propeller:

    def __init__(self, **kwargs):
        """
        This function initializes the propeller class and stores propeller properties
        under 'params'.

        Inputs
        -----
        kwargs      :   dictionary of various propeller user-specified propeller parameters

        Outputs
        -----
        self.params :   dictionary of propeller parameters
        """

        # unwrap kwargs and store under 'params'
        self.params = dict()
        for key, value in kwargs.items():
            self.params[key] = value

    def run_propLoading(self, V, model, T, rho, a):
        """
        This exercises user-specified propeller loading models to estimate performance.

        Inputs
        -----
        model       : str specifying the loading model 
                        "MT" momentum theory
                        "BET" blade element theory
                        "BEMT" blade element momentum theory
        T           : required total propeller thrust [N]
        rho         : ambient air density [Pa]
        a           : speed of sound [m/s]
        
        Ouputs
        -----
        self.perf   : dictionary of propeller performance data
        """

        # select propeller model
        if model == "MT":
            self.run_momentumTheory(V, T, rho, a)
        elif model == "BET":
            self.run_bladeElementTheory()
        elif model == "BET":
            self.run_bladeElementMomentumTheory()
        else:
            raise ValueError("Inappropriate propeller model selected. " \
            "Available models include 'MT', 'BET', and 'BEMT'.")

    def run_momentumTheory(self, V, W, rho, a, kappa=1.15, k=4.2):  #TODO:Validate trends
        """
        This function applies momentum theory to determine propeller performance.

        Inputs
        -----
        W                   :   vehicle weight [N]
        self.params["Np"]   :   number of propellers [-]
        rho                 :   ambient air density [kg/m^3]
        self.params["DL"]   :   total propeller disk loading [Pa]
        a                   :   ambient speed of sound [m/s]
        self.params["sigma"]:   propeller solidity [-]
        kappa               :   indcued power factor [-]
        self.params["Mtip"] :   propeller tip mach number [-]
        V                   :   flight speed [m/s]
        k                   :   Frank Harris fuselage drag factor, typ. 1.5--4.2 [-]
        
        Outputs
        -----
        self.perf           :   dictionary of propeller performance data
        self.perf["T"]      :   required total propeller thrust [N]
        self.params["A"]    :   total propeller area [m^2]
        self.params["Ap"]   :   individual propeller area [m^2]
        self.params["R"]    :   individual propeller radius [m]
        self.perf["RPM"]    :   propeller speed [rev/min]
        self.perf["P"]      :   total propeller power required [W]
        self.perf["Pp"]     :   individual propeller power required [W]
        self.perf["Tp"]     :   individual propeller thrust [N]
        self.perf["FM"]     :   propeller figure of merit [-]
        self.perf["lam"]    :   propeller inflow [-]
        self.perf["Pi"]     :   total propeller induced power [W]
        self.perf["P0"]     :   total propeller profile power [W]
        self.perf["Pf"]     :   total propeller propulsive power [W]
        self.perf["alpha"]  :   rotor tilt [deg]
        """

        # Apply Frank Harris model to find propulsive power
        # TODO: verify appropriate k-value for different aircraft configs
        Wlb = W / 0.4536  # convert kg->lb
        F = k * self.params["Np"]["value"]**(1/3) * (Wlb/1000)**(2/3)  # [ft^2]
        F = F * (0.3048)**2  # [m^2]
        Df = 0.5 * rho * V**2 * F  # fuselage drag [N]
        Pf = Df * V  # required power to overcome fuselage drag [W]

        alpha_rad = np.atan(Df / W)  # propeller tilt angle [rad]
        alpha = alpha_rad * 180 / np.pi


        # compute required thrusts
        T = W / np.cos(alpha_rad)  # total
        Tp = T / self.params["Np"]["value"]  # individual 

        # compute propeller geometry
        A = W / self.params["DL"]["value"]
        Ap = A / self.params["Np"]["value"]
        R = np.sqrt(Ap / np.pi)

        # propeller speed
        Vtip = self.params["Mtip"]["value"] * a
        RPM = Vtip / R * 60 / (2 * np.pi)


        # thrust coefficient
        CT = T / rho / Vtip**2 / A

        # blade loading
        BL = CT / self.params["sigma"]["value"]

        # flow velocities
        mu = V * np.cos(alpha_rad) / Vtip  # adv ratio [-]
        lam_z = V * np.sin(alpha_rad) / Vtip  # in-plane [-]
        lam = compute_inflow(mu, lam_z, CT, (CT/2)**0.5)  # normalized inflow [-]

        # average lift coefficient across propeller blade
        Cl_bar = 6 * BL

        # lift curve slope (/rad)
        Cla = 5.73

        # average angle of attack (rad)
        alpha_bar = Cl_bar / Cla

        # mean drag coefficient based on Bailey's Drag Curve
        Cd_bar  = 0.0087 - 0.035 * alpha_bar + 0.4 * alpha_bar**2

        # profile drag factor
        Fp = 1 + 4.6 * mu**2

        # propeller powers
        P0 = 1/8 * rho * Cd_bar * self.params["sigma"]["value"] * A * Vtip**3  * Fp # total profile power
        Ph = T * Vtip * (lam - lam_z)  # ideal hover power
        Pi = kappa * Ph  # actual induced power
        P = Pi + P0 + Pf  # total propeller power
        Pp = P / self.params["Np"]["value"]  # individual propeller power 

        # figure of merit
        FM = Ph / P

        # update propeller params
        self.params["A"] = add_dictEntry("A", A, "m^2")
        self.params["Ap"] = add_dictEntry("Ap", Ap, "m^2")
        self.params["R"] = add_dictEntry("R", R, "m")

        # combine performance data into self.perf dictionary
        self.perf = dict()
        self.perf["T"] = add_dictEntry("T", T, "N")
        self.perf["Tp"] = add_dictEntry("Tp", Tp, "N")
        self.perf["P"] = add_dictEntry("P", P, "W")
        self.perf["Pp"] = add_dictEntry("Pp", Pp, "W")
        self.perf["RPM"] = add_dictEntry("RPM", RPM, "rev/min")
        self.perf["FM"] = add_dictEntry("FM", FM, "-")
        self.perf["lam"] = add_dictEntry("lam", lam, "-")
        self.perf["Pi"] = add_dictEntry("Pi", Pi, "W")
        self.perf["P0"] = add_dictEntry("P0", P0, "W")
        self.perf["Pf"] = add_dictEntry("Pf", Pf, "W")
        self.perf["alpha"] = add_dictEntry("alpha", alpha, "deg")
        self.perf["mu"] = add_dictEntry("mu", mu, "-")

        return self

    def run_bladeElementTheory(self, T, rho):
        #TODO: finish this function
        raise NotImplementedError("This function hasn't been written yet.")

    def run_bladeElementMomentumTheory(self, T, rho):
        #TODO: finish this function
        raise NotImplementedError("This function hasn't been written yet.")
    
    def range_objective(self, V, *args):
        """
        This function provides the objective function to minimize the 
        total propeller power required versus cruise speed cruise for 
        finding best range speed.

        Inputs
        -----
        model       : str specifying the loading model 
                        "MT" momentum theory
                        "BET" blade element theory
                        "BEMT" blade element momentum theory
        T           : required total propeller thrust [N]
        rho         : ambient air density [Pa]
        a           : speed of sound [m/s]
        V           : flight speed [m/s]
        
        Outputs
        -----
        P_total / V : total required propeller power per unit flight speed [N]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 26 February 2026
        """

        self.run_propLoading(V, *args)

        P_total = self.perf["P"]["value"]

        return P_total / V
    
    def endurance_objective(self, V, *args):
        """
        This function provides the objective function to minimize the 
        total propeller power for finding best endurance speed.

        Inputs
        -----
        model       : str specifying the loading model 
                        "MT" momentum theory
                        "BET" blade element theory
                        "BEMT" blade element momentum theory
        T           : required total propeller thrust [N]
        rho         : ambient air density [Pa]
        a           : speed of sound [m/s]
        V           : flight speed [m/s]

        Outputs
        -----
        P_total     : total required propeller power [W]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 26 February 2026
        """

        self.run_propLoading(V, *args)

        P_total = self.perf["P"]["value"]

        return P_total
        
    def optimize_speeds(self, model, T, rho, a):
        """
        This function computes the optimum endurance and best range speed for the vehicle 
        based on propeller cruise performance.

        Inputs
        -----
        model       : str specifying the loading model 
                        "MT" momentum theory
                        "BET" blade element theory
                        "BEMT" blade element momentum theory
        T           : required total propeller thrust [N]
        rho         : ambient air density [Pa]
        a           : speed of sound [m/s]

        Outputs
        -----
        self.perf["V_br"]   :   best range speed [m/s]
        self.perf["V_be"]   :   best endurance speed [m/s]
        self.perf["P_Vbr"]  :   total propeller power required at best range speed [W]
        self.perf["P_Vbe"]  :   total propeller power required at best endurance speed [W]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 26 February 2026
        """

        # find best range speed
        result = minimize_scalar(self.range_objective, args=(model, T, rho, a), bounds=(1e-6, 1e6))
        V_br = result.x
        P_Vbr = V_br * result.fun

        # find endurance range speed
        result = minimize_scalar(self.endurance_objective, args=(model, T, rho, a), bounds=(1e-6, 1e6))
        V_be = result.x
        P_Vbe = result.fun

        # save output variables to performance dictionary
        self.perf["V_br"] = add_dictEntry("V_br", V_br, "m/s")
        self.perf["P_Vbr"] = add_dictEntry("P_Vbr", P_Vbr, "W")
        self.perf["V_be"] = add_dictEntry("V_be", V_be, "m/s")
        self.perf["P_Vbe"] = add_dictEntry("P_Vbe", P_Vbe, "W")

        return self

    def display_params(self):
        """
        This function prints the propeller parameters in 'self.params' to the console.

        Inputs
        -----
        self.params     :   dictionary of propeller parameters
        """

        print(f"\nDisplaying propeller parameters...\n")
        print(f"---------------\n")

        for param, values in self.params.items():
            print(f"{param:15}\t:\t{values["value"]:10} [{values["units"]}]\n")

        print(f"\nDisplaying propeller performance parameters...\n")
        print(f"---------------\n")

        for param, values in self.perf.items():
            print(f"{param:15}\t:\t{values["value"]:10} [{values["units"]}]\n")

