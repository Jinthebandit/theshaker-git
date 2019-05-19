#! /Projects/mqtt.py python3
#! config.py muss im selben Verzeichnis sein

# Standard Library Imports
import time
import json
import paho.mqtt.client as mqtt

# Local Imports
import config
from stepper import *
from kamera import *

# ---- MQTT Funktionen BEGINN ----

 # Nachricht bei erfolgreicher Verbindung mit MQTT Broker
def on_connect(client, userdata, flags, rc):
	print("Verbunden als: " + str(client) + "\nFlags: " + str(flags) + " und Result Code: " + str(rc))

	client.subscribe(str(config.CHANNEL + "/#")) # Alle Topics von config.CHANNEL abonnieren
	print("Abonnierter Kanal: " + config.CHANNEL)

 # Bei neuer Nachricht in config.CHANNEL:
def on_message(client, userdata, msg):
	m_decode = str(msg.payload.decode("utf-8", "ignore")) # msg.payload dekodieren
	message = json.loads(m_decode)

	myString = str(msg.topic)
	channel, topic = myString.split("/", 1)

	if topic in config.TOPICS:
		try:
			getattr(globals()[topic](), message["mode"])(message) # topic.mode(payload) ausfuehren
		except AttributeError:
			print("Attribute Error")

# MQTT Verbindung als Client mit Broker herstellen
client = mqtt.Client("")

client.on_connect = on_connect
client.on_message = on_message

client.connect(config.BROKER, config.PORT, 60)

try:
	client.loop_forever()
except KeyboardInterrupt:
	client.disconnect()
	print("MQTT disconnected")

# ---- MQTT Funktionen ENDE -----