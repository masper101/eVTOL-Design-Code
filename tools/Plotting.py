"""
This script is a collection of function to plotly arbitrary user-provided data with Plotly.

Author: Matt Asper
Last revised: 24 February 2026
"""

import plotly.graph_objects as go
from typing import List, Any

#TODO: edit function to so only one data point can be plotted
#TODO: edit function to change linestyle and color

def plot_multiple_lines(x_data: List[Any], y_data: List[Any], legends: List[str], yaxis: str = "Y-Axis", xaxis: str = "X-Axis"):
    """
    Plots multiple lines in a single Plotly figure.

    Inputs
    -----
    x_data: A list of x-axis data (each element is an array/list).
    y_data: A list of y-axis data (each element is an array/list).
    legends: A list of legend labels (strings) for each line.
    title: The title of the plot.

    Author: Matt Asper
    Last revised: 24 February 2026
    """
    if len(x_data) != len(y_data) != len(legends):
        raise ValueError("x_data_list, y_data_list, and legends must have the same number of elements.")

    # Create an empty figure
    fig = go.Figure()

    # Iterate through the data and add a trace for each line
    for i in range(len(x_data)):
        fig.add_trace(go.Scatter(
            x=x_data[i],
            y=y_data[i],
            mode='lines+markers', # Can change to 'lines', 'markers', or 'lines+markers'
            name=legends[i]
        ))

    # Update layout for title and general appearance
    fig.update_layout(
        xaxis_title=xaxis, # Customize your axis titles here
        yaxis_title=yaxis,
        legend_title="Data Series"
    )

    # Display the figure
    fig.show()

    return fig
