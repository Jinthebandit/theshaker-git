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
    def prg1(self,msg):
        client.publish("pdp/stepper", json.dumps({ "mode": "calibrate" }))
        time.sleep(1)
        client.publish("pdp/kamera", json.dumps({ "mode": "calibrate" }))
        time.sleep(0.5)
        client.publish("pdp/stepper", json.dumps({ "mode": "move", "dir": "cw", "steps": 40 }))
        time.sleep(0.5)
        client.publish("pdp/kamera", json.dumps({ "mode": "compare" }))

    def prg2(self,msg):
        print("prg2")
        try:
            stepper.calibrate(" ",1)
        except Exception as e:
            print(e)
        print("continue")
        kamera.calibrate()
        time.sleep(5)
        kamera.compare()
        time.sleep(5)
        stepper.move(json.dumps({ "dir": "cw", "steps": 40 }))
        kamera.compare()
        time.sleep(5)
        stepper.off()
