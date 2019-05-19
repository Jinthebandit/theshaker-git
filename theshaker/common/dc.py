#! /common/dc.py python3

# Library Imports
import time
import piplates.MOTORplate as MOTOR
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config

class dc:
  def start(self,msg):
    print("start dc")
