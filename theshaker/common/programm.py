#! /common/programm.py

# Library Imports
import time
import paho.mqtt.client as mqtt

# Local Imports
from .stepper import stepper
from .kamera import kamera
from .servo import servo
from .dc import dc
from ..data.settings import config

client = mqtt.Client('')
client.connect(config.BROKER, config.PORT, 60)

class prg:
    def __init__(self):
        pass

    def start(self, msg):
        stepper().calibrate(1)
        kamera().calibrate(1)

        time.sleep(1)
        prg().recursive(0)

    def stop(self, msg):
        dc().stop({'motor': 3})
        dc().stop({'motor': 4})
        stepper().off(1)

    def pause(self, msg):
        dc().stop({'motor': 3})
        dc().stop({'motor': 4})

    def resume(self, msg):
        prg().recursive(0)

    def recursive(self, load):
        if load >= 80:
            sleep = 2
        else:
            sleep = 8

        dc().stop({"motor": 4})
        servo().neutral(1)
        dc().start({'motor': 3, 'speed': 45, 'dir': 'cw', 'acc': 1})
        dc().start({'motor': 4, 'speed': 53, 'dir': 'cw', 'acc': 1})
        time.sleep(sleep)
        dc().speed({'motor': 4, 'speed': 20})
        servo().up(1)
        time.sleep(5)
        dc().stop({'motor': 3})

        time.sleep(2)

        stepper().calibrate(1)
        load = kamera().compare(1)

        if load <= 92:
            prg().recursive(load)
        else:
            stepper().neutral(1)
            stepper().off(1)
            time.sleep(0.5)
            client.publish("pdp/finished", 'Das Programm wurde erfolgreich beendet.')
