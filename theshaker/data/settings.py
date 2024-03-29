#! /data/settings.py python3


class config:
    # ---- MQTT Settings ----
    BROKER = "localhost"
    PORT = 1883
    CHANNEL = "pdp"
    TOPICS = ["stepper", "kamera", "dc", "servo", "prg"]
    # ---- /MQTT Settings ----

    # ---- PiPlates Settings ----
    ADDR = 0

    # ---- Stepper Settings ----
    MOTOR = "A"
    RES = "M8"
    SPEED = 500
    # ---- /Stepper Settings ----

    # ---- Servo Settings ----
    SERVO_PIN = 22 # Servo GPIO Pin Number
    SERVO_UP = 950
    SERVO_NEUTRAL = 1110
    # ---- /Servo Settings ----
