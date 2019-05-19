import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
	print(str(msg))

client = mqtt.Client("")

client.on_message = on_message

client.connect("localhost", 1883, 60)

client.subscribe("pdp/#")

try:
	client.loop_forever()
except KeyboardInterrupt:
	client.disconnect()
	print("disconnected")
