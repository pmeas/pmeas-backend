import time

import RPi.GPIO as GPIO

class GpioController:
    """
    GPIO Controller module that keeps track of the state of
    the button and other pins on the Raspberry device (if it 
    is being used). Changes the respective states and sends the
    new states to the main program.

    button_pressed -- Whether or not the button is being pressed
    BUTTON_STATE -- the current state of the loop machine. Valid states:
                    INACTIVE: Loop Machine is not being used
                    RECORDING: Recording the audio being played
                    ACTIVATE_LOOP: Stop recording and begin loop playback
                    LOOPING: Playing back the loop
                    CLEAR_LOOP: Initiate end to playback of loop
    last_pressed -- When the button was last pressed.
    time_pressed -- How long the button has been pressed for.
    button_held -- If the button has been held for 3 seconds (indicating clear of loop intent)
    """

    def __init__(self):
        self.button_pressed = False
        self.BUTTON_STATE = 'INACTIVE'
        self.last_pressed = 0
        self.time_pressed = 0
        self.button_held = False

    def update_gpio(self):
    """
    Update the state of the loop machine based on whether or not the
    button is being pressed.

    Return the state of the loop machine as BUTTON_STATE
    """
        pin_state = GPIO.input(17)

        # If the button is being pressed, set the pressed variable and
        # update the time in which it was last pressed.
        if pin_state == GPIO.LOW:
            self.time_pressed = time.time() - self.last_pressed

            if not self.button_pressed:
                self.button_pressed = True

        # If the button is not pressed, determine if it was previously
        # pressed to update the loop machine state. If not, update the
        # time in which it was last pressed.
        if pin_state == GPIO.HIGH:
            self.last_pressed = time.time()
            if self.button_held:
                self.button_held = False
                self.button_pressed = False

            if self.button_pressed and not self.button_held:
                self.change_state()
                self.button_pressed = False

        # If the button is held for 3 seconds, inititate the stop loop
        # machine process.
        if self.BUTTON_STATE == 'LOOPING' and (self.time_pressed >= 3):
            self.time_pressed = 0
            self.button_held = True
            self.BUTTON_STATE = 'CLEAR_LOOP'
        
        return self.BUTTON_STATE

    def change_state(self):
        """Change the state of the loop machine dependent on before state"""
        if self.BUTTON_STATE == 'INACTIVE':
            self.BUTTON_STATE = 'RECORDING'
        elif self.BUTTON_STATE == 'RECORDING':
            self.BUTTON_STATE = 'ACTIVATE_LOOP'
        elif self.BUTTON_STATE == 'ACTIVATE_LOOP':
            self.BUTTON_STATE = 'LOOPING'
        return self.BUTTON_STATE

    def set_state(self, new_state):
        """Set the state of the loop machine"""
        self.BUTTON_STATE = new_state
