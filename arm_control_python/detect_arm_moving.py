import cv2 as cv
import mediapipe as mp
import time
import math

# --- CONFIGURATION ---
SMOOTHING_FACTOR = 0.2     # 0.0 to 1.0. Lower = smoother.
XY_THRESHOLD = 50          # Pixel speed threshold for X/Y
Z_THRESHOLD = 40           # "Size change" speed threshold for Z (Push/Pull)

# --- SETUP MEDIAPIPE ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

cap = cv.VideoCapture(0)

# --- STATE VARIABLES ---
prev_time = 0
prev_pos = [0, 0, 0]      # [x, y, z_proxy]
curr_velocity = [0, 0, 0] # [vx, vy, vz]

def get_finger_coor(finger, w, h, number):
    return [int(finger.landmark[number].x * w), int(finger.landmark[number].y * h)]

def calculate_distance(p1, p2):
    # Standard Pythagorean theorem to get distance between two points
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

print("Press 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Get dimensions and time
    h, w, c = frame.shape
    current_time = time.time()
    dt = current_time - prev_time 
    if dt == 0: dt = 0.001

    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # --- 1. Get Positions ---
            wrist = get_finger_coor(hand_landmarks, w, h, 0)         # Point 0
            middle_mcp = get_finger_coor(hand_landmarks, w, h, 9)    # Point 9 (Knuckle)

            # Use X and Y from wrist
            curr_x = wrist[0]
            curr_y = wrist[1]
            
            # --- THE TRICK: Calculate Z based on Hand Size ---
            # Distance between Wrist and Middle Knuckle determines "Depth"
            curr_z_proxy = calculate_distance(wrist, middle_mcp) * 2 # Multiplied for sensitivity

            curr_pos_temp = [curr_x, curr_y, curr_z_proxy]

            # --- 2. Calculate Raw Velocity ---
            # Formula: (Current - Previous) / Time
            raw_vx = (curr_pos_temp[0] - prev_pos[0]) / dt
            raw_vy = (curr_pos_temp[1] - prev_pos[1]) / dt
            raw_vz = (curr_pos_temp[2] - prev_pos[2]) / dt

            # --- 3. Apply Smoothing ---
            curr_velocity[0] = (SMOOTHING_FACTOR * raw_vx) + ((1 - SMOOTHING_FACTOR) * curr_velocity[0])
            curr_velocity[1] = (SMOOTHING_FACTOR * raw_vy) + ((1 - SMOOTHING_FACTOR) * curr_velocity[1])
            curr_velocity[2] = (SMOOTHING_FACTOR * raw_vz) + ((1 - SMOOTHING_FACTOR) * curr_velocity[2])

            # --- 4. Logic & Display ---
            # Reset text
            x_text, y_text, z_text = "---", "---", "---"
            color_x, color_y, color_z = (200,200,200), (200,200,200), (200,200,200)

            # X-Axis Logic
            if curr_velocity[0] > XY_THRESHOLD:
                x_text = "RIGHT >>"
                color_x = (0, 255, 0)
            elif curr_velocity[0] < -XY_THRESHOLD:
                x_text = "<< LEFT"
                color_x = (0, 255, 0)

            # Y-Axis Logic (Inverted: +Y is Down)
            if curr_velocity[1] > XY_THRESHOLD:
                y_text = "DOWN v"
                color_y = (0, 0, 255)
            elif curr_velocity[1] < -XY_THRESHOLD:
                y_text = "UP ^"
                color_y = (0, 0, 255)

            # Z-Axis Logic (Size Change)
            # Positive Vz = Size Growing = Moving Closer
            if curr_velocity[2] > Z_THRESHOLD:
                z_text = "PUSHING (Forward)"
                color_z = (255, 0, 255) # Magenta
                cv.circle(frame, (wrist[0], wrist[1]), 30, (255, 0, 255), 4) # Visual cues
            elif curr_velocity[2] < -Z_THRESHOLD:
                z_text = "PULLING (Backward)"
                color_z = (255, 0, 255)
                cv.circle(frame, (wrist[0], wrist[1]), 10, (255, 0, 255), -1)

            # --- 5. Draw UI ---
            cv.putText(frame, f"X Vel: {int(curr_velocity[0])} | {x_text}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, color_x, 2)
            cv.putText(frame, f"Y Vel: {int(curr_velocity[1])} | {y_text}", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 0.7, color_y, 2)
            cv.putText(frame, f"Z Vel: {int(curr_velocity[2])} | {z_text}", (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.7, color_z, 2)

            # Update history
            prev_pos = curr_pos_temp
            prev_time = current_time

    else:
        curr_velocity = [0,0,0]

    cv.imshow('3D Hand Velocity', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
hands.close()