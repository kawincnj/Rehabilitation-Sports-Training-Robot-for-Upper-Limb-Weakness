import cv2 as cv
import mediapipe as mp
from motion_detect import HandMotionDetector

# --- SETUP ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils
cap = cv.VideoCapture(0)

# *** INSTANTIATE THE CLASS HERE ***
detector = HandMotionDetector(smoothing=0.2, xy_threshold=50, z_threshold=40)

while cap.isOpened():
    success, frame = cap.read()
    if not success: continue

    # Flip and prepare frame
    frame = cv.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # *** USE THE CLASS ***
            # We pass width/height because Landmarks are normalized (0.0 - 1.0)
            data = detector.process(hand_landmarks, w, h)

            # Extract data for display
            vel = data["velocity"]
            txt = data["states"]
            col = data["colors"]
            wrist = data["wrist_coor"]

            # --- DRAWING UI ---
            cv.putText(frame, f"X: {int(vel[0])} | {txt[0]}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, col[0], 2)
            cv.putText(frame, f"Y: {int(vel[1])} | {txt[1]}", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 0.7, col[1], 2)
            cv.putText(frame, f"Z: {int(vel[2])} | {txt[2]}", (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.7, col[2], 2)

            # Draw visual feedback for Push/Pull
            if txt[2] == "PUSHING":
                cv.circle(frame, (wrist[0], wrist[1]), 30, col[2], 4)
            elif txt[2] == "PULLING":
                cv.circle(frame, (wrist[0], wrist[1]), 10, col[2], -1)
    else:
        # Optional: Reset detector if no hand is found to avoid "jump" when hand returns
        detector.reset()

    cv.imshow('3D Hand Velocity', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()