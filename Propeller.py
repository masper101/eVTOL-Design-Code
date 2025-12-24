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


    def run_propLoading(self, model, T, rho, a):
        """
        This exercises user-specified propeller loading models to estimate performance.

        Inputs
        -----
        model       : str specifying the loading model 
                        "MT" momentum theory
                        "BET" blade element theory
                        "BEMT" blade element momentum theory
        
        Ouputs
        -----
        self.perf   : dictionary of propeller performance data
        """

        # select propeller model
        if model == "MT":
            self.run_momentumTheory(T, rho, a)
        elif model == "BET":
            self.run_bladeElementTheory()
        elif model == "BET":
            self.run_bladeElementMomentumTheory()
        else:
            raise ValueError("Inappropriate propeller model selected. " \
            "Available models include 'MT', 'BET', and 'BEMT'.")

    
    def run_momentumTheory(self, T, rho, a, kappa=1.15):  #TODO:Validate trends
        """
        This function applies momentum theory to determine propeller performance.

        Inputs
        -----
        T                   :   required total propeller thrust [N]
        self.params["Np"]   :   number of propellers [-]
        rho                 :   ambient air density [kg/m^3]
        self.params["DL"]   :   total propeller disk loading [Pa]
        a                   :   ambient speed of sound [m/s]
        self.params["sigma"]:   propeller solidity [-]
        kappa               :   indcued power factor [-]
        
        Outputs
        -----
        self.perf           :   dictionary of propeller performance data
        self.params["A"]    :   total propeller area [m^2]
        self.params["Ap"]   :   individual propeller area [m^2]
        self.params["R"]    :   individual propeller radius [m]
        self.perf["RPM"]    :   propeller speed [rev/min]
        self.perf["P"]      :   total propeller power required [W]
        self.perf["Pp"]     :   individual propeller power required [W]
        self.perf["Tp"]     :   individual propeller thrust [N]
        self.perf["FM"]     :   propeller figure of merit [-]
        """

        # compute propeller geometry
        A = T / self.params["DL"]["value"]
        Ap = A / self.params["Np"]["value"]
        R = np.sqrt(Ap / np.pi)

        # required propeller thrust
        Tp = T / self.params["Np"]["value"]

        # propeller speed
        Vtip = self.params["Mtip"]["value"] * a
        RPM = Vtip / R * 60 / (2 * np.pi)

        # thrust coefficient
        CT = self.params["DL"]["value"] / rho / Vtip**2

        # blade loading
        BL = CT / self.params["sigma"]["value"]

        # average lift coefficient across propeller blade
        Cl_bar = 6 * BL

        # lift curve slope (/rad)
        Cla = 5.73

        # average angle of attack (rad)
        alpha_bar = Cl_bar / Cla

        # mean drag coefficient based on Bailey's Drag Curve
        Cd_bar  = 0.0087 - 0.035 * alpha_bar + 0.4 * alpha_bar**2

        # propeller powers
        P0 = 1/8 * rho * Cd_bar * self.params["sigma"]["value"] * A * Vtip**3  # total profile
        Ph = T * np.sqrt(self.params["DL"]["value"] / 2 / rho)  # ideal hover power
        Pi = kappa * Ph  # actual induced power
        P = Pi + P0  # total propeller power
        Pp = P / self.params["Np"]["value"]  # individual propeller power 

        # figure of merit
        FM = T * np.sqrt(self.params["DL"]["value"] / 2 / rho) / P

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

        return self

    def run_bladeElementTheory(self, T, rho):
        #TODO: finish this function
        raise NotImplementedError("This function hasn't been written yet.")

    def run_bladeElementMomentumTheory(self, T, rho):
        #TODO: finish this function
        raise NotImplementedError("This function hasn't been written yet.")
    
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



if __name__=="__main__":
    
    # initialize propeller
    Np      = {"name": "Np",    "value": 4,         "units": "-"}  # number of propellers
    Mtip    = {"name": "Mtip",  "value": 0.4,       "units": "-"}  # tip mach
    sigma   = {"name": "sigma", "value": 0.08,      "units": "-"}  # solidity 
    DL      = {"name": "DL",    "value": 500,       "units": "Pa"}  # disk loading [Pa]

    prop_specs = {
        "Np"        :   Np,  
        "Mtip"     :   Mtip,  
        "sigma"     :   sigma,  
        "DL"        :   DL,   
    }
    
    prop = Propeller(**prop_specs)

    # run condition
    alt = 10  # hover alt [m]
    atmos = Atmosphere(alt)  # atmospheric data
    rho = float(atmos.density)  # air density
    T = 1 / 0.15 * 9.81  # required total propeller thrust [N]
    a = float(atmos.speed_of_sound)  # speed of sound in air [m/s]
    prop.run_propLoading("MT", T, rho, a)
    prop.display_params()


    # sweep DLs and store FM
    DLsweep = np.linspace(100, 700)
    FM = np.zeros(DLsweep.shape)
    CT = np.zeros(DLsweep.shape)
    for i in range(len(DLsweep)):
        DL      = {"name": "DL",    "value": DLsweep[i],       "units": "Pa"}  # disk loading [Pa]

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
        T = 1 / 0.15 * 9.81  # required total propeller thrust [N]
        a = float(atmos.speed_of_sound)  # speed of sound in air [m/s]
        prop.run_propLoading("MT", T, rho, a)

        FM[i] = prop.perf["FM"]["value"] 
        CT[i] = DLsweep[i] / (rho * (prop.perf["RPM"]["value"] * np.pi / 30 * prop.params["R"]["value"])**2)     

    # Create plotly figure
    fig = go.Figure()   

    fig.add_trace(go.Scatter(
        x=CT, 
        y=FM, 
        mode='lines', 
    ))

    # Add labels
    fig.update_layout(
        xaxis_title="Thrust Coefficient [-]",
        yaxis_title="Figure of Merit [-]"
    )

    # Show plot
    fig.show()

