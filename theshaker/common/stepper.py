#! /common/stepper.py python3

# Library Imports
import time

# Local Imports
from ..data.settings import config

class stepper:
	def start(self,msg):
		print("Nachricht: " + str(msg))
