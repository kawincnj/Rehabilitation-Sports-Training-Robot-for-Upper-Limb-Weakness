import paho.mqtt.client as mqtt
import time

# ---- Local Mosquitto Broker ----
broker = "10.50.102.43"   # Your Ubuntu IP
port = 1883
topic = "servo/control"

# Create MQTT client (no username/password)
client = mqtt.Client()

# Connect to local Mosquitto
client.connect(broker, port)

# Publish every second
while True:
    message = "0:90"     # Example: move servo channel 0 to 90°
    client.publish(topic, message)
    print(f"Published: {message}")
    time.sleep(1)
