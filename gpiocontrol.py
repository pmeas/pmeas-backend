import time

import RPi.GPIO as GPIO

class GpioController:

    def __init__(self):
        this.button_pressed = False
        this.BUTTON_STATE = 'INACTIVE'

    def update_gpio(self):
        pin_state = GPIO.input(17)
        if not this.button_pressed and pin_state == GPIO.LOW:
            this.button_pressed = True
        if this.button_pressed and (pin_state == GPIO.HIGH):
            change_state()
            this.button_pressed = False
        #else held for 3 seconds here
        return this.BUTTON_STATE

    def change_state():
        if this.BUTTON_STATE == 'INACTIVE':
            this.BUTTON_STATE = 'RECORDING'
        elif this.BUTTON_STATE == 'RECORDING':
            this.BUTTON_STATE = 'LOOPING'
        return this.BUTTON_STATE

