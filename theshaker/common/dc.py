#! /common/dc.py python3

# Library Imports
import time
import piplates.MOTORplate as MOTOR
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config

class dc:
    def __init__(self):
        pass

    def start(self, msg):
        MOTOR.dcCONFIG(config.ADDR, msg['motor'], msg['dir'], msg['speed'], msg['acc'])
        MOTOR.dcSTART(config.ADDR, msg['motor'])

    def stop(self, msg):
        MOTOR.dcSTOP(config.ADDR, msg['motor'])

    def speed(self, msg):
        MOTOR.dcSPEED(config.ADDR, msg['motor'], msg['speed'])