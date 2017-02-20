import pyo
import time
import configparser

effect_one = None
effect_two = None

# Start the server necessary for Pyo to get audio streams from JACK
s = pyo.Server(audio='jack', nchnls=1).boot()
s.start()

# Read input from the audio device on channel 1
audio_in = pyo.Input(chnl=0)

effects_dict = configparser.get_effects()
for effect in effects_dict.keys():
    #print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
    params = effects_dict[effect]
    if effect == 'distortion':
        #distortion stuff
        print("Enable distortion effect")
        if effect_one is None:
            effect_one = pyo.Disto(audio_in, drive=int(params['drive']), slope=int(params['slope']), mul=1, add=0).out()
        else:
            effect_two = pyo.Disto(effect_one, drive=int(params['drive']), slope=int(params['slope']), mul=1, add=0).out()
    elif effect == 'delay':
        #delay stuff
        print("Enable delay effect")
        if effect_one is None:
            effect_one = pyo.Delay(audio_in, delay=int(params['delay']), feedback=int(params['feedback']), mul=0.5).out()
        else:
            effect_two = pyo.Delay(effect_one, delay=int(params['delay']), feedback=int(params['feedback']), mul=0.5).out()
    elif effect == 'reverb':
        #reverb stuff
        print("Enable reverb effect")
        # there's a TON of reverb effects in Pyo. Gotta find out which one is the right to implement.
        if effect_one is None:
            effect_one = pyo.STRev(audio_in, inpos=0.25, revtime=int(params['revtime']), cutoff=int(params['cutoff']), bal=int(params['balance']), roomSize=int(params['roomsize'])).out()
        else:
            effect_two = pyo.STRev(effect_one, inpos=0.25, revtime=int(params['revtime']), cutoff=int(params['cutoff']), bal=int(params['balance']), roomSize=int(params['roomsize'])).out()
    elif effect == 'chorus':
        #chorus stuff
        print("Enable chorus effect")
        if effect_one is None:
            effect_one = pyo.Chorus(audio_in, depth=int(params['depth']), feedback=int(params['feedback']), bal=int(params['balance'], mul=1, add=0).out()
        else:
            effect_two = pyo.Chorus(effect_one, depth=int(params['depth']), feedback=int(params['feedback']), bal=int(params['balance'], mul=1, add=0).out()
    elif effect == 'freqshift':
        #frequency shift stuff
        print("Enable frequency shift effect")
        if effect_one is None:
            effect_one = pyo.FreqShift(audio_in, shift=int(params['shift']), mul=1, add=0).out()
        else:
            effect_two = pyo.FreqShift(effect_one, shift=int(params['shift']), mul=1, add=0).out()
    elif effect == 'harmonizer':
        #harmonizer stuff
        print("Enable harmonizer effect")
        if effect_one is None:
            effect_one = pyo.Harmonizer(audio_in, transpo=int(params['transpose']), feedback=int(params['feedback']), winsize=0.1, mul=1, add=0).out()
        else:
            effect_two = pyo.Harmonizer(effect_one, transpo=int(params['transpose']), feedback=int(params['feedback']), winsize=0.1, mul=1, add=0).out()
    else:
        # For invalid input just output direct audio
        if effect_one is None:
            audio_in.out()


# Eliminate need for GUI with loop - eventually to be used for updating effects.
while True:
    time.sleep(1)


