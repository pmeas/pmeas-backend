import pyo
import time
import configparser

def start_pyo_server():
    """Start the Pyo server
    
    Return the pyo instance of the server
    """
    pyo_server = pyo.Server(audio='jack', nchnls=1).boot()
    pyo_server.start()
    return pyo_server

pyo_server = start_pyo_server()

enabled_effects = []

# Read input from the audio device on channel 1
enabled_effects.append(pyo.Input(chnl=0))

effects_dict = configparser.get_effects()
for effect in effects_dict.keys():
    #print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
    params = effects_dict[effect]
    if effect == 'distortion':
        #distortion stuff
        print("Enable distortion effect")
        enabled_effects.append(pyo.Disto(
                                enabled_effects[len(enabled_effects)-1],
                                drive=int(params['drive']),
                                slope=int(params['slope']),
                                mul=1,
                                add=0)
                            )
    elif effect == 'delay':
        #delay stuff
        print("Enable delay effect")
        enabled_effects.append(pyo.Delay(
                                enabled_effects[len(enabled_effects)-1],
                                delay=int(params['delay']),
                                feedback=int(params['feedback']),
                                mul=0.5)
                            )
    elif effect == 'reverb':
        #reverb stuff
        print("Enable reverb effect")
        enabled_effects.append(pyo.STRev(
                                enabled_effects[len(enabled_effects)-1],
                                inpos=0.25,
                                revtime=int(params['revtime']),
                                cutoff=int(params['cutoff']),
                                bal=int(params['balance']),
                                roomSize=int(params['roomsize']))
                            )
    elif effect == 'chorus':
        #chorus stuff
        print("Enable chorus effect")
        enabled_effects.append(pyo.Chorus(
                                enabled_effects[len(enabled_effects)-1],
                                depth=int(params['depth']),
                                feedback=int(params['feedback']),
                                bal=int(params['balance']),
                                mul=1,
                                add=0)
                            )
    elif effect == 'freqshift':
        #frequency shift stuff
        print("Enable frequency shift effect")
        enabled_effects.append(pyo.FreqShift(
                                enabled_effects[len(enabled_effects)-1],
                                shift=int(params['shift']),
                                mul=1,
                                add=0)
                            )
    elif effect == 'harmonizer':
        #harmonizer stuff
        print("Enable harmonizer effect")
        enabled_effects.append(pyo.Harmonizer(
                                enabled_effects[len(enabled_effects)-1],
                                transpo=int(params['transpose']),
                                feedback=int(params['feedback']),
                                winsize=0.1,
                                mul=1,
                                add=0)
                            )

enabled_effects[len(enabled_effects)-1].out()


# Eliminate need for GUI with loop - eventually to be used for updating effects.
# Will be the location of the socket that will establish connection with GUI
while True:
    time.sleep(1)
