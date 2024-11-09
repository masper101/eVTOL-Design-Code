'''
This script defines the design point for the aircraft

By: Matt Asper
Date: 31 October 2024
'''
def inputs():
    payload = 0.2 # [kg]
    E       = 300 # [s]

    print(f'=========== Design Point ============')
    print(f'payload \t: {payload}\t kg')
    print(f'endurance \t: {E/60} \t min')
    print(f'=====================================\n')




if __name__=="__main__":
    inputs()
