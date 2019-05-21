#! /common/programm.py

# Library Imports
import time
import paho.mqtt.client as mqtt

# Local Imports
from .stepper import stepper
from .kamera import kamera
from .dc import dc
from ..data.settings import config

client = mqtt.Client('')
client.connect(config.BROKER, config.PORT, 60)

class prg:
    def __init__(self):
        print('Programme')

    def prg2(self, msg):
        stepper().calibrate(1)
        kamera().calibrate(1)

        time.sleep(1)

        dc().start({'motor': 3, 'speed': 45, 'dir': 'cw', 'acc': 1})
        time.sleep(5)
        dc().stop({'motor': 3})

        time.sleep(2)

        stepper().calibrate(1)
        kamera().compare(1)

        if load <= 95:
            print('mehr Steine: {}'.format(load))
            return prg().prg2(msg)
        else:
            print(load)
            stepper().off(1)
            client.publish("pdp/finished", True)
