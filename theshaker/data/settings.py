#! /data/config.py python3

class config:
  # ---- MQTT Settings ----
  BROKER = "localhost"
  PORT = 1883
  CHANNEL = "pdp"
  TOPICS = {"stepper": "stepper", "kamera": "kamera", "dc": "dc"}

  # ---- /MQTT Settings ----

  # ---- Stepper Settings ----
  ADDR = 0
  MOTOR = "A"
  # ---- /Stepper Settings ----
