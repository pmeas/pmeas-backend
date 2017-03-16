import time

import RPi.GPIO as GPIO

class GpioController:

    def __init__(self):
        self.button_pressed = False
        self.BUTTON_STATE = 'INACTIVE'
        self.last_pressed = 0
        self.time_pressed = 0

    def update_gpio(self):
        pin_state = GPIO.input(17)
        if pin_state == GPIO.LOW:
            self.time_pressed = time.time() - self.last_pressed

        if not self.button_pressed and pin_state == GPIO.LOW:
            self.button_pressed = True

        if pin_state == GPIO.HIGH:
            self.last_pressed = time.time()

        if self.button_pressed and (pin_state == GPIO.HIGH):
            self.change_state()
            self.button_pressed = False

        # do a check here to see if previous button_state
        # is LOOPING so we can set it to clear_loop ONLY
        # in that instance!
        if self.BUTTON_STATE == 'LOOPING' and (self.time_pressed >= 3):
            self.time_pressed = 0
            self.BUTTON_STATE = 'CLEAR_LOOP'
        
        return self.BUTTON_STATE

    def change_state(self):
        if self.BUTTON_STATE == 'INACTIVE':
            self.BUTTON_STATE = 'RECORDING'
        elif self.BUTTON_STATE == 'RECORDING':
            self.BUTTON_STATE = 'ACTIVATE_LOOP'
        elif self.BUTTON_STATE == 'ACTIVATE_LOOP':
            self.BUTTON_STATE = 'LOOPING'
        return self.BUTTON_STATE

    def set_state(self, new_state):
        self.BUTTON_STATE = new_state
