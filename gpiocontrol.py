import time

import RPi.GPIO as GPIO

def update_gpio(button_pressed):
    pin_state = GPIO.input(button)
    if not button_pressed and pin_state == GPIO.LOW:
        button_pressed = True
    if button_pressed and (pin_state == GPIO.HIGH):
        change_state()
        button_pressed = False
    #else held for 3 seconds here
    return BUTTON_STATE

def change_state(BUTTON_STATE):
    if BUTTON_STATE == 'INACTIVE':
        BUTTON_STATE = 'RECORDING'
    elif BUTTON_STATE == 'RECORDING':
        BUTTON_STATE = 'LOOPING'
    return BUTTON_STATE

