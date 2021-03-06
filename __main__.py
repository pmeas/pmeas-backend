#!/usr/bin/python

GPIO_CAPABLE = False

import time
from functools import partial
import signal
import sys
import pyo
try:
    import RPi.GPIO as GPIO
    GPIO_CAPABLE = True
except ImportError:
    pass

if GPIO_CAPABLE:
    import gpiocontrol
import bridge
import configparser
import jackserver
import flanger 

import socket

SOCKET_TIMEOUT = 30 #seconds

button_pin = 17

PYO_INIT_SETTINGS = {
    'audio':'jack',
    'nchnls':1
}

def start_pyo_server():
    """Start the Pyo server
    
    Return the pyo instance of the server
    """
    print("Attempting to start the pyo server")
    pyo_server = pyo.Server(**PYO_INIT_SETTINGS).boot()
    print("Pyo server booted")
    pyo_server.start()
    print("Pyo server started")
    return pyo_server

def stop_pyo_server(pyo_server):
    """Stop the Pyo server
    """
    print("Attempting to stop the pyo server")
    pyo_server.stop()
    print("Pyo server stopped")


def chain_effects( initial_source, config_effects_dict ):
    '''
    Loop through the effects and assembles their configuration in order according to their keys.
    
    initial_source - the medium by which the audio stream is read (i.e through the input port)
    config_effects_dict - the list of effects to enable on top of the audio stream.
    '''
    vol = 1 #default volume
    enabled_effects = [initial_source]

    # Make the source of the next effect the previously applied effect.
    source = enabled_effects[len(enabled_effects) - 1]

    # If the volume was set, change the default value to the requested volume.
    if "volume" in config_effects_dict:
        vol = config_effects_dict.pop("volume")
        enabled_effects.append(pyo.Tone(
                source,
                freq = 20000,
                mul = vol
                )
        )
    
    # Run through all the effects in our configuration file and apply
    # them to the previously used stream (i.e source)
    for effect in sorted(config_effects_dict.keys()):
	source = enabled_effects[len(enabled_effects) - 1]
        # print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
        params = config_effects_dict[effect]

        if params['name'] == 'distortion':
            # distortion stuff
            print("Enable distortion effect")
            enabled_effects.append(pyo.Disto(
                source,
                drive=float(params['drive']),
                slope=float(params['slope']),
                mul = vol
                )
            )

        elif params['name'] == 'delay':
            # delay stuff
            print("Enable delay effect")
            enabled_effects.append(pyo.Delay(
                source,
                delay=[0, float(params['delay'])],
                feedback=float(params['feedback']),
                maxdelay=5,
                mul = vol
                )
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
                mul = vol
                )
            )

        elif params['name'] == 'chorus':
            # chorus stuff
            print("Enable chorus effect")
            enabled_effects.append(pyo.Chorus(
                source,
                depth=[(params['depth_min']), (params['depth_max'])],
                feedback=float(params['feedback']),
                bal=float(params['balance']),
                mul = vol
                )
            )

        elif params['name'] == 'flanger':
            # flanger stuff
            print("Enable flanger effect")
            enabled_effects.append(flanger.Flanger(
                source,
                depth=float(params['depth']),
                freq=float(params['freq']),
                feedback=float(params['feedback']),
                mul = vol
                )
            )

        elif params['name'] == 'freqshift':
            # frequency shift stuff
            print("Enable frequency shift effect")
            enabled_effects.append(pyo.FreqShift(
                source,
                shift=params['shift'],
                mul = vol
                )
            )

        elif params['name'] == 'harmonizer':
            # harmonizer stuff
            print("Enable harmonizer effect")
            enabled_effects.append(pyo.Harmonizer(
                source,
                transpo=params['transpose'],
                feedback=float(params['feedback']),
                winsize=0.1,
                mul = vol
                )
            )

        elif params['name'] == 'phaser':
            # phaser stuff
            print("Enable phaser effect")
            enabled_effects.append(pyo.Phaser(
                source,
                freq=float(params['frequency']),
                spread=float(params['spread']),
                q=float(params['q']),
                feedback=float(params['feedback']),
                num=int(params['num']),
                mul = vol
                )
            )

    return enabled_effects


def apply_effects( effects_list ):
    '''Once an effects list has been assembled by chain_effects, use this function to enable it'''
    effects_list[len(effects_list) - 1].out()
    print("APPLIED EFFECTS: ", effects_list)

def signal_handler(jack_id, pyo_server, signal, frame):
    '''Close the program and kill JACK appropriately'''
    stop_pyo_server(pyo_server)
    time.sleep(1)
    jackserver.kill_jack_server(jack_id)
    sys.exit(0)

def main():
    '''Main method. Inits gpio, bridge, jack, and pyo. Then reads effects and starts handling gpio'''
    # If GPIO is enabled, initialize the pins and GPIO module.
    if GPIO_CAPABLE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(button_pin, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(23, GPIO.OUT)

        gpio_controller = gpiocontrol.GpioController()

    # Initialize the bridge to allow the app to accept connections.
    bridge_conn = bridge.Bridge()

    # Set up custom options for the sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP SOCKET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP SOCKET
    s.setblocking(0)
    sock.setblocking(0)
    s.bind(('', 10000))
    sock.bind(('', 10001))

    jack_id = jackserver.start_jack_server()

    # give the application time for JACK to boot.
    time.sleep(5)

    # JACK and Pyo set up procedures
    pyo_server = start_pyo_server()
    pyo_server.setJackAuto()

    # Read input from the audio device on channel 0
    # and apply the necessary effects from the config file 
    enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())
    apply_effects( enabled_effects )

    # Create necessary variables used by the GPIO controller module
    record_table = []
    audio_recorder = []
    loop = []
    record_table.append(pyo.NewTable(length=60, chnls=1, feedback=0.5))
    audio_recorder.append(pyo.TableRec((enabled_effects[len(enabled_effects) - 1]), table=record_table[-1], fadetime=0.05))
    already_recording = False
    recording_time = 0
    inactive_end_time = 0
    signal.signal(signal.SIGINT, partial(signal_handler, jack_id, pyo_server))

    while True:
        # Executes GPIO and loop machine logic flow.
        if GPIO_CAPABLE:
            # Read the state of the button press. 
            BUTTON_STATE = gpio_controller.update_gpio()
            # Perform actions dependent on the state of the button press.
            if BUTTON_STATE == 'INACTIVE' or BUTTON_STATE == 'LOOPING':
                inactive_end_time = time.time()
            if BUTTON_STATE == 'RECORDING':
                recording_time = time.time()
                if not already_recording:
                    print("Recording audios for 5 segundos")
                    (audio_recorder[-1]).play()
                    already_recording = True
            elif BUTTON_STATE == 'ACTIVATE_LOOP':
                loop_len = recording_time - inactive_end_time
                loop.append(
                    pyo.Looper(
                        table=record_table[-1],
                        dur=loop_len, xfade=0,
                        mul=1).out()
                    )
                record_table.append(
                    pyo.NewTable(
                        length=60,
                        chnls=1,
                        feedback=0.5)
                    )
                audio_recorder.append(
                    pyo.TableRec(
                        (enabled_effects[len(enabled_effects) - 1]),
                        table=record_table[-1],
                        fadetime=0.05)
                    )
                print("ACTIVATING LOOP")
                gpio_controller.set_state("LOOPING")
                already_recording = False
            elif BUTTON_STATE == 'CLEAR_LOOP':
                loop = []
                record_table = []
                audio_recorder = []
                record_table.append(
                    pyo.NewTable(
                        length=60,
                        chnls=1,
                        feedback=0.5)
                    )
                audio_recorder.append(
                    pyo.TableRec(
                        (enabled_effects[len(enabled_effects) - 1]),
                        table=record_table[-1],
                        fadetime=0.05)
                    )
                gpio_controller.set_state("INACTIVE")

        # See if we got a message from the frontend application
        res = bridge_conn.backend(s,sock)
        if res:
            print(res)
            if 'UPDATEPORT' == res[0]:
                # There was a request to update the ports. Kill the
                # JACK server and restart it with the new ports.
                print("Request to update ports")
                pyo_server.shutdown()
                jackserver.kill_jack_server(jack_id)
                time.sleep(2)
                jack_id = jackserver.start_jack_server(jackserver.filter_port_selection(res[1]), jackserver.filter_port_selection(res[2]))
                time.sleep(2)
                pyo_server.reinit(**PYO_INIT_SETTINGS)
                pyo_server.boot()
                pyo_server.start()
            enabled_effects[-1].stop()
            enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())
            apply_effects( enabled_effects )
        time.sleep(0.0001)


if __name__ == "__main__":
    main()
