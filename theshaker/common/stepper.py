#! /common/stepper.py python3

# Library Imports
import time
import piplates.MOTORplate as MOTOR
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config

# Funktion fuer Endstop: wenn Endstop erreicht -> Motor stoppen
def endstop(flag):
	print("endstop")
	while(flag):
		stat=MOTOR.getSENSORS(config.ADDR)
		if not (stat & 0x1):
			flag = 0
	Motor.stepperSTOP(config.ADDR,config.MOTOR)

# Warten bis der Motor seine endgueltige Geschwindigkeit erreicht hat
def wait(flag):
	print("wait")
	MOTOR.enablestepSTOPint(config.ADDR,config.MOTOR)
	while(flag):
		stat = MOTOR.getINTflag0(config.ADDR)
		if (stat & 0x20):
			flag = 0

class stepper:
	# Stepper mit Hilfe des Endstops kalibrieren und in neutrale Position fahren.
	def calibrate(self,msg):
		print("test")
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		wait(1)
		MOTOR.stepperOFF(config.ADDR,config.MOTOR)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"ccw","M8",500,0)
		MOTOR.stepperJOG(config.ADDR,config.MOTOR)
		endstop(1)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"cw","M8",1000,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,300)
		wait(1)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"ccw","M8",800,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,200)
		
		# MQTT Nachricht senden: Stepper Kalibrierung abgeschlossen
		client = mqtt.Client("")
		client.connect(config.BROKER,config.PORT,60)
		client.publish("pdp/status", "Stepper Kalibrierung abgeschlossen.")

	# Stepper eine Anzahl an Steps bewegen
	def move(self,msg):
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		wait(1)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,msg["dir"],config.RES,config.SPEED,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,msg["steps"])

	# Motor stoppen und dann abstellen
	def off(self):
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		wait(1)
		MOTOR.stepperOFF(config.ADDR,config.MOTOR)

		# MQTT Nachricht senden: Stepper Kalibrierung abgeschlossen
		client = mqtt.Client("")
		client.connect(config.BROKER,config.PORT,60)
		client.publish("pdp/status", "Stepper ist abgestellt.")
