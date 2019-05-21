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
        pi().set_servo_pulsewidth(config.SERVO_PIN, config.SERVO_UP)
        time.sleep(0.1)
        pi().stop()

    def neutral(self, msg):
        pi().set_servo_pulsewidth(config.SERVO_PIN, config.SERVO_NEUTRAL)
        time.sleep(0.1)
        pi().stop()
