#! /data/settings.py python3

class config:
  # ---- MQTT Settings ----
  BROKER = "localhost"
  PORT = 1883
  CHANNEL = "pdp"
  TOPICS = [ "stepper", "kamera", "dc", "servo", "prg" ]
  # ---- /MQTT Settings ----

  # ---- Stepper Settings ----
  ADDR = 0
  MOTOR = "A"
  RES = "M8"
  SPEED = 500
  # ---- /Stepper Settings ----
