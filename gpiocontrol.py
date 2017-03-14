import time

import RPi.GPIO as GPIO

BUTTON_STATE = 'INACTIVE'
pin_state = GPIO.HIGH
button = 0
button_pressed = False

def init_gpio(button_pin):
    button = button_pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(button_pin, GPIO.IN, GPIO.PUD_UP)

def update_gpio():
    pin_state = GPIO.input(button)
    if not button_pressed and pin_state == GPIO.LOW:
        button_pressed = True
    if button_pressed and (pin_state == GPIO.HIGH):
        change_state()
        button_pressed = False
    #else held for 3 seconds here
    return BUTTON_STATE

def change_state():
    if BUTTON_STATE == 'INACTIVE':
        BUTTON_STATE = 'RECORDING'
    elif BUTTON_STATE == 'RECORDING':
        BUTTON_STATE = 'LOOPING'

