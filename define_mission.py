"""
This class is used to define the aircraft mission profile.

Attributes
--------
- mission profile


Functions
--------
- input segments
- plot trajectory


Author: Matt Asper (matt.asper101@gmail.com)
Last Revised: 23 December 2025
"""

from ambiance import Atmosphere
from read_yml import read_yml
from pathlib import Path
import plotly.graph_objects as go
import numpy as np
from compute_distance import compute_distance

class Mission():

    def __init__(self, run_mode):
        """
        This function initializes the mission profile by querying the user and saving mission attributes to self.


        Inputs
        -----
        run_mode            :   str specifying how to run the mission initialization; "manual" or "auto"
        
        Outputs
        -----
        self.segments       :   list of mission degments
        self.segments[i]    :   dictionary of segment_i detailing mission attributes
        """

        if run_mode == "manual":
            #TODO: write code to query the user to input mission params.
            pass
        elif run_mode == "auto":
            full_path = Path("configs/group1_quad.yml")  # path to .yml config file
            config_params = read_yml(full_path)
            self.segments = config_params["mission"]["segments"]
            
            # loop through segments to compute distances travelled
            for i in range(len(self.segments)):
                V = np.array(self.segments[i]["Velocity"])
                self.segments[i]["Velocity"] = V  # convert Velocity to np array
                dt = float(self.segments[i]["duration"])
                self.segments[i]["Displacement"] = compute_distance(dt, V)  # compute distance traveled in segment

    def input_segments(self):
        """
        This function queries the user to input mission segment details.
        """

        #TODO: finish this function

        return
    
    def plot_trajectory(self):
        """
        This function plots the trajectory of the aircraft mission.
        """

        # Append mission segment trajectories to dX array
        dX = np.array([0, 0])

        for seg_i in self.segments:
            dX = np.vstack([dX, dX[-1]+seg_i["Displacement"]])
    
        # Create plotly figure
        fig = go.Figure()   

        # Loop through dX and plot trajectory
        for i in range(len(dX)-1):
            fig.add_trace(go.Scatter(
                x=dX[i:i+2,0], 
                y=dX[i:i+2,1], 
                mode='lines', 
                name=f'{self.segments[i]["name"]}' # Name for the legend
            ))
            
        # Add labels
        fig.update_layout(
            xaxis_title="X Displacement [m]",
            yaxis_title="Y Displacement [m]"
        )

        # Show plot
        fig.show()

if __name__=="__main__":
    mission = Mission(run_mode="auto")
    mission.plot_trajectory()

