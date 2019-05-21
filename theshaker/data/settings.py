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
