#! /common/programm.py

# Library Imports
import time
import json
import paho.mqtt.client as mqtt

# Local Imports
from .stepper import stepper
from .kamera import kamera
from ..data.settings import config

client = mqtt.Client("")
client.connect(config.BROKER,config.PORT,60)

class prg:
    def __init__(self):
        print('Programme')

    def prg2(self, msg):
        stepper().calibrate(1)
        kamera().calibrate(1)
        time.sleep(5)
        kamera().compare(1)
        time.sleep(5)
        stepper().move({ 'dir': 'cw', 'steps': 40 })
        kamera().compare(1)
        time.sleep(5)        
        stepper().move({ "dir": 'ccw', 'steps': 40 })
        load = kamera().compare(1)
        if load <= 95:
            print('mehr Steine: {}'.format(load))
        else:
            print(load)
        stepper().off(1)