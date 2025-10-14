import paho.mqtt.client as mqtt

# ---- HiveMQ Cloud Broker ----
broker = "1da2e234bf424783bc46e915d899b1b8.s1.eu.hivemq.cloud"
port = 8883  # TLS port
username = "esp32_winkawin2552"
password = "K12042009k"
topic = "/test/winkawin"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

# Create MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()  # Use TLS

client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
client.connect(broker, port)

# Blocking loop to keep the script running and listening
client.loop_forever()
