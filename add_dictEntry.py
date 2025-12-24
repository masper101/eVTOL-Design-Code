"""
This function adds entries to a user-provided dictionary

Inputs
-----
name    :   str specifying the variable name of the dictionary item
value   :   any specifying the value of the variable
units   :   str specifying the unit of the variable

Outputs
-----
dict_entry      :   dict for dictionary entry

Author: Matt Asper
Last Revised: 24 December 2025
"""

def add_dictEntry(name, value, units):

    dict_entry = {'name': name, 'value': value, 'units': units}

    return dict_entry
