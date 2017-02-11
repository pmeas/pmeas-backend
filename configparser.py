import json

def readConfigFile():
    """
    Reads the configuration file stored in config/
    Returns string being read.
    """
    config_file = open("config/effects.txt")
    return config_file.read()

def parseConfigFile(config_data):
    config_data = json.loads(config_data)
    print("Effect: " + config_data['effect'])
    parameters = config_data['parameters']
    print("Parameters: " + str(parameters))

contents = readConfigFile()
parseConfigFile(contents)
