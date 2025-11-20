#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// ---------- PCA9685 ----------
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN 150
#define SERVOMAX 600

// ---------- WiFi ----------
const char* ssid = "winkawin2552";
const char* password = "winkawin2552";

// ---------- MQTT ----------
const char* mqttServer = "10.50.102.43";   // <-- Your laptop IP running Mosquitto
const int mqttPort = 1883;
const char* mqttTopic = "servo/control";

WiFiClient espClient;
PubSubClient client(espClient);

// ---------- Servo function ----------
void setServoAngle(int channel, int angle) {
  int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(channel, 0, pulse);
}

// ---------- MQTT callback ----------
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("MQTT message received: ");

  String msg = "";
  for (int i = 0; i < length; i++) {
    msg += (char)message[i];
  }

  Serial.println(msg);

  // Expected format: channel:angle  (example: 0:90)
  int colonIndex = msg.indexOf(':');
  if (colonIndex > 0) {
    int channel = msg.substring(0, colonIndex).toInt();
    int angle = msg.substring(colonIndex + 1).toInt();

    Serial.printf("Moving servo %d to %d degrees\n", channel, angle);

    setServoAngle(channel, angle);
  }
}

// ---------- WiFi connection ----------
void connectWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected!");
  Serial.println(WiFi.localIP());
}

// ---------- MQTT connection ----------
void connectMQTT() {
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("nanoESP32-servo")) {
      Serial.println("Connected to MQTT!");
      client.subscribe(mqttTopic);
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// ---------- Setup ----------
void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22);
  pwm.begin();
  pwm.setPWMFreq(50);

  connectWiFi();

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
}

// ---------- Loop ----------
void loop() {
  if (!client.connected()) {
    connectMQTT();
  }

  client.loop();
}
