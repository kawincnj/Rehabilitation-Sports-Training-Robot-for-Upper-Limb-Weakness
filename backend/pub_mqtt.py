import paho.mqtt.client as mqtt

# ---- HiveMQ Cloud Broker ----
broker = "1da2e234bf424783bc46e915d899b1b8.s1.eu.hivemq.cloud"
port = 8883  # TLS port
username = "esp32_winkawin2552"
password = "K12042009k"
topic = "/test/winkawin"

# Create MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()  # Use TLS

client.connect(broker, port)

# Publish messages every 5 seconds
import time
while True:
    message = "Hello from Python!"
    client.publish(topic, message)
    print(f"Published: {message}")
    time.sleep(1)
