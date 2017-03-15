import time

import RPi.GPIO as GPIO

class GpioController:

    def __init__(self):
        self.button_pressed = False
        self.BUTTON_STATE = 'INACTIVE'

    def update_gpio(self):
        pin_state = GPIO.input(17)
        if not self.button_pressed and pin_state == GPIO.LOW:
            self.button_pressed = True
        if self.button_pressed and (pin_state == GPIO.HIGH):
            self.change_state()
            self.button_pressed = False
        #else held for 3 seconds here
        return self.BUTTON_STATE

    def change_state(self):
        if self.BUTTON_STATE == 'INACTIVE':
            self.BUTTON_STATE = 'RECORDING'
        elif self.BUTTON_STATE == 'RECORDING':
            self.BUTTON_STATE = 'LOOPING'
        return self.BUTTON_STATE

