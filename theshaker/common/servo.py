#! /commong/servo.py python3

# Library Imports
import time
import pigpio

# Local Imports
from ..data.settings import config

class servo:
    def __init__(self):
        pass

    def up(self, msg):
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(config.SERVO_PIN, config.SERVO_UP)
        time.sleep(0.2)
        pi.stop()

    def neutral(self, msg):
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(config.SERVO_PIN, config.SERVO_NEUTRAL)
        time.sleep(0.2)
        pi.stop()
