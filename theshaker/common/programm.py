#! /common/programm.py

# Library Imports
import time
import json
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config

client = mqtt.Client("")
client.connect(config.BROKER,config.PORT,60)

class prg:
  def prg1(self,msg):
    client.publish("pdp/stepper", json.dumps({ "mode": "calibrate" })
    client.publish("pdp/kamera", json.dumps({ "mode": "calibrate" })
    client.publish("pdp/stepper", json.dumps({ "mode": "move", "dir": "cw", "steps": 40 })
    client.publish("pdp/kamera", json.dumps({ "mode": "compare" })
    print("fertig")
