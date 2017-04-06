from pyo import *

class Flanger(PyoObject):
    def __init__(self, input, depth=0.5, freq=0.25, feedback=0.5, mul=1, add=0):
        PyoObject.__init__(self)
        self._input = input
        self._depth = depth
        self._freq = freq
        self._feedback = feedback
        self._fader = InputFader(input)
        fader, lmax = convertArgsToLists(self._fader)
        self._modamp = Sig(depth, mul=0.01)
        self._mod = Sine(freq=freq, mul=self._modamp, add=0.01)
        self._dls = Delay(fader, delay=self._mod, feedback=feedback)
        self._flanger = Interp(fader, self._dls, mul=mul, add=add)
        self._base_objs = self._flanger.getBaseObjects()

    def play(self, dur=0, delay=0):
        self._modamp.play(dur, delay)
        self._mod.play(dur, delay)
        self._dls.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self):
        self._modamp.stop()
        self._mod.stop()
        self._dls.stop()
        return PyoObject.stop(self)
	
