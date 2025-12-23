'''
Initialize this module first to begin the eVTOL design process. 

Module functions
- initialization: 
    -- queries user to input aircraft requirements.
    -- return aircraft object with requirements and vehicle specifications
- compute_MTOW
- display_specs
- output_specs


Author: Matt Asper
Last Revised: 22 December 2025
'''
from ambiance import Atmosphere

class vehicle_class():
    def __init__(self):
        """
        This function initializes the vehicle and queries the user for requirements.

        inputs
        --------
        self.reqs                   :   requirements dictionary {dict}
        self.reqs["range"]          :   required cruise range [m]
        self.reqs["payload"]        :   required payload [kg]
        self.reqs["vtas_cruise"]    :   required true airspeed during cruise [m/s]
        self.reqs["endurance"]      :   required endurance [s]

        
        outputs
        --------
        self.iter                   :   iteration counter to converge MTOW [-]
        self.reqs["MTOW"]           :   max takeoff weight [kg]
        """

        print(f"Starting vehicle design process...\n")

        self.reqs = dict()

        # query user to input requirements
        self.reqs["range"]        = {"value": float(input("Input cruise range in meters: ")), "units": "m"}
        self.reqs["payload"]      = {"value": float(input("Enter required payload in kilograms: ")), "units": "kg"}
        self.reqs["vtas_cruise"]  = {"value": float(input("Enter required cruise speed (true) in meters per second: ")), "units": "m/s"}
        self.reqs["endurance"]    = {"value": float(input("Enter required endurance in seconds: ")), "units": "s"}

        # initialize iteration counter for vehicle weight
        self.iter = 1

        # estimate MTOW based on emprical data
        self.compute_MTOW()

        return
    
    def compute_MTOW(self, margin=1):
        """
        This function computes the maximum takeoff weight of the aircraft.

        inputs
        ------
        margin      :   factor added to MTOW computation to account for uncertainty

        outputs
        ------
        self.reqs["MTOW"]   :   max takeoff weight of the aircraft [kg]

        """

        if self.iter == 1:
            # first guess of MTOW assumes payload mass fraction is 15%
            self.reqs["MTOW"] = {"value": self.reqs["payload"]["value"] / 0.15 * margin, "units": "kg"}

        else:
            self.reqs["MTOW"]["value"] = 0  #reset MTOW for new calc

            # loop through vehicle subsystem and sum weights
            for key, value in self.subsystem.items():
                self.reqs["MTOW"]["value"] += self.subsystem[key][mass] * margin


    def display_specs(self):
        """"
        This function prints the aircraft specifications to the screen.
        """

        print(f"Displaying vehicle specifications...\n")
        print(f"-------------------------------\n")

        for key, value in self.reqs.items():
            print(f"{key} \t: \t {value["value"]} {round(value["units"],1)}\n")

    def output_specs(self, filepath, filename):
        """
        This function exports the aircraft specifications to a comma deliminted file.

        Inputs
        ------
        filepath    : string that specifies the relative filepath for the csv file.
        filename    : filename for the csv file.        
        """
        #TODO: finish this


if __name__=="__main__":
    vehicle = vehicle_class()
    vehicle.display_specs()
