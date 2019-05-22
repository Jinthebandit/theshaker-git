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


class prg:
    def __init__(self):
        pass

    def start(self, msg):
        stepper().calibrate(1)
        kamera().calibrate(1)

        time.sleep(1)
        prg().recursive(0, msg)

    def stop(self, msg):
        print("stop")
        dc().stop({'motor': 3})
        dc().stop({'motor': 4})
        stepper().off(1)

    def resume(self, msg):
        prg().recursive(0)

    def recursive(self, load, msg):
        if load >= 80:
            sleep = 2
        else:
            sleep = 8

        servo().neutral(1)
        dc().start({'motor': 3, 'speed': 45, 'dir': 'cw', 'acc': 1})
        dc().start({'motor': 4, 'speed': 53, 'dir': 'cw', 'acc': 1})
        time.sleep(sleep)
        dc().speed({'motor': 4, 'speed': 20})
        servo().up(1)
        time.sleep(5)
        dc().stop({"motor": 4})
        dc().stop({'motor': 3})

        time.sleep(2)

        stepper().calibrate(1)
        load = kamera().compare(1)

        if load < 91 & msg['pause'] is not True:
            prg().recursive(load)
        elif load >= 91 & msg['pause'] is not True:
            client1 = mqtt.Client('')
            client1.connect(config.BROKER, config.PORT, 60)
            stepper().neutral(1)
            time.sleep(0.5)
            stepper().off(1)
            client1.publish("pdp/finished", 'Das Programm wurde erfolgreich beendet.')
            client1.disconnect()
        else:
            print("paused")
