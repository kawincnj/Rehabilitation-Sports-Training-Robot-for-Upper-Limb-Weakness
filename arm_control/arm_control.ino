#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN 90
#define SERVOMAX 560

// Servo joint IDs
#define finger_joint  0
#define hand_left_joint 2
#define hand_right_joint 1
#define elbow_joint 3

// ---- ASYNC SERVO STRUCT ----
struct ServoMotor {
  int channel;
  int currentAngle;
  int targetAngle;
  bool left;
};

ServoMotor servos[4] = {
  {finger_joint,     0, 0, true},
  {hand_left_joint,  0, 0, true},
  {hand_right_joint, 0, 0, false},
  {elbow_joint,      0, 0, true}
};

// ---- NON-BLOCKING SETTINGS ----
unsigned long lastUpdate = 0;
const int updateInterval = 30;   // ms between each step (speed)
const int angleStep = 2;         // degrees per update

// ========== MAP ANGLE TO PULSE ==========
int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

// ========== SET TARGET ANGLE (ASYNC) ==========
void moveServoAsync(int channel, int angle) {
  for (int i = 0; i < 4; i++) {
    if (servos[i].channel == channel) {

      if (!servos[i].left) angle = 180 - angle;
      if (channel == elbow_joint && angle > 90) return;  // limit elbow

      servos[i].targetAngle = angle;
    }
  }
}

// ========== MAIN ASYNC SERVO UPDATER ==========
void updateServos() {
  unsigned long now = millis();
  if (now - lastUpdate < updateInterval) return;
  lastUpdate = now;

  for (int i = 0; i < 4; i++) {
    ServoMotor &s = servos[i];

    if (s.currentAngle == s.targetAngle) continue;

    if (s.currentAngle < s.targetAngle)
      s.currentAngle += angleStep;
    else
      s.currentAngle -= angleStep;

    int pulse = angleToPulse(s.currentAngle);
    pwm.setPWM(s.channel, 0, pulse);
  }
}

// ===================== SETUP ======================
void setup() {
  Serial.begin(115200);
  Wire.begin();

  pwm.begin();
  pwm.setPWMFreq(50);

  // initial positions
  moveServoAsync(finger_joint, 20);
  moveServoAsync(hand_right_joint, 110);
  moveServoAsync(hand_left_joint, 100);

  Serial.println("Async PCA9685 servo control is running!");
}

// ===================== LOOP ======================
void loop() {
  updateServos();

  // Example demo motion: elbow + hand movement
  static unsigned long timer = 0;
  static bool toggle = false;

  if (millis() - timer > 1500) {
    timer = millis();
    toggle = !toggle;

    if (toggle) {
      moveServoAsync(elbow_joint, 90);
      moveServoAsync(hand_right_joint, 110);
      moveServoAsync(hand_left_joint, 100);
    }
    else {
      moveServoAsync(elbow_joint, 0);
      moveServoAsync(hand_right_joint, 110 - 20); // 70
      moveServoAsync(hand_left_joint, 100 - 20);  // 60
    }
  }
}
