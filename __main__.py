import time
import pyo
import configparser
import jackserver
import flanger 

import socket

import bridge
SOCKET_TIMEOUT = 30 #seconds

def start_pyo_server():
    """Start the Pyo server
    
    Return the pyo instance of the server
    """
    pyo_server = pyo.Server(audio='jack', nchnls=1).boot()
    #pyo_server.setJackAuto( False, False )
    pyo_server.start()
    return pyo_server


def chain_effects( initial_source, config_effects_dict ):
    main_volume = 0.5 #default volume 
    enabled_effects = [initial_source]
    for effect in sorted(config_effects_dict.keys()):

        source = enabled_effects[len(enabled_effects) - 1]

        # print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
        params = config_effects_dict[effect]
        if effect == 'volume':
            # volume stuff
            print("Volume captured")
            main_volume=float(params['vol'])

        elif params['name'] == 'distortion':
            # distortion stuff
            print("Enable distortion effect")
            enabled_effects.append(pyo.Disto(
                source,
                drive=float(params['drive']),
                slope=float(params['slope']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'delay':
            # delay stuff
            print("Enable delay effect")
            enabled_effects.append(pyo.Delay(
                source,
                delay=[0, float(params['delay'])],
                feedback=float(params['feedback']),
                maxdelay=10,
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'reverb':
            # reverb stuff
            print("Enable reverb effect")
            enabled_effects.append(pyo.STRev(
                source,
                inpos=0.25,
                revtime=float(params['revtime']),
                cutoff=float(params['cutoff']),
                bal=float(params['balance']),
                roomSize=float(params['roomsize']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'chorus':
            # chorus stuff
            print("Enable chorus effect")
            enabled_effects.append(pyo.Chorus(
                source,
                depth=float(params['depth']),
                feedback=float(params['feedback']),
                bal=float(params['balance']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'flanger':
            # flanger stuff
            print("Enable flanger effect")
            enabled_effects.append(flanger.Flanger(
                source,
                depth=float(params['depth']),
                freq=float(params['freq']),
                feedback=float(params['feedback']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'freqshift':
            # frequency shift stuff
            print("Enable frequency shift effect")
            enabled_effects.append(pyo.FreqShift(
                source,
                shift=params['shift'],
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'harmonizer':
            # harmonizer stuff
            print("Enable harmonizer effect")
            enabled_effects.append(pyo.Harmonizer(
                source,
                transpo=params['transpose'],
                feedback=float(params['feedback']),
                winsize=0.1,
                mul=main_volume,
                add=0)
            )

    return enabled_effects


def apply_effects( effects_list ):
    effects_list[len(effects_list) - 1].out()


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(('', 10000))

    #jackserver.start_jack_server(2, 1)

    pyo_server = start_pyo_server()
    pyo_server.setJackAuto()

    # Read input from the audio device on channel 1
    enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())

    apply_effects( enabled_effects )

    while True:
        # Effects have now been loaded from last good configuration
        # and the modulator is ready, so we'll block and await
        # await a new configuration. When one arrives, we'll
        # restart the program
        res = bridge.backend(s)
        if res:
            print(res)
            enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())
            apply_effects(enabled_effects)
        #print(res)
        time.sleep(1)


if __name__ == "__main__":
    main()
