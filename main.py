import pyo
import time

# Start the server necessary for Pyo to get audio streams from JACK
s = pyo.Server(audio='jack', nchnls=1).boot()
s.start()

# Read input from the audio device on channel 1
audioIn = pyo.Input(chnl=0).out()

# Eliminate need for GUI with loop - eventually to be used for updating effects.
while True:
    time.sleep(1)
