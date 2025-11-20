import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #=========== POSE (แขน ไหล่ ศอก ข้อมือ) ===========
    pose_result = pose.process(rgb)

    if pose_result.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            pose_result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # ตัวอย่าง: อ่านจุด landmark แขนขวา
        R_shoulder = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        R_elbow    = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        R_wrist    = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

        print("Right Wrist:", R_wrist.x, R_wrist.y)


    #=========== HANDS (มือ + นิ้ว 21 จุด) ===========
    hands_result = hands.process(rgb)

    if hands_result.multi_hand_landmarks:
        for hand_landmarks in hands_result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # ตัวอย่าง: อ่านปลายนิ้วชี้
            index_tip = hand_landmarks.landmark[8]  # landmark 8 = นิ้วชี้ปลาย
            print("Index Tip:", index_tip.x, index_tip.y)


    cv2.imshow("Arm + Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
