import cv2 as cv
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,      
    max_num_hands=1,              
    min_detection_confidence=0.35   
)
mp_drawing = mp.solutions.drawing_utils

cap = cv.VideoCapture(0)  

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def is_close_hand(finger, h, w):
    finger_tip_knuckle = [8, 12, 16, 20]
    wrist = 0
    normal_pos = [45.76411318763862, 45.3422366653561, 43.730585931375224, 40.54341424950317]
    diff = 7
    is_close = []
    try:
        for i in range(4):
            is_close.append(normal_pos[0] - distance(
                finger.landmark[finger_tip_knuckle[i]].x * w,
                finger.landmark[finger_tip_knuckle[i]].y * h,
                finger.landmark[wrist].x * w,
                finger.landmark[wrist].y * h
            ) < diff)
        return not any(is_close)
    except:
        return False

# --- SET UP GAME VARIABLES ---
on_catch_ball = False
score = 0
lock_bug_score = True

def move_ball_game(frame, close_hand, x_y_index_knuckle, score, on_catch_ball, lock_bug_score):
    # SETUP
    first_ball_pos = [80, 430]
    final_ball_pos = [209, 290]
    get_ball_dist = 30

    dist_to_start = distance(x_y_index_knuckle[0], x_y_index_knuckle[1], first_ball_pos[0], first_ball_pos[1])
    dist_to_goal = distance(x_y_index_knuckle[0], x_y_index_knuckle[1], final_ball_pos[0], final_ball_pos[1])

    # LOGIC
    if close_hand and dist_to_start <= get_ball_dist:
        on_catch_ball = True
        lock_bug_score = False

    elif on_catch_ball and not close_hand and dist_to_goal <= get_ball_dist and not lock_bug_score:
        score += 1
        on_catch_ball = False
        lock_bug_score = True 

    elif not close_hand:
        on_catch_ball = False

    if on_catch_ball:
        color = (165,29,138)
        cv.circle(frame, x_y_index_knuckle, 40, color, -1)

    color_first_ball = (255, 0, 0) if dist_to_start >= (get_ball_dist + 20) else (255, 0, 255)
    color_final_ball = (0, 255, 0) if dist_to_goal <= get_ball_dist else (0, 0, 255)
    cv.circle(frame, first_ball_pos, 40, color_first_ball, 10)
    cv.circle(frame, final_ball_pos, 40, color_final_ball, 10)

    return score, on_catch_ball, lock_bug_score


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    h, w, c = frame.shape
    open_hand = "NO HAND"
    x_y_index_knuckle = []

    try:
        hand_landmarks = results.multi_hand_landmarks[0]
        try:
            x_y_index_knuckle = [
                int(hand_landmarks.landmark[20].x * w),
                int(hand_landmarks.landmark[20].y * h)
            ]
        except:
            pass

        close_hand = is_close_hand(hand_landmarks, h, w)
        open_hand = "Close" if close_hand else "Open"

        # GAME SECTION
        if x_y_index_knuckle:
            score, on_catch_ball, lock_bug_score = move_ball_game(frame, close_hand, x_y_index_knuckle, score, on_catch_ball, lock_bug_score)

        # Draw hand landmarks
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )
    except:
        pass

    cv.putText(frame, open_hand, (w - 170, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    cv.putText(frame, f"Score: {score}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    cv.imshow('Hand Detection', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
