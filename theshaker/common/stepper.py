#! /common/stepper.py python3

# Library Imports
import time
import piplates.MOTORplate as MOTOR
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config

# Funktion fuer Endstop: wenn Endstop erreicht -> Motor stoppen
def endstop(flag):
	while(flag):
		stat=MOTOR.getSENSORS(config.ADDR)
		if not (stat & 0x1):
			flag = 0
	MOTOR.stepperSTOP(config.ADDR,config.MOTOR)

# Warten bis der Motor seine endgueltige Geschwindigkeit erreicht hat
def wait(flag):
	MOTOR.enablestepSTOPint(config.ADDR,config.MOTOR)
	while(flag):
		stat = MOTOR.getINTflag0(config.ADDR)
		if (stat & 0x20):
			flag = 0

class stepper:
	# Stepper mit Hilfe des Endstops kalibrieren und in neutrale Position fahren.
	def calibrate(self,msg):
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"ccw","M8",500,0)
		MOTOR.stepperJOG(config.ADDR,config.MOTOR)
		endstop(1)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"cw","M8",1000,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,300)
		wait(1)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,"ccw","M8",800,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,200)
		wait(1)
		
		# MQTT Nachricht senden: Stepper Kalibrierung abgeschlossen
		client = mqtt.Client("")
		client.connect(config.BROKER,config.PORT,60)
		client.publish("pdp/status", "Stepper Kalibrierung abgeschlossen.")

	# Stepper eine Anzahl an Steps bewegen
	def move(self,msg):
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		MOTOR.stepperCONFIG(config.ADDR,config.MOTOR,msg["dir"],config.RES,config.SPEED,0)
		MOTOR.stepperMOVE(config.ADDR,config.MOTOR,msg["steps"])
		wait(1)

	# Motor stoppen und dann abstellen
	def off(self,msg):
		MOTOR.stepperSTOP(config.ADDR,config.MOTOR)
		MOTOR.stepperOFF(config.ADDR,config.MOTOR)

		# MQTT Nachricht senden: Stepper Kalibrierung abgeschlossen
		client = mqtt.Client("")
		client.connect(config.BROKER,config.PORT,60)
		client.publish("pdp/status", "Stepper ist abgestellt.")
