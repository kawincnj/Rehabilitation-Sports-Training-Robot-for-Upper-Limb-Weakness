import paho.mqtt.client as mqtt

# ---- Local Mosquitto MQTT ----
broker = "10.50.102.43"   # Your Ubuntu IP
port = 1883
topic = "servo/control"

# Callback when connected
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to local MQTT!")
        client.subscribe(topic)
    else:
        print("Failed to connect, error code:", rc)

# Callback when message received
def on_message(client, userdata, msg):
    print(f"Received: {msg.payload.decode()} on {msg.topic}")

# Create client
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Connect (NO TLS for local broker)
client.connect(broker, port, 60)

client.loop_forever()
