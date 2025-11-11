import cv2 as cv
import mediapipe as mp
from tools import *
from games import *

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.35
)
mp_drawing = mp.solutions.drawing_utils

# --- Initialize Video Capture ---
cap = cv.VideoCapture(0)

# --- SET UP GAME VARIABLES ---
on_catch_ball = False
score = 0
lock_bug_score = True
lock_bug_score_squeez = False

# --- Load Image ---
football_image_path = 'backend/img/football.png'
football = cv.imread(football_image_path, cv.IMREAD_UNCHANGED)

badminton_rac_image_path = 'backend/img/badminton_rac.png'
badminton_rac = cv.imread(badminton_rac_image_path, cv.IMREAD_UNCHANGED)

shuttlecock_image_path = 'backend/img/shuttlecock.png'
shuttlecock = cv.imread(shuttlecock_image_path, cv.IMREAD_UNCHANGED)

ball_normal_image_path = 'backend/img/ball_normal.png'
ball_normal = cv.imread(ball_normal_image_path, cv.IMREAD_UNCHANGED)

ball_squeez_image_path = 'backend/img/ball_squeez.png'
ball_squeez = cv.imread(ball_squeez_image_path, cv.IMREAD_UNCHANGED)

pingpong_ball_image_path = 'backend/img/pingpong_ball.png'
pingpong_ball = cv.imread(pingpong_ball_image_path, cv.IMREAD_UNCHANGED)

pingpong_rac_image_path = 'backend/img/pingpong_rac.png'
pingpong_rac = cv.imread(pingpong_rac_image_path, cv.IMREAD_UNCHANGED)

def get_finger_coor(finger, w,h, number):
    return [int(finger.landmark[number].x * w), int(finger.landmark[number].y * h)]

# --- Main Loop ---
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a mirror effect (optional, but common)
    frame = cv.flip(frame, 1)
    h, w, c = frame.shape
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    open_hand = "NO HAND"
    x_y_index = []
    
    if (results.multi_hand_landmarks):
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Get coordinates for the tip of the index finger (landmark 9)
        x_y_index = get_finger_coor(hand_landmarks, w,h,9)
        z_index = hand_landmarks.landmark[9].z
        x_y_pinkey = get_finger_coor(hand_landmarks, w,h,20)
        
        close_hand = is_close_hand(hand_landmarks)
        open_hand = "Close" if close_hand else "Open"
        
        # --- GAME SECTION ---
        if x_y_index:
            match 'pingpong':
                case "badminton":
                    # BADMINTON
                    frame, on_catch_ball, score = badminton(frame, close_hand, badminton_rac, shuttlecock, x_y_index,x_y_pinkey,
                                      w, on_catch_ball, score)
                    
                case 'football':
                    # CATCH BALL
                    score, on_catch_ball, lock_bug_score, frame = catch_ball_game(
                        frame, close_hand, x_y_index, 
                        score, on_catch_ball, lock_bug_score, 
                        football, w, get_finger_coor(hand_landmarks, w,h,12)
                    )
                
                case 'ball':
                    frame, score, lock_bug_score_squeez = squezz_ball(frame, close_hand, ball_normal, ball_squeez, x_y_index, score,
                                                               lock_bug_score_squeez, 0.16)
                
                case 'pingpong':
                    # PINGPONG
                    frame, score, on_catch_ball = pingpong(frame, score, pingpong_rac, pingpong_ball,
                                            get_finger_coor(hand_landmarks, w,h,12), close_hand, abs(z_index),
                                            on_catch_ball)
                    
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )
        
    else:
        pass
        
    # --- Display Info ---
    text_color = [166,216,0][::-1]
    cv.putText(frame, open_hand, (w - 170, 50), cv.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv.LINE_AA)
    cv.putText(frame, f"Score: {score}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv.LINE_AA)
    
    # --- Show Frame ---
    cv.imshow('Hand Detection and Game', frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv.destroyAllWindows()

# -0.0021031429059803486
# -0.0027911739889532328
# -0.0012794340727850795

# -0.08473743498325348
# -0.07776138186454773
# -0.07650122046470642