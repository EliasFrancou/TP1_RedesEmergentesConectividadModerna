import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    hum = round(random.uniform(40, 70), 2)
    client.publish("casa/humedad", hum)
    print("Humedad:", hum)
    time.sleep(5)