#! /common/mqtt.py python3

# Standard Library Imports
import time
import json
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config
from .stepper import stepper
from .kamera import kamera
from .dc import dc

# ---- MQTT Funktionen ----

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

# Verbindung zu Broker herstellen und endlos Loop starten.
def connect():
	# MQTT Verbindung als Client mit Broker herstellen
	client = mqtt.Client("")

	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(config.BROKER, config.PORT, 60)

	# MQTT Protokoll auf Nachrichten abhoeren
	try:
		client.loop_forever()
	except KeyboardInterrupt:
		client.disconnect()
		print("MQTT disconnected")
# ---- /MQTT Funktionen -----
