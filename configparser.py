import json, os

PATH = "config/effects.json"

def read_config_file():
    """
    Reads the configuration file stored in config/
    Returns string being read.
    """
    effects_file = os.path.join( os.path.dirname(os.path.abspath(__file__)), PATH)

    config_file = open(effects_file)
    config_data = config_file.read()
    config_file.close()
    return config_data


def parse_json_data(config_data):
    """
    Parse the data formatted as json into respective
    objects.
    Currently prints the objects to the screen for testing.
    """
    config_data = json.loads(config_data)
    return config_data


def get_effects():
    """
    High level function that parses the configuration content
    and returns the result as a dictionary of effects.
    """
    file_contents = read_config_file()
    return parse_json_data(file_contents)

def update_config_file(data):
    """
    Overwrites the configuration file containing the effects and
    parameters with the new effects sent by the GUI interface.

    data -- the effects and parameters data sent by the GUI
            packaged in a JSON format.
    """
    data_to_json = json.dumps(data)

    effects_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), PATH)

    with open(effects_file, "w") as config_file:
        config_file.write(data_to_json)

