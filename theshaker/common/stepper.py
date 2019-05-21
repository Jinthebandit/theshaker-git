#! /common/stepper.py python3

# Library Imports
import piplates.MOTORplate as MOTOR
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config


# Endstop function: stop stepper when endstop is reached
def endstop(flag):
    while flag:
        stat = MOTOR.getSENSORS(config.ADDR)
        if not (stat & 0x1):
            flag = 0
    MOTOR.stepperSTOP(config.ADDR, config.MOTOR)


# Wait for stepper to reach driving speed
def wait(flag):
    MOTOR.enablestepSTOPint(config.ADDR, config.MOTOR)
    while flag:
        stat = MOTOR.getINTflag0(config.ADDR)
        if stat & 0x20:
            flag = 0


class stepper:
    # Calibrate stepper by driving it to the endstop and then into a neutral position
    def calibrate(self, msg):
        MOTOR.stepperSTOP(config.ADDR, config.MOTOR)
        MOTOR.stepperCONFIG(config.ADDR, config.MOTOR, "ccw", "M8", 500, 0)
        MOTOR.stepperJOG(config.ADDR, config.MOTOR)
        endstop(1)
        MOTOR.stepperCONFIG(config.ADDR, config.MOTOR, "cw", "M8", 1000, 0)
        MOTOR.stepperMOVE(config.ADDR, config.MOTOR, 300)
        wait(1)
        MOTOR.stepperCONFIG(config.ADDR, config.MOTOR, "ccw", "M8", 800, 0)
        MOTOR.stepperMOVE(config.ADDR, config.MOTOR, 200)
        wait(1)

        # Send MQTT message: stepper calibration finished.
        client = mqtt.Client("")
        client.connect(config.BROKER, config.PORT, 60)
        client.publish("pdp/status", "Stepper Kalibrierung abgeschlossen.")

    # Move stepper a number of steps
    def move(self, msg):
        MOTOR.stepperSTOP(config.ADDR, config.MOTOR)
        MOTOR.stepperCONFIG(config.ADDR, config.MOTOR, msg["dir"], config.RES, config.SPEED, 0)
        MOTOR.stepperMOVE(config.ADDR, config.MOTOR, msg["steps"])
        wait(1)

    def neutral(self, msg):
        MOTOR.stepperSTOP(config.ADDR, config.MOTOR)
        MOTOR.stepperCONFIG(config.ADDR, config.MOTOR, "ccw", "M8", 500, 0)
        MOTOR.stepperJOG(config.ADDR, config.MOTOR)
        endstop(1)
        MOTOR.stepperCONFIG(config.ADDR, config.MOTOR, "cw", "M8", 1000, 0)
        MOTOR.stepperMOVE(config.ADDR, config.MOTOR, 300)
        wait(1)

    # Stop and turn off stepper
    def off(self, msg):
        MOTOR.stepperSTOP(config.ADDR, config.MOTOR)
        MOTOR.stepperOFF(config.ADDR, config.MOTOR)

        # Send MQTT message: stepper is turned off
        client = mqtt.Client("")
        client.connect(config.BROKER, config.PORT, 60)
        client.publish("pdp/status", "Stepper ist abgestellt.")
