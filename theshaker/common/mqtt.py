#! /common/mqtt.py python3

# Standard Library Imports
import json
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config
from .stepper import stepper
from .kamera import kamera
from .dc import dc
from .programm import prg

print('test')


# ---- MQTT functions ----

# Message upon connection with MQTT broker
def on_connect(client, userdata, flags, rc):
    print('test3')
    print('Verbunden als: {}'.format(str(client)))
    print('\nFlags: {}'.format(str(flags)))
    print('Result Code: {}'.format(str(rc)))

    client.subscribe(str(config.CHANNEL + '/#'))  # Subscribe to all topics in "pdp" channel
    print('Abonnierter Kanal: {}'.format(config.CHANNEL))


# On new message in "pdp" channel
def on_message(msg):
    m_decode = str(msg.payload.decode('utf-8', 'ignore'))  # Decode msg.payload
    message = json.loads(m_decode)

    my_string = str(msg.topic)
    channel, topic = my_string.split('/', 1)

    if topic in config.TOPICS:
        getattr(globals()[topic](), message['mode'])(message)  # Execute topic.mode(payload)


# Establish connection with MQTT broker and listen
def connect():
    print('test2: {}'.format(config.BROKER))
    # Connect to MQTT broker
    client = mqtt.Client(' ')

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.BROKER, config.PORT, 60)

    # Listen on MQTT protocol in endless loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        print('MQTT disconnected')
# ---- /MQTT functions -----
