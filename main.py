import pyo
import time
import configparser

effect_one = None
effect_two = None

# Start the server necessary for Pyo to get audio streams from JACK
s = pyo.Server(audio='jack', nchnls=1).boot()
s.start()

enabled_effects = []

# Read input from the audio device on channel 1
enabled_effects.append(pyo.Input(chnl=0))

effects_dict = configparser.get_effects()
for effect in effects_dict.keys():
    #print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
    if effect == 'distortion':
        #distortion stuff
        print("Enable distortion effect")
        enabled_effects.append(pyo.Disto(enabled_effects[len(enabled_effects)-1], drive=0.75, slope=0.5, mul=1, add=0))
    elif effect == 'delay':
        #delay stuff
        print("Enable delay effect")
        enabled_effects.append(pyo.Delay(enabled_effects[len(enabled_effects)-1], delay=.25, feedback=0.5, mul=0.5))
    elif effect == 'reverb':
        #reverb stuff
        print("Enable reverb effect")
        # there's a TON of reverb effects in Pyo. Gotta find out which one is the right to implement.
        enabled_effects.append(pyo.Freeverb(enabled_effects[len(enabled_effects)-1], size=0.5, damp=0.5, bal=0.5, mul=1, add=0))
    elif effect == 'chorus':
        #chorus stuff
        print("Enable chorus effect")
        enabled_effects.append(pyo.Chorus(enabled_effects[len(enabled_effects)-1], depth=1, feedback=0.25, bal=0.5, mul=1, add=0))
    elif effect == 'freqshift':
        #frequency shift stuff
        print("Enable frequency shift effect")
        enabled_effects.append(pyo.FreqShift(enabled_effects[len(enabled_effects)-1], shift=100, mul=1, add=0))
    elif effect == 'harmonizer':
        #harmonizer stuff
        print("Enable harmonizer effect")
        enabled_effects.append(pyo.Harmonizer(enabled_effects[len(enabled_effects)-1], transpo=-7.0, feedback=0, winsize=0.1, mul=1, add=0))

enabled_effects[len(enabled_effects)-1].out()

#audioIn.out()

# Eliminate need for GUI with loop - eventually to be used for updating effects.
while True:
    time.sleep(1)


