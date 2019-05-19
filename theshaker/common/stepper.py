#! /common/stepper.py python3

# Library Imports
import time
import piplates.MOTORplate as MOTOR

# Local Imports
from ..data.settings import config

def endstop(flag):
	while(flag):
		stat=MOTOR.getSENSORS(config.ADDR)
		if not (stat & 0x1):
			flag = 0
			
def wait(flag):
	while(flag):
		stat = MOTOR.getINTflag0(config.ADDR)
		if (stat & 0x20):
			flag = 0
			
def off():
	wait(1)
	MOTOR.stepperOFF(config.ADDR,config.MOTOR)

class stepper:
	def calibrate(self,msg):
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		MOTOR.stepperOFF(config.ADDR,config.MOTOR)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"ccw","M8",500,0)
		MOTOR.stepperJOG(config.ADDR,config.MOTOR)
		endstop(1)
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		
		MOTOR.enablestepSTOPint(config.ADDR,config.MOTOR)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"cw","M8",1000,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,300)
		wait(1)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"ccw","M8",800,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,200)
		off()
		
