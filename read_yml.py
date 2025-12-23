import yaml

def read_yml(full_path):
    """
    This function reads a .yml file from a specified 'full_path' and returns contents in 'config_data'.

    Author: Matt Asper (matt.asper101@gmail.com)
    Date Revised: 23 December 2025
    """

    # Open the file and load the data safely
    try:
        with open(full_path, 'r') as file:
            config_data = yaml.safe_load(file)

        return config_data
    except FileNotFoundError:
        print(f"Error: The file {full_path} was not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")
