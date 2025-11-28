// WORK FLOW
/*
arm and hand image from website -> python (local) -> plot arm and play game normally
                                         |
                                         ----> another python file to get data and process whether arm or hand trying to move -> control exo to move arm and hand (mqtt local wifi)
*/

#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// ---------- PCA9685 ----------
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN 90
#define SERVOMAX 560

// ---------- WiFi (NOT USED, but kept if needed later) ----------
const char* ssid = "winkawin2552";
const char* password = "winkawin2552";


// ---------- Servo Joint pins  ----------
#define finger_joint  0
#define hand_left_joint 2
#define hand_right_joint  1
#define elbow_joint  3

// ---------- Servo function ----------
void setServoAngle(int channel, int angle, bool left = true, int delayMs = 50, int step = 2) {
  static int currentAngle[16] = {0};   // stores last angle of each servo

  // Skip elbow > 90°
  if ((channel == elbow_joint) && (angle > 90)) {
    return;
  }

  if (!left) {
    angle = 180 - angle;
  }               

  if (currentAngle[channel] < angle) {
    for (int a = currentAngle[channel]; a <= angle; a += step) {
      int pulse = map(a, 0, 180, SERVOMIN, SERVOMAX);
      pwm.setPWM(channel, 0, pulse);
      delay(delayMs);
    }
  } else {
    for (int a = currentAngle[channel]; a >= angle; a -= step) {
      int pulse = map(a, 0, 180, SERVOMIN, SERVOMAX);
      pwm.setPWM(channel, 0, pulse);
      delay(delayMs);
    }
  }

  currentAngle[channel] = angle;
}


// ---------- Setup ----------
void setup() {
  Serial.begin(115200);

  Wire.begin();      // SDA, SCL
  pwm.begin();
  pwm.setPWMFreq(50);
  setServoAngle(finger_joint, 20);

  Serial.println("PCA9685 servo test (no MQTT)");
}


// // ---------- Loop ----------
void loop() {
  // Example test for servo on channel 0
  Serial.println("Servo 0 -> 0°");
  // setServoAngle(hand_left_joint, 0);
  // setServoAngle(hand_right_joint, 0, false);
  setServoAngle(elbow_joint, 0,true,30);
  delay(500);

  Serial.println("Servo 0 -> 90°");
  // setServoAngle(hand_left_joint, 90);
  // setServoAngle(hand_right_joint, 90, false);
  setServoAngle(elbow_joint, 90, true,30);
  delay(500);

  // Serial.println("Servo 0 -> 180°");
  // setServoAngle(hand_left_joint, 180);
  // setServoAngle(hand_right_joint, 180, false);
  // setServoAngle(elbow_joint, 180);
  // delay(1500);
}
