"""
This module creates a Motor(s) object(s) to
1) store motor properties
2) estimate performance data via a varitey of analytical methods


Author: Matt Asper (matt.asper101@gmail.com)
Last Revised: 27 February 2026
"""

import numpy as np
from add_dictEntry import add_dictEntry

class Motor:

    def __init__(self, **kwargs):
        """
        This function initializes the motor(s) objects and appends user-provided 
        kwargs, which are a dictionary of fixed motor parameters.

        Inputs
        -----
        kwargs["Nm"]        :   number of motors [-]
        kwargs["GR"]        :   gear ratio of gearbox attached to motor 
                                (rotor speed/motor speed) [-]        

        Outputs
        -----
        self.params         :   dictionary of motor parameters

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 27 February 2026
        """

        # unwrap kwargs and store under 'params'
        self.params = dict()
        for key, value in kwargs.items():
            self.params[key] = value

    def compute_performance(self, model: str, *args):
        """
        This functions executes the user-specified motor performance 'model' 
        to estimate motor performance.

        Inputs
        -----
        model               :   motor performance model to be executed
                                    'simple' for fixed efficiency model
                                    'parametric' for parametric motor model
        *args               :   various inputs that are required which are specific to 
                                    selected model
        
        Outputs
        -----
        self.perf["P"]      :   total motor power output [W]
        self.perf["Pin"]    :   required total motor power input [W]
        self.perf["Q"]      :   total motor torque output [Nm]
        self.perf["RPM"]    :   motor speed [rev/min]
        self.perf["eta"]    :   total motor efficiency [-]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 27 February 2026
        """

        if model == 'simple':
            P, Pin, eta, RPM, Q = self.run_fixedEfficiency(*args)
        elif model == 'parametric':
            P, Pin, eta, RPM, Q = self.run_parametricEfficiency(*args)
        else:
            raise ValueError(f"Incorrect motor model selected.\nAvailable models are 'simple' or 'parametric'.")
        
        # save performance parameters to perf dictionary
        self.perf = dict()
        self.perf["P"] = add_dictEntry("P", P, "W")
        self.perf["Pin"] = add_dictEntry("Pin", Pin, "W")
        self.perf["eta"] = add_dictEntry("eta", eta, "-")
        self.perf["RPM"] = add_dictEntry("Pin", RPM, "rev/min")
        self.perf["Q"] = add_dictEntry("Q", Q, "Nm")

        return self

    def run_fixedEfficiency(self, eta: float, RPM: float, Q: float):
        """
        This function computes the total motor power required based on an
        assumed efficiency.

        Inputs
        -----
        eta         :   efficiency of all motors [-]
        RPM         :   speed of all motors [rev/min] 
        Q           :   total motor torque output [Nm]

        Outputs
        -----
        P           :   total power output from all motors [W]
        Pin         :   total power input required for all motors [W]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 27 February 2026
        """

        P = Q * RPM * (np.pi / 30)
        Pin = P / eta

        return P, Pin, eta, RPM, Q

    def run_parametricEfficiency(self, RPM: float, Q: float, Q_pk: float, eta_pk: float, RPM_pk: float):
        """
        This function computes the total motor power required based on a 
        parametric efficiency developed by McDonald (doi: 10.2514/6.2014-0536).

        Inputs
        -----
        RPM         :   speed of all motors [rev/min] 
        Q           :   total motor torque output [Nm]
        eta_pk      :   peak efficiency of all motors [-]
        RPM_pk      :   speed at peak efficiency of all motors [rev/min] 
        Q_pk        :   total motor torque output at peak efficiency [Nm]

        Outputs
        -----
        eta         :   efficiency of all motors [-]
        P           :   total power output from all motors [W]
        Pin         :   total power input required for all motors [W]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 27 February 2026
        """

        # convert speeds to rad/s
        w = RPM * (np.pi / 30)
        w_pk = RPM_pk * (np.pi / 30)

        # define constants
        k0 = 0.5  # assumed parasite loss ratio [-]

        # parametric model loss coefficients
        C0 = k0 * w_pk * Q_pk / 6 * (1 - eta_pk) / eta_pk
        C1 = -1.5 * C0 / w_pk + Q_pk * (1 - eta_pk) / 4 / eta_pk
        C2 = 0.5 * C0 / w_pk**3 + Q_pk * (1 - eta_pk) / 4 / eta_pk / w_pk**2
        C3 = 0.5 * w_pk * (1 - eta_pk) / Q_pk / eta_pk

        # calculate powers
        P = Q * w
        P_L = C0 + C1 * w + C2 * w**3 + C3 * Q**2
        Pin = P + P_L

        # calculate efficiency
        eta = P / (P + P_L)

        return P, Pin, eta, RPM, Q
        
    def compute_weight(self, Q: float):
        """
        This function estimates the motor weight 
        required to provide a user-specified torque.

        Inputs
        -----
        Q                   :   required output torque from all motors [Nm]

        Outputs
        -----
        self.params["W"]    :   motor weight [N]

        Author: Matt Asper (matt.asper101@gmail.com)
        Last revised: 27 February 2026
        """

        # check if compute_performance has been executed
        if hasattr(self, 'perf'):
            
            # extract variables
            Q = self.perf["Q"]["value"]
            GR = self.params["GR"]["value"]
            eta = self.perf["eta"]["value"]
            eta_GB = 0.98  # TODO: update with gearbox efficiency model
            
            W = 0.4 * (Q / GR / eta / eta_GB)**0.71 * 9.81

        else:

            raise NotImplementedError("Need to execute compute_performance before compute_weight.")
        
        self.params["W"] = add_dictEntry("W", W, "N")

        return self
    