#! /common/stepper.py python3

import time
from ..data.settings import config

class stepper:
	def start(self,msg):
		print("Nachricht: " + str(msg))
