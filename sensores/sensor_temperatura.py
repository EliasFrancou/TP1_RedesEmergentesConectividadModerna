import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    temp = round(random.uniform(20, 30), 2)
    client.publish("casa/temperatura", temp)
    print("Temperatura:", temp)
    time.sleep(5)