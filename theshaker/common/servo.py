#! /commong/servo.py python3

# Library Imports
import time
from pigpio import pi

# Local Imports
from ..data.settings import config

class servo:
    def __init__(self):
        pass

    def up(self, msg):
        print('up')
        pi().set_servo_pulsewidth(config.SERVO_PIN, config.SERVO_UP)
        pi().stop()

    def neutral(self, msg):
        print('neutral')
        pi().set_servo_pulsewidth(config.SERVO_PIN, config.SERVO_NEUTRAL)
        pi().stop()
