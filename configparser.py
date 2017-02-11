import json

def readConfigFile():
    """
    Reads the configuration file stored in config/
    Returns string being read.
    """
    config_file = open("config/effects.txt")
    config_data = config_file.read()
    config_file.close()
    return config_data

def parseConfigFile(config_data):
    """
    Parse the data from the file into respective
    objects.
    Currently prints the objects to the screen for testing.
    """
    config_data = json.loads(config_data)
    print("Effect: " + config_data['effect'])
    parameters = config_data['parameters']
    print("Parameters: " + str(parameters))

contents = readConfigFile()
parseConfigFile(contents)
